PACKAGE = eventline

all: check test

check: mypy pylint

test: pytest

mypy:
	mypy $(PACKAGE)

pylint:
	pylint $(PACKAGE)

pytest:
	pytest $(CURDIR)/tests

.PHONY: all check mypy pylint
