"""Unit tests for i18n loading behavior."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from passwordgen import i18n


class TestI18n(unittest.TestCase):
    """Validate translation loading from locale catalogs."""

    def test_load_translations_from_passwordgen_po(self) -> None:
        """passwordgen.po should be loaded as fallback when .mo is unavailable."""

        with tempfile.TemporaryDirectory() as tmpdir:
            po_dir = Path(tmpdir) / "es" / "LC_MESSAGES"
            po_dir.mkdir(parents=True, exist_ok=True)
            (po_dir / "passwordgen.po").write_text(
                "\n".join(
                    [
                        'msgid ""',
                        'msgstr ""',
                        '"Language: es\\n"',
                        '',
                        'msgid "Secure Password Generator"',
                        'msgstr "Generador de Contrasenas Seguras"',
                        '',
                    ]
                ),
                encoding="utf-8",
            )

            with (
                patch("passwordgen.i18n._LOCALES_DIR", Path(tmpdir)),
                patch("passwordgen.i18n._preferred_languages", return_value=["es"]),
            ):
                translations = i18n._load_translations()  # pylint: disable=protected-access

            self.assertEqual(
                translations.gettext("Secure Password Generator"),
                "Generador de Contrasenas Seguras",
            )
