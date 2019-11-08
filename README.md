# Seamlessly manage Python virtual environment with a Makefile

`Makefile.venv` takes care of creating, updating and invoking Python virtual
environment that you can use in your Makefiles. It will allow you to reduce
venv related routines to almost zero!


## Installation

### Recommended method

Copy [`Makefile.venv`](Makefile.venv) to your project directory and add
include statement to the bottom of your `Makefile`:

```make
include Makefile.venv
```

### Alternative method

Alternatively, you can add installation actions as the Makefile rule:

> **Note the checksum step!** Do not skip it, it would be as bad as [piping curl
> to shell](https://0x46.net/thoughts/2019/04/27/piping-curl-to-shell/)!

```make
include Makefile.venv
Makefile.venv:
	curl \
		-o Makefile.fetched \
		-L "https://github.com/sio/Makefile.venv/raw/v2019.11.07/Makefile.venv"
	echo "74d3b4ddfd18c3dea4a271640b73b73e1640710cd18a109f6623bd888a5fbcf9 *Makefile.fetched" \
		| sha256sum --check - \
		&& mv Makefile.fetched Makefile.venv
```


## Usage

When writing your Makefile use `$(VENV)/python` to refer to the Python
interpreter within virtual environment and `$(VENV)/executablename` for any
other executable in venv.

This Makefile provides the following targets:

- `venv` - use this as a dependency for any target that requires virtual
  environment to be created and configured
- `python, ipython` - use these to launch interactive Python shell within
  virtual environment
- `shell, bash, zsh` - launch interactive command line shell. `shell` target
  launches the default shell Makefile executes its rules in (usually /bin/sh).
  `bash` and `zsh` can be used to refer to the specific desired shell.
- `show-venv` - show versions of Python and pip, and the path to the virtual
  environment
- `clean-venv` - remove virtual environment
- `$(VENV)/executable_name` - install `executable_name` with pip.

  Only packages with names matching the name of the corresponding executable
  are supported.

  Use this as a lightweight mechanism for development dependencies tracking.
  E.g. for one-off tools that are not required in every developer's
  environment, therefore are not included into `requirements.txt` or `setup.py`.

  **Note:** Rules using such dependency MUST be defined below
  `include` directive to make use of correct $(VENV) value.

  Example (see `ipython` target for another example):

```Makefile
    codestyle: $(VENV)/pyflakes
        $(VENV)/pyflakes .
```

This Makefile can be configured via following variables:

- `PY` - Command name for system Python interpreter. It is used only initially
  to create the virtual environment. *Default: python3*
- `WORKDIR` - Parent directory for the virtual environment. *Default: current
  working directory*
- `VENVDIR` - Python virtual environment directory. *Default: $(WORKDIR)/.venv*

This Makefile was written for GNU Make and may not work with other make
implementations.

This Makefile has been tested both on Linux and on Windows (Msys). Any
inconsistency encountered when running on Windows should be considered a bug
and should be reported via [issues].


## Samples

Makefile:

```make
.PHONY: test
test: venv
	$(VENV)/python -m unittest

include Makefile.venv
```

Larger sample from a real project can be seen
[here](https://github.com/sio/issyours/blob/master/Makefile).
Also see [an introductory blog
post](https://potyarkin.ml/posts/2019/manage-python-virtual-environment-from-your-makefile/)
from project author.

Command line:

```
$ make test

...Skipped: creating and updating virtual environment...

...
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```
```
$ make show-venv
Python 3.5.4 (v3.5.4:3f56838, Aug  8 2017, 02:07:06) [MSC v.1900 32 bit (Intel)]
pip 19.2.3 from c:\users\99e7~1\appdata\local\temp\.venv\lib\site-packages\pip (python 3.5)
venv: C:\Users\99E7~1\AppData\Local\Temp\.venv
```
```
$ make python
C:/Users/99E7~1/AppData/Local/Temp/.venv/Scripts/python
Python 3.5.4 (v3.5.4:3f56838, Aug  8 2017, 02:07:06) [MSC v.1900 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> _
```


## Demo screencast

<a href="https://asciinema.org/a/279646" target="_blank">
<img src="https://asciinema.org/a/279646.svg" title="Demo screencast"/>
</a>


## Support and contributing

If you need help with using this Makefile or including it into your project,
please create **[an issue][issues]**.
Issues are also the primary venue for reporting bugs and posting feature
requests. General discussion related to this project is also acceptable and
very welcome!

In case you wish to contribute code or documentation, feel free to open
**[a pull request](https://github.com/sio/Makefile.venv/pulls)**. That would
certainly make my day!

I'm open to dialog and I promise to behave responsibly and treat all
contributors with respect. Please try to do the same, and treat others the way
you want to be treated.

If for some reason you'd rather not use the issue tracker, contacting me via
email is OK too. Please use a descriptive subject line to enhance visibility
of your message. Also please keep in mind that public discussion channels are
preferable because that way many other people may benefit from reading past
conversations. My email is visible under the GitHub profile and in the commit
log.

[issues]: https://github.com/sio/Makefile.venv/issues


## License and copyright

Copyright 2019 Vitaly Potyarkin

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
