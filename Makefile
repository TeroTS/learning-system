VENV := .venv
BIN := $(VENV)/bin
PYTHON ?= python$(shell cat .python-version)

.PHONY: install fmt fmt-check lint test coverage check

install:
	$(PYTHON) -m venv --clear $(VENV)
	$(BIN)/pip install -q -r requirements-dev.txt

fmt:
	$(BIN)/ruff format .

fmt-check:
	$(BIN)/ruff format --check .

lint:
	$(BIN)/ruff check .

test:
	$(BIN)/python -m unittest discover -s tests -t .

coverage:
	$(BIN)/coverage run -m unittest discover -s tests -t .
	$(BIN)/coverage report

check: fmt-check lint coverage
