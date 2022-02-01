PACKAGE = eventline

all: check

check: mypy pylint

mypy:
	mypy $(PACKAGE)

pylint:
	pylint $(PACKAGE)

.PHONY: all check mypy pylint
