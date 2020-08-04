# Using pip-compile with Makefile.venv

---

> **Note:** *Described workflow is possible only with v2020.08.04 and newer*

---

*Makefile.venv* supports many non-trivial use cases. One such case is using
`pip-compile` installed into a virtual environment to generate requirements
file that defines that very environment.

As always with *Makefile.venv* all venv related routines are handled
automatically and are totally transparent to user.

The task at hand is twofold:

- We need to automatically generate `requirements.txt` with a Makefile recipe
- We want to use a tool from virtual environment before that virtual
  environment is finalized by *Makefile.venv*

Here is how it can be done:

```Makefile
# We need to explicitly specify this value because by default it's ok for
# requirements.txt to be missing. Providing any non-default value tells
# Makefile.venv that the files listed must exist or be made from recipe.
# This statement MUST come before `include Makefile.venv`
REQUIREMENTS_TXT=requirements.txt


include Makefile.venv


# Save pip-compile path to variable for brevity
# We may omit $(EXE) suffix if we're ok with Windows builds being broken
PIP_COMPILE=$(VENV)/pip-compile$(EXE)


# This and the next recipe MUST be defined after include statement.
# We need to inject pip-compile into virtual environment
# before Makefile.venv finishes working on it, but after venv is created.
# There already exists a target we can add as dependency for this case:
$(PIP_COMPILE): | $(VENV)
	$(VENV)/pip install pip-tools  # or any other installation method
	touch $@


# Our requirements file directly depends upon *.in file and also requires
# pip-compile to be available
requirements.txt: requirements.in | $(PIP_COMPILE)
	$(PIP_COMPILE) --output-file $@ $<
```

And that's all. The rest of the Makefile should be written as usual when
working with *Makefile.venv*: depend on `venv`, call `$(VENV)/entrypoints`,
etc. The trick is to use `$(VENV)` as dependency for `$(PIP_COMPILE)` - that
way we can avoid circular dependency and pip-compile will be installed after
bare venv is created but before *Makefile.venv* attempts to fill it with
packages from 'requirements.txt'.

For example, after adding this rule to the Makefile above:

```Makefile
all: venv
    $(VENV)/pip freeze
```

we can execute `make all` in a folder with only the makefiles and
`requirements.in` - and both `requirements.txt` and full virtual environment
described by it will be created automatically upon first invocation.

---

> Thanks to [@belm0] for [bringing this](https://github.com/sio/Makefile.venv/issues/8)
> to author's attention!

[@belm0]: https://github.com/belm0

---

> Automated tests ensure that this workflow will not break in the future:
> [tests/test_pip_compile.py]

[tests/test_pip_compile.py]: ../tests/test_pip_compile.py

