pyfiles = __init__.py passfail2.py
version = 0.2.1

outfile = passfail2-$(version).ankiaddon

.PHONY: addon clean

dist: $(outfile)

clean:
	rm *.ankiaddon

$(outfile): manifest.json $(pyfiles)
	zip -r $(outfile) $^

