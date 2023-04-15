# Instruct Pipenv to create .venv directory in project root
PIPENV_VENV_IN_PROJECT:=1
export PIPENV_VENV_IN_PROJECT

# Instruct Pipenv to hide verbose output
PIPENV_VERBOSITY=-1
export PIPENV_VERBOSITY

.phony: lint format clean test default

# Default target
default: env format lint test

# Create virtual environment
env: .venv
.venv: Pipfile Pipfile.lock
	pipenv install --dev

# Format code
format:
	pipenv run isort ./src ./tests
	pipenv run black ./src ./tests

# Lint code
lint:
	pipenv run isort --check-only --diff ./src ./tests
	pipenv run flake8 ./src ./tests
	pipenv run mypy ./src ./tests

# Run tests
test: .venv
	pipenv run python -m unittest discover -v -s ./tests -p 'test_*.py'

# Clean up
clean:
	git clean -Xdf
