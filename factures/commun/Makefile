.PHONY: clean
all: $(addsuffix .pdf,$(basename $(basename $(wildcard *.html.jinja2))))

../commun/.venv:
	virtualenv -p python3 $(PWD)/../commun/.venv
	$(PWD)/../commun/.venv/bin/pip install jinja2-cli weasyprint

clean:
	rm -rf $(PWD)/../commun/.venv

%.pdf: %.html ../commun/.venv
	$(PWD)/../commun/.venv/bin/weasyprint $< $@

%.html: %.html.jinja2 ../commun/.venv
	$(PWD)/../commun/.venv/bin/jinja2 $< -D number=$* -D date=$(shell date +%x) > $@
