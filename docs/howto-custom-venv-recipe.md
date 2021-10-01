# Using custom Makefile recipe to create virtual environment

Sometimes assumptions made by *Makefile.venv* about how virtual environment
should be created seem too rigid. Using venv module from standard library and
always installing the latest version of pip, setuptools and wheel is a sane
default, but users may want to:

- Use another tool to create the virtual environment ([virtualenv] anyone?)
  *or*
- Pass some [extra command line arguments] to venv module
  *or*
- Specify which [versions of pip/setuptools/wheel] to use instead of latest.

There is a way to do all of that.

You can provide an alternative recipe for venv creation after you include
*Makefile.venv*:

```makefile
CUSTOM_INITIAL_PACKAGES=path/to/your/requirements-for-pip-wheel-setuptools.txt
$(VENV):
	$(PY) -m venv $(VENVDIR)
	$(VENV)/python -m pip install -r $(CUSTOM_INITIAL_PACKAGES)
```

Here is [another example] where the last supported pip version is used when
outdated Python interpreter is detected:

```makefile
# Override default venv packages for older Python versions
ifeq (True,$(shell $(PY) -c "import sys; print(sys.version_info < (3,5))"))
$(VENV):
	$(PY) -m venv $(VENVDIR)
	$(VENV)/python -m pip install --upgrade "pip<19.2" "setuptools<44.0" "wheel<0.34"
endif
```

It works because GNU Make allows to [redefine the recipe] for any target later
in the Makefile. Downside is that this usage is not officially endorsed and
GNU Make will spit out some warnings:

```
Makefile:46: warning: overriding recipe for target '.venv/bin'
Makefile.venv:137: warning: ignoring old recipe for target '.venv/bin'
```

Despite the small drawback this solution allows for endless customization at
practically zero cost. There is no way we could predict all oddly specific
requests that users may come up with, let alone add variables and feature
flags to support those. But with custom recipes users can define their venv
whichever way they need.

[Alternative suggestion] with `*-default` targets was considered and rejected
because of being too invasive and producing unexpected outcomes in some
scenarios.
See more [here](https://github.com/sio/Makefile.venv/issues/13#issuecomment-928932526)

[virtualenv]: https://pypi.org/project/virtualenv/
[extra command line arguments]: https://github.com/sio/Makefile.venv/pull/10
[versions of pip/setuptools/wheel]: https://github.com/sio/Makefile.venv/issues/13
[another example]: https://github.com/sio/bash-complete-partial-path/blob/2be6ef1f1885d3cb1ec2547ae41d78aa66f4ab78/Makefile#L42-L48
[redefine the recipe]: https://www.gnu.org/software/make/manual/html_node/Multiple-Rules.html
[Alternative suggestion]: https://stackoverflow.com/questions/11958626/m/49804748#49804748

---

> Thanks to [@belm0] and [@simaoafonso-pwt] for bringing this to author's attention!

[@belm0]: https://github.com/belm0
[@simaoafonso-pwt]: https://github.com/simaoafonso-pwt

---

> Automated tests ensure that this workflow will not break in the future:
> [tests/test_recipe_override.py]

[tests/test_recipe_override.py]: ../tests/test_recipe_override.py
