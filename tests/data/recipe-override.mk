# Makefile for tests/test_recipe_override.py

include {{ Makefile.venv }}

CUSTOM_PACKAGE=noop==1.0

$(VENV):
	$(PY) -m venv $(VENVDIR)
	$(VENV)/python -m pip install --upgrade pip setuptools wheel $(CUSTOM_PACKAGE)

freeze: venv
	$(VENV)/pip freeze
