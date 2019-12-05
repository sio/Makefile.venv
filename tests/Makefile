PY?=python3
REPODIR:=$(dir $(firstword $(MAKEFILE_LIST)))..
ARGS=

.PHONY: test
test: deps
	cd $(REPODIR) && $(PY) -m unittest $(ARGS)

.PHONY: deps
deps:
	@pwd
	@$(PY) -c "import sys; print('Python ' + sys.version.replace('\n',''))"
	@$(PY) -c "import platform; print(platform.platform())"
	@$(MAKE) --version
	@echo SHELL=$(SHELL)

test-fast: export SKIP_SLOW_TESTS=1
test-fast: test

test-verbose: ARGS+=-v
test-verbose: test
