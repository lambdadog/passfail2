pyfiles = __init__.py passfail2.py configuration_menu.py button_color.py config.json
version = 0.2.2

outfile = passfail2-$(version).ankiaddon

.PHONY: addon clean

dist: $(outfile)

clean:
	rm *.ankiaddon

$(outfile): manifest.json $(pyfiles)
	zip -r $(outfile) $^

