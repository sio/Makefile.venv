DEMO_REPO?=sio/bash-complete-partial-path
DEMO_STORAGE?=$(WORKDIR)/demo-github-data
export DEMO_REPO
export DEMO_STORAGE


DEMO_INPUT=$(WORKDIR)/demo-input
DEMO_OUTPUT?=$(WORKDIR)/demo-output
CONFIG=pelican_demo.py
PORT=8000
EXTRAS=


DOCS_OUTPUT?=$(WORKDIR)/public
export DOCS_OUTPUT


.PHONY: demo
demo: venv $(DEMO_STORAGE)/.ready
	[ -d "$(DEMO_INPUT)" ] || mkdir -p "$(DEMO_INPUT)"
	$(VENV)/pip install --upgrade -r requirements.txt  # update theme
	$(VENV)/pelican $(DEMO_INPUT) -o $(DEMO_OUTPUT) -s $(CONFIG) $(EXTRAS)


$(DEMO_STORAGE)/.ready: $(CONFIG)
	$(VENV)/issyours-github $(DEMO_REPO) $(DEMO_STORAGE)
	touch $(DEMO_STORAGE)/.ready


.PHONY: serve
serve: venv
	cd $(DEMO_OUTPUT) && $(VENV)/python -m http.server $(PORT)


.PHONY: clean-demo
clean-demo:
	[ ! -d $(DEMO_OUTPUT) ] || rm -rf $(DEMO_OUTPUT)
	[ ! -d $(DEMO_STORAGE) ] || rm -rf $(DEMO_STORAGE)


.PHONY: docs
docs: venv
	$(VENV)/pip install mkdocs mkdocs-material pygments
	sed -e 's/\bdocs\///g' README.md > docs/index.md
	$(VENV)/mkdocs build


.PHONY: serve-docs
serve-docs: venv
	cd $(DOCS_OUTPUT) && $(VENV)/python -m http.server $(PORT)


.PHONY: clean-docs
clean-docs:
	[ ! -d $(DOCS_OUTPUT) ] || rm -rf $(DOCS_OUTPUT)


.PHONY: test
test: venv
	$(VENV)/python -m unittest


.PHONY: clean
clean: clean-demo clean-docs clean-venv


include Makefile.venv
