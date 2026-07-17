# Copilot Instructions for passwordgen

## Project summary

`passwordgen` is a **secure password generator** (v2.0.0) with a Tkinter GUI and three CLI generation strategies: random symbols, random words (passphrases), and alternating words+symbols. Includes entropy-based strength evaluation and i18n (English `/` Spanish). Licensed under MIT.

- **Language**: Python 3.14+
- **GUI toolkit**: Tkinter (stdlib, no extra deps)
- **Package manager**: Pipenv (with `PIPENV_VENV_IN_PROJECT=1`)
- **Type checker**: mypy `--strict`
- **Linters**: pylint (10.00/10 target), pydocstyle (numpy convention)
- **Formatter**: black (88 cols) + isort (black profile)
- **Test framework**: unittest with coverage (≥85% threshold)
- **Build backend**: setuptools via `python -m build`
- **CI**: GitHub Actions (`.github/workflows/python-app.yml`) on push/PR to `main` & `develop`

**Repo size**: ~30 Python source files, ~70 tests.

---

## How to build and validate

### ALWAYS bootstrap first

```bash
cd /home/mario/Proyectos/passwordgen
PIPENV_VENV_IN_PROJECT=1 pipenv install --dev
```

The `PIPENV_VENV_IN_PROJECT=1` env var is **critical** — it creates `.venv/` inside the project so the Makefile targets can find it. Omit it and the venv goes to `~/.local/share/virtualenvs/` and Makefile targets will fail.

### Format (always run before committing)

```bash
pipenv run isort src tests
pipenv run black src tests
```

### Lint (always run after formatting)

```bash
pipenv run python -m mypy --strict src
pipenv run pylint src tests
pipenv run pydocstyle src
```

**IMPORTANT**: Always use `pipenv run python -m mypy --strict src`, NOT `pipenv run mypy --strict src`. The latter can fail if the `mypy` entrypoint is not found in PATH after `git clean -xdf`.

### Test (always run before considering work done)

```bash
PYTHONPATH=src pipenv run coverage run --rcfile=pyproject.toml -m unittest discover -s tests -q
```

**CRITICAL**: `PYTHONPATH=src` is mandatory. Also, use `discover -s tests`, NOT plain `-m unittest -q` — the latter does not find tests.

The test suite has **70 tests** across 9 files. Expected output: `Ran 70 tests in ... OK`.

### Coverage check

```bash
pipenv run coverage report --rcfile=pyproject.toml -m --fail-under=85
```

Coverage must be ≥85%. The following modules are **excluded** from coverage (defined in `pyproject.toml`):
- `__main__.py`
- `gui/*` (Tkinter code — hard to test headlessly)
- `wordlists/downloader.py` (network-dependent)
- `i18n.py` (locale-dependent)

### Build

```bash
pipenv run python -m build
```

### Full pipeline (via Makefile)

```bash
make all   # format → lint → test → coverage → build
```

You can also run individual steps: `make format`, `make lint`, `make test`, `make coverage`, `make build`, `make clean`.

---

## ⚠️ Known pitfalls

### Black + pylint interaction

After `make format`, **re-run `make lint` immediately**. Black sometimes moves `# pylint: disable=protected-access` inline comments to a different line than the access they suppress. This causes pylint to fail with `W0212: Access to a protected member`. If this happens, add the pylint disable comment on the **same line** as the protected access, not on the closing parenthesis line. Affected file: `tests/test_i18n.py`.

### CI vs local Python version mismatch

The CI workflow uses **Python 3.11** (hardcoded in `.github/workflows/python-app.yml`), but `pyproject.toml` requires `>=3.14`. The workflow also does **not** run `make all` — it runs lint and test steps individually **without** formatting first. This means CI-visible formatting issues won't be caught in CI; they must be caught locally.

### Test output noise

The test suite prints `usage: passwordgen ... error: unrecognized arguments: --not-a-real-option` to stderr. This is **expected** — it comes from a test that validates argparse error handling. Do not treat it as a failure.

### Configuration location

User config is stored at `$XDG_CONFIG_HOME/passwordgen/config.json` (default: `~/.config/passwordgen/config.json`). Tests use `tempfile.TemporaryDirectory` to avoid touching real config.

---

## Project layout and architecture

