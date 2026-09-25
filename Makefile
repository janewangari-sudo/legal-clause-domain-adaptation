.PHONY: install test lint validate

install:
	python -m pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check src scripts tests

validate: lint test
	python scripts/validate_repository.py
