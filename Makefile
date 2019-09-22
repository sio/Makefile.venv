#
# PELICAN RULES
#

STORAGE?=$(CURDIR)

PELICAN=pelican
INPUTDIR=$(STORAGE)/demo-input
OUTPUTDIR=$(STORAGE)/demo-output
CONFIG=pelican_demo.py
PORT=8000
EXTRAS=


.PHONY: demo
demo: venv
	[ -d "$(INPUTDIR)" ] || mkdir -p "$(INPUTDIR)"
	$(VENV)/$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFIG) $(EXTRAS)


.PHONY: clean
clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)


.PHONY: serve
serve: venv
	cd $(OUTPUTDIR) && $(VENV)/python -m pelican.server $(PORT)


#
# VIRTUAL ENVIRONMENT RULES
#


PY?=python3
VENVDIR=$(STORAGE)/.venv


ifdef OS
	VENV=$(VENVDIR)/Scripts
else
	VENV=$(VENVDIR)/bin
endif


$(VENV)/activate: setup.py
	$(PY) -m venv $(VENVDIR)
	$(VENV)/python -m pip install --upgrade pip
	$(VENV)/pip install -e .
	touch $(VENVDIR)/activate


.PHONY: venv
venv: $(VENV)/activate


$(VENV)/ipython: $(VENV)/activate
	$(VENV)/pip install ipython


.PHONY: ipython
ipython: $(VENV)/ipython
	$(VENV)/ipython


.PHONY: python
python: venv
	$(VENV)/python
