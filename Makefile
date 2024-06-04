pyfiles = __init__.py passfail2.py configuration_menu.py config.json
version = 0.2.2

sed_cmds = -e "s/\$$version/'$(version)'/g"

outfile = passfail2-$(version).ankiaddon

.PHONY: addon clean

dist: $(outfile)

clean:
	rm *.ankiaddon

build_info.py: build_info.py.in Makefile
	sed $(sed_cmds) $< > $@

$(outfile): manifest.json $(pyfiles) build_info.py
	zip -r $(outfile) $^

