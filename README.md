# Passwordgen

A secure password generator with a Tkinter GUI and multiple generation strategies.

## Features

- **Random symbols** — classic password from a configurable character set.
- **Random words** — passphrase built from an EFF-style word list (English or Spanish).
- **Alternating** — words interspersed with random symbols for a balance of memorability and strength.
- **Strength evaluator** — entropy-based feedback shown alongside every result.
- **Persistent settings** — theme, batch size, and word list preferences are saved between sessions.

## Installation

Requires Python 3.14 or later. Install with [pipx](https://pipx.pypa.io):

```bash
pipx install git+https://github.com/knkillname/passwordgen
```

Then launch the application:

```bash
passwordgen
```

By default, `passwordgen` runs in CLI mode and prints generated passwords.
Use `--gui` when you prefer the desktop interface:

```bash
passwordgen --gui
```

### CLI algorithms

The CLI now uses subcommands, one per algorithm:

```bash
passwordgen symbols --count 3 --length 24
passwordgen words --count 3 --word-count 4 --separator "-" --language es
passwordgen alternating --count 2 --word-count 3 --symbols-per-group 2 --language en
```

Notes:

- `symbols` is the default algorithm when no subcommand is provided.
- `--gui` bypasses subcommands and launches the desktop app.

### Upgrading

```bash
pipx upgrade passwordgen
```

### Uninstalling

```bash
pipx uninstall passwordgen
```

## Development

Clone the repository and set up the environment with [Pipenv](https://pipenv.pypa.io):

```bash
git clone https://github.com/knkillname/passwordgen
cd passwordgen
pipenv install --dev
```

### Common tasks

| Command | Description |
| --- | --- |
| `make all` | Format, lint, test, measure coverage and build |
| `make test` | Run the test suite |
| `make coverage` | Generate an HTML coverage report |
| `make lint` | Run mypy, pylint and pydocstyle |
| `make format` | Auto-format code with isort and black |
| `make build` | Build the distribution package |
| `make clean` | Remove build artefacts and caches |

### Project layout

```
src/passwordgen/   Package source code
tests/             Unit tests
Makefile           Development, quality, coverage and build tasks
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
