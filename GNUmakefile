PACKAGE = eventline

all: check test

check: mypy pylint

test: pytest

mypy:
	mypy $(CURDIR)/$(PACKAGE)

pylint:
	pylint $(CURDIR)/$(PACKAGE)

pytest:
	pytest $(CURDIR)/tests

.PHONY: all check mypy pylint
