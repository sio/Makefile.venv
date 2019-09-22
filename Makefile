PY?=python3
PELICAN=pelican
INPUTDIR=demo-input
OUTPUTDIR=demo-output
CONFIG=pelican_demo.py
PORT=8000
EXTRAS=


VENVDIR=$(CURDIR)/demo-venv
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


$(VENV)/ipython: $(VENV)/activate
	$(VENV)/pip install ipython


.PHONY: python
python: venv
	$(VENV)/python


.PHONY: ipython
ipython: $(VENV)/ipython
	$(VENV)/ipython


.PHONY: venv
venv: $(VENV)/activate


.PHONY: demo
demo: venv
	$(VENV)/$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFIG) $(EXTRAS)


.PHONY: clean
clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)


.PHONY: serve
serve: venv
	cd $(OUTPUTDIR) && $(VENV)/python -m pelican.server $(PORT)
