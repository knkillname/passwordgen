"""Internationalization utilities for GUI text translation."""

from __future__ import annotations

import ast
import gettext
import locale
import os
from pathlib import Path

_DOMAIN = "passwordgen"
_LOCALES_DIR = Path(__file__).resolve().parent / "locales"


class _POTranslations(gettext.NullTranslations):
    """Simple translation catalog loaded from a `.po` file."""

    def __init__(self, catalog: dict[str, str]) -> None:
        super().__init__()
        self._catalog = catalog

    def gettext(self, message: str) -> str:
        return self._catalog.get(message, message)


def _unquote_po_string(raw: str) -> str:
    """Decode a PO quoted string literal."""

    return str(ast.literal_eval(raw))


def _parse_po_catalog(po_path: Path) -> dict[str, str]:
    """Parse PO file contents into a translation catalog."""

    if not po_path.exists():
        return {}

    catalog: dict[str, str] = {}
    current_id: list[str] = []
    current_str: list[str] = []
    mode = ""

    def flush() -> None:
        if not current_id:
            return
        msgid = "".join(current_id)
        msgstr = "".join(current_str)
        if msgid:
            catalog[msgid] = msgstr or msgid

    for raw_line in po_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("msgid "):
            flush()
            current_id = [_unquote_po_string(line[6:])]
            current_str = []
            mode = "id"
            continue
        if line.startswith("msgstr "):
            current_str = [_unquote_po_string(line[7:])]
            mode = "str"
            continue
        if line.startswith('"'):
            if mode == "id":
                current_id.append(_unquote_po_string(line))
            elif mode == "str":
                current_str.append(_unquote_po_string(line))
    flush()
    return catalog


def _preferred_languages() -> list[str]:
    """Return preferred language codes derived from current locale."""

    lang = locale.getlocale()[0]
    if not lang:
        lang = os.environ.get("LANG", "")
        if "." in lang:
            lang = lang.split(".", maxsplit=1)[0]
    if not lang:
        return []
    short = lang.split("_", maxsplit=1)[0].lower()
    return [short, lang]


def _load_translations() -> gettext.NullTranslations:
    """Load translations using `.mo` if available, else `.po` fallback."""

    languages = _preferred_languages()
    if not languages:
        return gettext.NullTranslations()

    try:
        return gettext.translation(
            _DOMAIN,
            localedir=str(_LOCALES_DIR),
            languages=languages,
            fallback=False,
        )
    except OSError:
        po_path = _LOCALES_DIR / languages[0] / "LC_MESSAGES" / f"{_DOMAIN}.po"
        catalog = _parse_po_catalog(po_path)
        if catalog:
            return _POTranslations(catalog)
        return gettext.NullTranslations()


_TRANSLATIONS = _load_translations()


def _(message: str) -> str:
    """Translate a text message for the current locale."""

    return _TRANSLATIONS.gettext(message)
