"""Download and process Hunspell dictionaries from LibreOffice repository."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Callable, Final
from urllib.request import urlopen

KNOWN_DICTS: Final[dict[str, str]] = {
    "es": "https://raw.githubusercontent.com/LibreOffice/dictionaries/master/es/es_ES.dic",
    "en": "https://raw.githubusercontent.com/LibreOffice/dictionaries/master/en/en_GB.dic",
}


class HunspellProcessor:
    """Convert Hunspell `.dic` files into plain wordlists."""

    _word_pattern = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ]+$")

    def process(self, raw_text: str) -> list[str]:
        """Parse and clean Hunspell text.

        Parameters
        ----------
        raw_text : str
            Raw content of a Hunspell `.dic` file.

        Returns
        -------
        list[str]
            Sorted unique words normalized for passphrase generation.
        """

        lines = raw_text.splitlines()
        if not lines:
            return []

        candidates = lines[1:]
        output: set[str] = set()
        for line in candidates:
            root = self.normalize_entry(line)
            if root:
                output.add(root)

        return sorted(output)

    def normalize_entry(self, entry: str) -> str:
        """Normalize a single Hunspell entry into a plain word.

        Parameters
        ----------
        entry : str
            Raw dictionary entry.

        Returns
        -------
        str
            Normalized word or empty string if filtered out.
        """

        stripped = entry.strip()
        if not stripped:
            return ""

        root = stripped.split("/", maxsplit=1)[0]
        root = root.split(" ", maxsplit=1)[0].strip().lower()
        if len(root) < 3 or len(root) > 10:
            return ""
        if not self._word_pattern.match(root):
            return ""
        return root


class HunspellDownloader:
    """Download and process known language dictionaries."""

    def __init__(self, processor: HunspellProcessor | None = None) -> None:
        self._processor = processor or HunspellProcessor()

    @staticmethod
    def supported_languages() -> tuple[str, ...]:
        """Return supported language keys for remote dictionaries.

        Returns
        -------
        tuple[str, ...]
            Available language keys.
        """

        return tuple(sorted(KNOWN_DICTS.keys()))

    def download(
        self,
        language: str,
        destination: Path,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> Path:
        """Download dictionary for a language and save processed list.

        Parameters
        ----------
        language : str
            Language key in `KNOWN_DICTS`.
        destination : Path
            Output plain-text path where one word per line will be written.
        progress_callback : Callable[[int, int], None] | None, optional
            Optional callback receiving `(downloaded_bytes, total_bytes)`.

        Returns
        -------
        Path
            Destination path.

        Raises
        ------
        ValueError
            If language is not supported.
        OSError
            If write operation fails.
        """

        if language not in KNOWN_DICTS:
            raise ValueError(f"Unsupported language: {language}")

        url = KNOWN_DICTS[language]
        raw = self._download_text(url, progress_callback)
        words = self._processor.process(raw)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("\n".join(words) + "\n", encoding="utf-8")
        return destination

    @staticmethod
    def _download_text(
        url: str,
        progress_callback: Callable[[int, int], None] | None,
    ) -> str:
        """Fetch remote text content.

        Parameters
        ----------
        url : str
            Source URL.
        progress_callback : Callable[[int, int], None] | None
            Download progress callback.

        Returns
        -------
        str
            Downloaded text decoded as UTF-8.
        """

        with urlopen(url, timeout=30) as response:
            total_header = response.headers.get("Content-Length")
            total = int(total_header) if total_header and total_header.isdigit() else 0
            buffer = bytearray()
            downloaded = 0
            while True:
                chunk = response.read(8192)
                if not chunk:
                    break
                buffer.extend(chunk)
                downloaded += len(chunk)
                if progress_callback is not None:
                    progress_callback(downloaded, total)
        return bytes(buffer).decode("utf-8", errors="ignore")
