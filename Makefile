pyfiles = __init__.py passfail2.py logger.py config.py configuration_menu.py
version = 0.3.0

sed_cmds = -e "s/\$$version/'$(version)'/g"

outfile = passfail2-$(version).ankiaddon

.PHONY: addon clean

dist: $(outfile)

clean:
	rm *.ankiaddon

build_info.py: build_info.py.in Makefile
	sed $(sed_cmds) $< > $@

$(outfile): manifest.json config.json $(pyfiles) build_info.py
	zip -r $(outfile) $^

