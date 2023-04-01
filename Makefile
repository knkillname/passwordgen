PIPENV_VENV_IN_PROJECT:=1
export PIPENV_VENV_IN_PROJECT

.phony: clean
clean:
	git clean -Xdf

.phony: test
test: .venv
	# Format code isort and black
	pipenv run isort ./src ./tests
	pipenv run black ./src ./tests
	
	# Lint code with flake8
	pipenv run flake8 ./src ./tests

	# Run unit tests
	pipenv run python -m unittest discover -v -s ./tests -p 'test_*.py'

env: .venv
.venv: Pipfile Pipfile.lock
	pipenv install --dev
