DEMO_REPO?=sio/bash-complete-partial-path
DEMO_STORAGE?=$(WORKDIR)/demo-github-data
DEMO_THEME?=$(CURDIR)/../pelican-alchemy/alchemy
export DEMO_REPO
export DEMO_STORAGE
export DEMO_THEME


PELICAN=pelican
DEMO_INPUT=$(WORKDIR)/demo-input
DEMO_OUTPUT?=$(WORKDIR)/demo-output
CONFIG=pelican_demo.py
PORT=8000
EXTRAS=


.PHONY: demo
demo: venv $(DEMO_STORAGE)/.ready
	[ -d "$(DEMO_INPUT)" ] || mkdir -p "$(DEMO_INPUT)"
	$(VENV)/$(PELICAN) $(DEMO_INPUT) -o $(DEMO_OUTPUT) -s $(CONFIG) $(EXTRAS)


$(DEMO_STORAGE)/.ready: $(CONFIG)
	$(VENV)/issyours-github $(DEMO_REPO) $(DEMO_STORAGE)
	touch $(DEMO_STORAGE)/.ready


.PHONY: test
test: venv
	$(VENV)/python -m unittest


.PHONY: clean-demo
clean-demo:
	[ ! -d $(DEMO_OUTPUT) ] || rm -rf $(DEMO_OUTPUT)
	[ ! -d $(DEMO_STORAGE) ] || rm -rf $(DEMO_STORAGE)


.PHONY: serve
serve: venv
	cd $(DEMO_OUTPUT) && $(VENV)/python -m pelican.server $(PORT)


.PHONY: clean
clean: clean-demo clean-venv


include Makefile.venv
