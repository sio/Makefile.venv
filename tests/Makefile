PY?=python3
REPODIR:=$(dir $(firstword $(MAKEFILE_LIST)))..

test:
	cd $(REPODIR) && $(PY) -m unittest -v
