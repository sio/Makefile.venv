PACKAGE_ROOT=src/Makefile_venv


include ../Makefile.venv


.PHONY: package build
package build: dist


dist: setup.cfg pyproject.toml
dist: $(PACKAGE_ROOT)/LICENSE
dist: $(PACKAGE_ROOT)/Makefile.venv
dist: $(PACKAGE_ROOT)/README.md
dist: | $(VENV)/build
	-$(RM) -rv dist
	$(VENV)/python -m build


$(PACKAGE_ROOT)/%: ../%
	cp $< $@


.PHONY: upload
upload: dist | $(VENV)/twine
	$(VENV)/twine upload --repository testpypi $(TWINE_ARGS) dist/*
	$(VENV)/twine upload $(TWINE_ARGS) dist/*


.PHONY: test
test: | $(VENV)/tox
	$(VENV)/tox $(TOX_ARGS)


.PHONY: clean
clean:
	git clean -idx
