PELICAN=pelican
INPUT=demo-input
OUTPUT=demo-output
CONFIG=pelican_demo.py
EXTRAS=


demo:
	$(PELICAN) $(INPUT) -o $(OUTPUT) -s $(CONFIG) $(EXTRAS)


clean:
	[ ! -d $(OUTPUT) ] || rm -rf $(OUTPUT)


.PHONY: demo clean
