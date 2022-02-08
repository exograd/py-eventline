PACKAGE = eventline

all: check test

check: mypy pylint

test: pytest

mypy:
	python -m mypy $(CURDIR)/$(PACKAGE)

pylint:
	python -m pylint $(CURDIR)/$(PACKAGE)

pytest:
	python -m pytest $(CURDIR)/tests

tox:
	cd $(CURDIR) && python -m tox

package:
	$(RM) -r $(CURDIR)/dist
	python -m build $(CURDIR)

release: package
	twine upload --skip-existing $(CURDIR)/dist/*

.PHONY: all check mypy pylint package
