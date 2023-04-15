# Instruct Pipenv to create .venv directory in project root
PIPENV_VENV_IN_PROJECT:=1
export PIPENV_VENV_IN_PROJECT

# Instruct Pipenv to hide verbose output
PIPENV_VERBOSITY=-1
export PIPENV_VERBOSITY

.phony: lint format clean test default pipenv_check

# Default target
default: pipenv_check env format lint test

pipenv_check:
	@which pipenv > /dev/null || (echo "Pipenv not found. Please install it first." && exit 1)

# Create virtual environment
env: .venv
.venv: Pipfile Pipfile.lock
	make pipenv_check
	pipenv install --dev

# Format code
format: pipenv_check
	pipenv run isort ./src ./tests
	pipenv run black ./src ./tests

# Lint code
lint: pipenv_check
	pipenv run flake8 ./src ./tests
	pipenv run mypy ./src ./tests
	pipenv run isort --check-only --diff ./src ./tests
	pipenv run pydocstyle ./src ./tests

# Run tests
test: pipenv_check .venv
	pipenv run python -m unittest discover -v -s ./tests -p 'test_*.py'

# Clean up
clean:
	git clean -Xdf
