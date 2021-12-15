all: venv
	$(VENV)/pyflakes --help


clean: clean-venv
	-$(RM) Makefile.venv requirements.txt


# You need to explicitly specify this value because by default it's ok for
# requirements.txt to be missing. This statement MUST come before `include
# Makefile.venv`
REQUIREMENTS_TXT=requirements.txt  requirements.txt   # add trailing whitespace


# Save pip-compile path to variable for brevity
PIP_COMPILE=$(VENV)/pip-compile$(EXE)


include {{ Makefile.venv }}


# You need to inject pip-compile into virtual environment
# before Makefile.venv finishes working on it, but after venv is created.
# There already exists a target you can add as dependency for this case:
$(PIP_COMPILE): | $(VENV)
	$(VENV)/pip install pip-tools
	$(call touch,$@)


# Your requirements file directly depends upon *.in file and also requires
# pip-compile to be available
requirements.txt: requirements.in | $(PIP_COMPILE)
	$(PIP_COMPILE) --output-file $@ $<
