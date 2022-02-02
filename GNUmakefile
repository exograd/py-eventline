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

package:
	python -m build $(CURDIR)

.PHONY: all check mypy pylint package
