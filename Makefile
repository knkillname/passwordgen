
export PIPENV_VENV_IN_PROJECT=1

.DEFAULT_GOAL := all

.PHONY: venv clean build format lint test coverage all

venv: .venv/bin/python

.venv/bin/python:
	pipenv install --dev

clean:
	rm -rf build dist *.egg-info .mypy_cache .pytest_cache .ruff_cache htmlcov
	rm -f .coverage

build: .venv/bin/python
	pipenv run python -m build

format: .venv/bin/python
	pipenv run isort src tests
	pipenv run black src tests

lint: .venv/bin/python
	pipenv run python -m mypy --strict src
	pipenv run pylint src tests
	pipenv run pydocstyle src

test: .venv/bin/python
	PYTHONPATH=src pipenv run coverage run -m unittest discover -s tests -q

coverage: .venv/bin/python
	pipenv run coverage report -m --fail-under=85
	pipenv run coverage html

all: .venv/bin/python format lint test coverage build
