PACKAGE_ROOT=src/Makefile_venv
PACKAGE_DATA=\
	$(PACKAGE_ROOT)/LICENSE \
	$(PACKAGE_ROOT)/Makefile.venv \
	$(PACKAGE_ROOT)/README.md


include ../Makefile.venv


.PHONY: package build
package build: dist


dist: setup.cfg pyproject.toml Makefile
dist: $(PACKAGE_DATA)
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
test: $(PACKAGE_DATA)
test: | $(VENV)/tox
	$(VENV)/tox $(TOX_ARGS)


.PHONY: clean
clean:
	git clean -idx
