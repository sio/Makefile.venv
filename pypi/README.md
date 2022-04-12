# Packaging Makefile.venv for PyPI

This directory contains helper code and configuration files used to build a
Python package for *Makefile.venv* and to upload that package to PyPI.

It is assumed that *Makefile.venv* itself is in a working state when working
on packaging, so we depend on it in multiple places here.

This is also the reason why packaging tests are stored separately from the
rest of test suite: we can not depend on *Makefile.venv* in the main test
suite, but it's too useful to forego when doing auxiliary work.
