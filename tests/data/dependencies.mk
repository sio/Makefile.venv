.DEFAULT: hello

include {{ Makefile.venv }}

hello: venv
	$(VENV)/python hello.py

freeze: venv
	$(VENV)/pip freeze

oneoff: $(VENV)/pyflakes
	$(VENV)/pyflakes --help
