# Changelog for Makefile.venv

<!--Template for new entries


## CURRENT

*
*

[Source code tree](https://github.com/sio/Makefile.venv/tree/CURRENT)
| [Tarball](https://github.com/sio/Makefile.venv/tarball/CURRENT)
| [Commit history](https://github.com/sio/Makefile.venv/compare/PREVIOUS...CURRENT)
-->


## v2019.12.04

* New configuration variable: FORCE_UNIX_PATHS. If this variable is set,
  unix-like file paths are assumed and no Windows detection takes place.
  Thanks to [@jpc4242](https://github.com/jpc4242) for reporting
  [the issue](https://github.com/sio/Makefile.venv/issues/2) with Cygwin.

[Source code tree](https://github.com/sio/Makefile.venv/tree/v2019.12.04)
| [Tarball](https://github.com/sio/Makefile.venv/tarball/v2019.12.04)
| [Commit history](https://github.com/sio/Makefile.venv/compare/v2019.11.22...v2019.12.04)


## v2019.11.22

* Upgrade pip only at initial environment creation. This helps to avoid build
  failures with old Python versions where pip can not be upgraded to newer
  releases. [Example](https://circleci.com/gh/sio/bash-complete-partial-path/53)

[Source code tree](https://github.com/sio/Makefile.venv/tree/v2019.11.22)
| [Tarball](https://github.com/sio/Makefile.venv/tarball/v2019.11.22)
| [Commit history](https://github.com/sio/Makefile.venv/compare/v2019.11.08...v2019.11.22)


## v2019.11.08

* Support multiple requirements.txt files via REQUIREMENTS_TXT environment
  variable

[Source code tree](https://github.com/sio/Makefile.venv/tree/v2019.11.08)
| [Tarball](https://github.com/sio/Makefile.venv/tarball/v2019.11.08)
| [Commit history](https://github.com/sio/Makefile.venv/compare/v2019.11.07...v2019.11.08)


## v2019.11.07

* Virtual environment creation happens only once. Dependencies change does not
  trigger a redundant call to `-m venv` if environment already exists.

[Source code tree](https://github.com/sio/Makefile.venv/tree/v2019.11.07)
| [Tarball](https://github.com/sio/Makefile.venv/tarball/v2019.11.07)
| [Commit history](https://github.com/sio/Makefile.venv/compare/v2019.11.06...v2019.11.07)


## v2019.11.06

* New pattern rule for rarely used dependencies (CLI tools in virtual
  environment)
* Improved code readability and documentation

[Source code tree](https://github.com/sio/Makefile.venv/tree/v2019.11.06)
| [Tarball](https://github.com/sio/Makefile.venv/tarball/v2019.11.06)
| [Commit history](https://github.com/sio/Makefile.venv/compare/v2019.10.04...v2019.11.06)


## v2019.10.04

* Automated testing for new releases with GitHub CI
* Deduplicated code for interactive shell targets

[Source code tree](https://github.com/sio/Makefile.venv/tree/v2019.10.04)
| [Tarball](https://github.com/sio/Makefile.venv/tarball/v2019.10.04)
| [Commit history](https://github.com/sio/Makefile.venv/compare/v2019.10.03...v2019.10.04)


## v2019.10.03

* Cleaner process tree thanks to launching interactive shells via `exec`

[Source code tree](https://github.com/sio/Makefile.venv/tree/v2019.10.03)
| [Tarball](https://github.com/sio/Makefile.venv/tarball/v2019.10.03)
| [Commit history](https://github.com/sio/Makefile.venv/compare/v2019.10.01...v2019.10.03)


## v2019.10.01

* New targets for interactive shells in virtual environment:
  `make bash`, `make zsh`
* Promotional post in author's blog: [https://potyarkin.ml/...][blog]

[blog]: https://potyarkin.ml/posts/2019/manage-python-virtual-environment-from-your-makefile/

[Source code tree](https://github.com/sio/Makefile.venv/tree/v2019.10.01)
| [Tarball](https://github.com/sio/Makefile.venv/tarball/v2019.10.01)
| [Commit history](https://github.com/sio/Makefile.venv/compare/v2019.09.30...v2019.10.01)


## v2019.09.30

* First reusable version of Makefile.venv. All essential features are available.

[Source code tree](https://github.com/sio/Makefile.venv/tree/v2019.09.30)
| [Tarball](https://github.com/sio/Makefile.venv/tarball/v2019.09.30)
| [Commit history](https://github.com/sio/Makefile.venv/compare/9c9b6d5aae8955d207d5c9d45b754c01c20be650...v2019.09.30)
