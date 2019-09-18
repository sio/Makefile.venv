PY=python
PELICAN=pelican
INPUT=demo-input
OUTPUT=demo-output
CONFIG=pelican_demo.py
PORT=8000
EXTRAS=


demo:
	$(PELICAN) $(INPUT) -o $(OUTPUT) -s $(CONFIG) $(EXTRAS)


clean:
	[ ! -d $(OUTPUT) ] || rm -rf $(OUTPUT)


serve:
	cd $(OUTPUT) && $(PY) -m pelican.server $(PORT)


.PHONY: demo clean serve
