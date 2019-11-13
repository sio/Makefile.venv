PY?=python3
REPODIR:=$(dir $(firstword $(MAKEFILE_LIST)))..
ARGS=

.PHONY: test
test:
	cd $(REPODIR) && $(PY) -m unittest $(ARGS)

test-fast: export SKIP_SLOW_TESTS=1
test-fast: test

test-verbose: ARGS+=-v
test-verbose: test
