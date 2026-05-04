"""Modal settings dialog for editing defaults and dictionary sources."""

from __future__ import annotations

import threading
import tkinter as tk
from functools import partial
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Callable, cast

from passwordgen.config.manager import ConfigManager
from passwordgen.config.schema import (
    AlternatingDefaults,
    AppConfig,
    SymbolsDefaults,
    WordlistsConfig,
    WordsDefaults,
)
from passwordgen.i18n import _
from passwordgen.wordlists.downloader import KNOWN_DICTS, HunspellDownloader


class SettingsDialog(tk.Toplevel):
    """Dialog for persistent configuration editing."""

    def __init__(
        self,
        parent: tk.Misc,
        config_manager: ConfigManager,
        app_config: AppConfig,
        on_saved: Callable[[], None],
    ) -> None:
        super().__init__(parent)
        self.title(_("Settings"))
        self.resizable(False, False)
        self.transient(cast(tk.Wm, parent))
        self.grab_set()

        self._config_manager = config_manager
        self._downloader = HunspellDownloader()
        self._on_saved = on_saved

        self.length_var = tk.IntVar(value=app_config.symbols.length)
        self.upper_var = tk.BooleanVar(value=app_config.symbols.use_upper)
        self.digits_var = tk.BooleanVar(value=app_config.symbols.use_digits)
        self.punct_var = tk.BooleanVar(value=app_config.symbols.use_punctuation)
        self.charset_var = tk.StringVar(value=app_config.symbols.custom_charset)

        self.words_count_var = tk.IntVar(value=app_config.words.word_count)
        self.words_separator_var = tk.StringVar(value=app_config.words.separator)
        self.words_language_var = tk.StringVar(value=app_config.words.language)

        self.alt_count_var = tk.IntVar(value=app_config.alternating.word_count)
        self.alt_group_var = tk.IntVar(value=app_config.alternating.symbols_per_group)
        self.alt_language_var = tk.StringVar(value=app_config.alternating.language)
        self.alt_digits_var = tk.BooleanVar(value=app_config.alternating.use_digits)

        self.theme_var = tk.StringVar(value=app_config.theme)
        self.batch_var = tk.IntVar(value=app_config.batch_size)
        self.crack_speed_var = tk.IntVar(value=app_config.crack_attempts_per_second)

        self.wordlist_paths: dict[str, str] = dict(app_config.wordlists.paths)

        notebook = ttk.Notebook(self)
        notebook.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")

        notebook.add(self._build_symbols_tab(notebook), text=_("Symbols"))
        notebook.add(self._build_words_tab(notebook), text=_("Words"))
        notebook.add(self._build_alternating_tab(notebook), text=_("Alternating"))
        notebook.add(self._build_wordlists_tab(notebook), text=_("Dictionaries"))
        notebook.add(self._build_general_tab(notebook), text=_("General"))

        action_frame = ttk.Frame(self)
        action_frame.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 12))
        action_frame.columnconfigure(0, weight=1)

        ttk.Button(action_frame, text=_("Save"), command=self._save).grid(
            row=0, column=1, padx=(8, 0)
        )
        ttk.Button(action_frame, text=_("Cancel"), command=self.destroy).grid(
            row=0, column=2
        )

    def _build_symbols_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent, padding=10)
        ttk.Label(frame, text=_("Length")).grid(row=0, column=0, sticky="w")
        ttk.Spinbox(
            frame, from_=4, to=128, textvariable=self.length_var, width=10
        ).grid(row=0, column=1, sticky="w")
        ttk.Checkbutton(frame, text=_("Uppercase"), variable=self.upper_var).grid(
            row=1, column=0, sticky="w", pady=(8, 0)
        )
        ttk.Checkbutton(frame, text=_("Digits"), variable=self.digits_var).grid(
            row=1, column=1, sticky="w", pady=(8, 0)
        )
        ttk.Checkbutton(frame, text=_("Punctuation"), variable=self.punct_var).grid(
            row=1, column=2, sticky="w", pady=(8, 0)
        )
        ttk.Label(frame, text=_("Custom charset")).grid(
            row=2, column=0, sticky="w", pady=(8, 0)
        )
        ttk.Entry(frame, textvariable=self.charset_var, width=42).grid(
            row=3, column=0, columnspan=3, sticky="ew"
        )
        return frame

    def _build_words_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent, padding=10)
        ttk.Label(frame, text=_("Word count")).grid(row=0, column=0, sticky="w")
        ttk.Spinbox(
            frame, from_=2, to=16, textvariable=self.words_count_var, width=10
        ).grid(row=0, column=1, sticky="w")
        ttk.Label(frame, text=_("Separator")).grid(
            row=1, column=0, sticky="w", pady=(8, 0)
        )
        ttk.Entry(frame, textvariable=self.words_separator_var, width=10).grid(
            row=1, column=1, sticky="w", pady=(8, 0)
        )
        ttk.Label(frame, text=_("Dictionary")).grid(
            row=2, column=0, sticky="w", pady=(8, 0)
        )
        ttk.Combobox(
            frame,
            textvariable=self.words_language_var,
            values=["en", "es"],
            state="readonly",
            width=8,
        ).grid(row=2, column=1, sticky="w", pady=(8, 0))
        return frame

    def _build_alternating_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent, padding=10)
        ttk.Label(frame, text=_("Word count")).grid(row=0, column=0, sticky="w")
        ttk.Spinbox(
            frame, from_=2, to=16, textvariable=self.alt_count_var, width=10
        ).grid(row=0, column=1, sticky="w")
        ttk.Label(frame, text=_("Symbols per group")).grid(
            row=1, column=0, sticky="w", pady=(8, 0)
        )
        ttk.Spinbox(
            frame, from_=1, to=12, textvariable=self.alt_group_var, width=10
        ).grid(row=1, column=1, sticky="w", pady=(8, 0))
        ttk.Label(frame, text=_("Dictionary")).grid(
            row=2, column=0, sticky="w", pady=(8, 0)
        )
        ttk.Combobox(
            frame,
            textvariable=self.alt_language_var,
            values=["en", "es"],
            state="readonly",
            width=8,
        ).grid(row=2, column=1, sticky="w", pady=(8, 0))
        ttk.Checkbutton(
            frame, text=_("Include digits"), variable=self.alt_digits_var
        ).grid(row=3, column=0, sticky="w", pady=(8, 0), columnspan=2)
        return frame

    def _build_wordlists_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent, padding=10)
        self._wordlist_status: dict[str, tk.StringVar] = {}

        for row, language in enumerate(sorted(KNOWN_DICTS.keys())):
            ttk.Label(frame, text=f"{language.upper()}").grid(
                row=row, column=0, sticky="w"
            )
            status_var = tk.StringVar(
                value=self.wordlist_paths.get(language, _("embedded"))
            )
            self._wordlist_status[language] = status_var
            ttk.Label(frame, textvariable=status_var, width=46).grid(
                row=row, column=1, sticky="w"
            )
            ttk.Button(
                frame,
                text=_("Download"),
                command=partial(self._download_dictionary, language),
            ).grid(row=row, column=2, padx=(8, 0))
            ttk.Button(
                frame,
                text=_("Browse"),
                command=partial(self._pick_file, language),
            ).grid(row=row, column=3, padx=(8, 0))
            ttk.Button(
                frame,
                text=_("Reset"),
                command=partial(self._reset_language, language),
            ).grid(row=row, column=4, padx=(8, 0))

        self.download_progress = ttk.Progressbar(frame, mode="indeterminate")
        self.download_progress.grid(
            row=len(KNOWN_DICTS), column=0, columnspan=5, sticky="ew", pady=(10, 0)
        )

        return frame

    def _build_general_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent, padding=10)
        ttk.Label(frame, text=_("ttk theme")).grid(row=0, column=0, sticky="w")
        ttk.Combobox(
            frame,
            textvariable=self.theme_var,
            values=["clam", "alt", "default", "classic"],
            state="readonly",
            width=12,
        ).grid(row=0, column=1, sticky="w")

        ttk.Label(frame, text=_("Batch size")).grid(
            row=1, column=0, sticky="w", pady=(8, 0)
        )
        ttk.Spinbox(frame, from_=1, to=30, textvariable=self.batch_var, width=10).grid(
            row=1, column=1, sticky="w", pady=(8, 0)
        )
        ttk.Label(frame, text=_("Attempts/s for crack time")).grid(
            row=2, column=0, sticky="w", pady=(8, 0)
        )
        ttk.Spinbox(
            frame,
            from_=1,
            to=10_000_000_000,
            textvariable=self.crack_speed_var,
            width=14,
        ).grid(row=2, column=1, sticky="w", pady=(8, 0))
        return frame

    def _pick_file(self, language: str) -> None:
        chosen = filedialog.askopenfilename(
            title=_("Select wordlist for {language}").format(language=language),
            filetypes=[(_("Text"), "*.txt"), (_("All"), "*.*")],
            parent=self,
        )
        if not chosen:
            return
        self.wordlist_paths[language] = chosen
        self._wordlist_status[language].set(chosen)

    def _reset_language(self, language: str) -> None:
        self.wordlist_paths.pop(language, None)
        self._wordlist_status[language].set(_("embedded"))

    def _download_dictionary(self, language: str) -> None:
        target = Path.home() / ".local" / "share" / "passwordgen" / f"{language}.txt"

        self.download_progress.start(8)

        def worker() -> None:
            try:
                saved = self._downloader.download(language=language, destination=target)
            except (OSError, ValueError) as exc:
                self.after(0, lambda: self._on_download_error(str(exc)))
                return
            self.after(0, lambda: self._on_download_success(language, saved))

        threading.Thread(target=worker, daemon=True).start()

    def _on_download_success(self, language: str, path: Path) -> None:
        self.download_progress.stop()
        self.wordlist_paths[language] = str(path)
        self._wordlist_status[language].set(str(path))
        messagebox.showinfo(
            _("Dictionary"),
            _("Downloaded and processed: {path}").format(path=path),
            parent=self,
        )

    def _on_download_error(self, message: str) -> None:
        self.download_progress.stop()
        messagebox.showerror(_("Dictionary"), message, parent=self)

    def _save(self) -> None:
        words_separator = self.words_separator_var.get() or "-"
        config = AppConfig(
            symbols=SymbolsDefaults(
                length=max(4, self.length_var.get()),
                use_upper=self.upper_var.get(),
                use_digits=self.digits_var.get(),
                use_punctuation=self.punct_var.get(),
                custom_charset=self.charset_var.get().strip(),
            ),
            words=WordsDefaults(
                word_count=max(2, self.words_count_var.get()),
                separator=words_separator,
                language=self.words_language_var.get() or "en",
            ),
            alternating=AlternatingDefaults(
                word_count=max(2, self.alt_count_var.get()),
                symbols_per_group=max(1, self.alt_group_var.get()),
                language=self.alt_language_var.get() or "en",
                use_digits=self.alt_digits_var.get(),
            ),
            wordlists=WordlistsConfig(paths=dict(self.wordlist_paths)),
            theme=self.theme_var.get() or "clam",
            batch_size=max(1, self.batch_var.get()),
            crack_attempts_per_second=max(1, self.crack_speed_var.get()),
        )
        self._config_manager.save(config)
        self._on_saved()
        self.destroy()
