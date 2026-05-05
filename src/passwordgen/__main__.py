"""Module entry point for `python -m passwordgen`."""

from passwordgen.cli import cli

if __name__ == "__main__":
    raise SystemExit(cli())
