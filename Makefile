DEMO_REPO?=sio/bash-complete-partial-path
DEMO_STORAGE?=$(WORKDIR)/demo-github-data
export DEMO_REPO
export DEMO_STORAGE


PELICAN=pelican
DEMO_INPUT=$(WORKDIR)/demo-input
DEMO_OUTPUT?=$(WORKDIR)/demo-output
CONFIG=pelican_demo.py
PORT=8000
EXTRAS=


.PHONY: demo
demo: venv $(DEMO_STORAGE)/.ready
	[ -d "$(DEMO_INPUT)" ] || mkdir -p "$(DEMO_INPUT)"
	$(VENV)/pip install --upgrade -r requirements.txt  # update theme
	$(VENV)/$(PELICAN) $(DEMO_INPUT) -o $(DEMO_OUTPUT) -s $(CONFIG) $(EXTRAS)


$(DEMO_STORAGE)/.ready: $(CONFIG)
	$(VENV)/issyours-github $(DEMO_REPO) $(DEMO_STORAGE)
	touch $(DEMO_STORAGE)/.ready


.PHONY: docs
docs: venv
	$(VENV)/pip install mkdocs mkdocs-material pygments
	sed -e 's/\bdocs\///g' README.md > docs/index.md
	$(VENV)/mkdocs build


.PHONY: serve-docs
serve-docs: venv
	cd public && $(VENV)/python -m http.server


.PHONY: test
test: venv
	$(VENV)/python -m unittest


.PHONY: clean-demo
clean-demo:
	[ ! -d $(DEMO_OUTPUT) ] || rm -rf $(DEMO_OUTPUT)
	[ ! -d $(DEMO_STORAGE) ] || rm -rf $(DEMO_STORAGE)
	[ ! -d public ] || rm -rf public  # specified in mkdocs.yml


.PHONY: serve
serve: venv
	cd $(DEMO_OUTPUT) && $(VENV)/python -m pelican.server $(PORT)


.PHONY: clean
clean: clean-demo clean-venv


include Makefile.venv
