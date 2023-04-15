# Instruct Pipenv to create .venv directory in project root
PIPENV_VENV_IN_PROJECT:=1
export PIPENV_VENV_IN_PROJECT

# Instruct Pipenv to hide verbose output
PIPENV_VERBOSITY=-1
export PIPENV_VERBOSITY

.phony: lint format clean test default check_pipenv

# Default target
default: check_pipenv venv format lint test

# Check if Pipenv is installed
check_pipenv:
	@which pipenv > /dev/null || (echo "Pipenv is not installed. Please install it first." && exit 1)

# Create virtual environment
venv: .venv/bin/activate
.venv/bin/activate: Pipfile Pipfile.lock
	pipenv install --dev
	@touch $@

# Format code
format: check_pipenv venv
	pipenv run isort ./src ./tests
	pipenv run black ./src ./tests

# Lint code
lint: check_pipenv venv
	pipenv run flake8 ./src ./tests
	pipenv run mypy ./src ./tests
	pipenv run isort --check-only --diff ./src ./tests
	pipenv run pydocstyle ./src ./tests

# Run tests
test: check_pipenv venv
	pipenv run coverage run -m unittest discover -v -s ./tests -p 'test_*.py'
	pipenv run coverage html
	pipenv run coverage report -m

# Clean up
clean:
	git clean -Xdf
