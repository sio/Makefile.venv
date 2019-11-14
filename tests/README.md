# Some sanity checks for Makefile.venv

Execute `python -m unittest` from the repo's top directory
or run `make` from the `tests/` directory.

Slow tests can be skipped by setting `SKIP_SLOW_TESTS` environment variable,
e.g. `make SKIP_SLOW_TESTS=1` (shortcut: `make test-fast`)
