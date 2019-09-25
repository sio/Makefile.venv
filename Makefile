include Makefile.venv


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


.PHONY: test
test: venv
	$(VENV)/python -m unittest


.PHONY: clean
clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)


.PHONY: serve
serve: venv
	cd $(OUTPUTDIR) && $(VENV)/python -m pelican.server $(PORT)


.PHONY: clean-all
clean-all: clean clean-venv
