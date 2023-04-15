PIPENV_VENV_IN_PROJECT:=1
export PIPENV_VENV_IN_PROJECT

PIPENV_VERBOSITY=-1
export PIPENV_VERBOSITY

.phony: lint format clean test default

default: format lint test

env: .venv
.venv: Pipfile Pipfile.lock
	pipenv install --dev

lint:
	pipenv run isort --check-only --diff ./src ./tests
	pipenv run flake8 ./src ./tests
	pipenv run mypy ./src ./tests

format:
	pipenv run isort ./src ./tests
	pipenv run black ./src ./tests

test: .venv
	pipenv run python -m unittest discover -v -s ./tests -p 'test_*.py'


clean:
	git clean -Xdf