```
.
├── .github/workflows/python-app.yml   # CI pipeline
├── Makefile                           # All build/dev targets
├── Pipfile / Pipfile.lock             # Pipenv deps (Python 3.14)
├── pyproject.toml                     # All tool config (black, isort, mypy, pylint, pydocstyle, coverage, build)
├── passwordgen.sh                     # Shell wrapper (sets PYTHONPATH)
├── src/passwordgen/                   # Package source
│   ├── __init__.py                    # Package metadata, __version__ = "2.0.0"
│   ├── __main__.py                    # python -m passwordgen entry
│   ├── cli.py                         # CLI: argparse, CommandLineApp, cli()
│   ├── i18n.py                        # gettext + .po fallback translations (excluded from coverage)
│   ├── strength.py                    # PasswordStrengthEvaluator, StrengthLevel, StrengthResult
│   ├── config/
│   │   ├── __init__.py
│   │   ├── manager.py                 # ConfigManager: JSON load/save/merge at XDG path
│   │   └── schema.py                  # Dataclasses: AppConfig, SymbolsDefaults, WordsDefaults, AlternatingDefaults, WordlistsConfig
│   ├── generators/
│   │   ├── __init__.py
│   │   ├── base.py                    # ABC PasswordGenerator with abstract generate()
│   │   ├── symbols.py                 # RandomSymbolsGenerator + SymbolsConfig
│   │   ├── words.py                   # RandomWordsGenerator + WordsConfig
│   │   └── alternating.py             # AlternatingGenerator + AlternatingConfig
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── app.py                     # tk.Tk App: tabs, batch spinbox, theme support
│   │   ├── config_frames.py           # SymbolsConfigFrame, WordsConfigFrame, AlternatingConfigFrame
│   │   ├── results_frame.py           # ResultsFrame: listbox, strength bar, crack-time estimation
│   │   └── settings_dialog.py         # SettingsDialog: wordlist download, all defaults editing
│   ├── wordlists/
│   │   ├── __init__.py                # WordlistLoader, available_dictionary_keys(), embedded map
│   │   ├── downloader.py              # HunspellDownloader (excluded from coverage)
│   │   ├── eff_large.txt              # English EFF wordlist
│   │   └── spanish.txt                # Spanish wordlist
│   └── locales/es/LC_MESSAGES/
│       └── passwordgen.po             # Spanish translations (PO fallback)
└── tests/
    ├── __init__.py                    # (empty)
    ├── test_main.py                   # CLI/GUI entry point tests
    ├── test_strength.py               # Strength evaluator tests
    ├── test_config_manager.py         # Config load/save/merge tests
    ├── test_symbols_generator.py      # Symbols generator tests
    ├── test_words_generator.py        # Words generator tests
    ├── test_alternating_generator.py  # Alternating generator tests
    ├── test_i18n.py                   # i18n loading tests
    ├── test_wordlist_loader.py        # Wordlist loading tests
    └── test_hunspell_processor.py     # Hunspell parsing tests
```

### Key architectural patterns

- **Config schema**: `AppConfig` is a nested dataclass tree. All sub-configs use `slots=True`. `ConfigManager.load()` merges JSON overrides onto defaults.
- **Generator interface**: `PasswordGenerator` (ABC in `base.py`) with `generate(config) -> str`. Each algorithm has its own config dataclass. Words/Alternating generators accept `WordlistLoader` + `WordlistsConfig` via constructor.
- **i18n**: Custom `_()` function. Falls back from `.mo` → `.po` → null translations. Locale detected from `$LANG`.
- **Strength**: `PasswordStrengthEvaluator.evaluate()` returns `StrengthResult` with entropy bits, score 0-100, level enum, and feedback list.
- **GUI**: Excluded from coverage. Not tested in CI. Use `--gui` flag to launch.

### Adding a new generator

1. Create config dataclass + generator class inheriting `PasswordGenerator` in `src/passwordgen/generators/`
2. Export from `generators/__init__.py`
3. Add subparser in `cli.py` `_build_parser()` and handler in `_run_cli()`
4. Add config frame in `gui/config_frames.py` and tab in `gui/app.py`
5. Add default config in `config/schema.py` `AppConfig`
6. Add tests in `tests/`

---

## Trust these instructions

These instructions have been validated by running every command and observing every pitfall. **Only perform additional exploration if the information here is incomplete or found to be in error.** Avoid re-discovering build steps, test commands, or lint rules through trial and error — they are documented above.
