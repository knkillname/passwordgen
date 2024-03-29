# Instruct Pipenv to create .venv directory in project root
PIPENV_VENV_IN_PROJECT:=1
export PIPENV_VENV_IN_PROJECT

# Instruct Pipenv to hide verbose output
PIPENV_VERBOSITY=-1
export PIPENV_VERBOSITY

.phony: lint format clean test default check_pipenv

# Default target
default: check_pipenv venv format lint test

# Ensure that user packages can be run and install the package
install:
	@if [ ! -z "$${PATH##*:$${HOME}/.local/bin*}" ]; then \
		echo "'~/.local/bin' is not in PATH, so no user packages can run."; \
		echo "would you like to add it to PATH? [y/N]"; \
		read -r response; \
		if [ "$$response" = "y" ]; then \
			if [ -f ~/.bashrc ]; then \
				echo "export PATH=\"$$PATH:$$HOME/.local/bin\"" >> ~/.bashrc; \
			fi; \
			if [ -f ~/.zshrc ]; then \
				echo "export PATH=\"$$PATH:$$HOME/.local/bin\"" >> ~/.zshrc; \
			fi; \
			echo "Please restart your shell to apply changes."; \
		fi; \
	fi
	pip3 install --user --break-system-packages .

uninstall:
	pip3 uninstall --break-system-packages passwordgen

# Check if Pipenv is installed
check_pipenv:
	@which pipenv > /dev/null \
	|| (echo "Pipenv is not installed. Please install it first." && exit 1)

# Create virtual environment
.venv/bin/activate: Pipfile
	pipenv install --dev
	@touch $@
venv: .venv/bin/activate

# Format code
format: check_pipenv venv
	pipenv run isort ./src ./tests
	pipenv run black ./src ./tests

# Lint code
lint: check_pipenv venv
	pipenv run pylint ./src ./tests
	pipenv run mypy --strict ./src ./tests
	pipenv run pydocstyle ./src ./tests
	pipenv run isort --check-only --diff ./src ./tests

# Run tests
test: check_pipenv venv
	pipenv run coverage run -m unittest discover -v -s ./tests -p 'test_*.py'
	pipenv run coverage report -m

# Build package as a wheel
build: check_pipenv venv
	pipenv run pip3 wheel --no-deps --wheel-dir dist .

# Clean up
clean:
	git clean -Xdf
