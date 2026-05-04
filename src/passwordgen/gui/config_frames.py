"""Configuration frames for each password generator algorithm."""

from __future__ import annotations

import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import ttk

from secure_passwords.config.schema import AppConfig
from secure_passwords.generators.alternating import AlternatingConfig
from secure_passwords.generators.symbols import SymbolsConfig
from secure_passwords.generators.words import WordsConfig
from secure_passwords.i18n import _
from secure_passwords.wordlists import available_dictionary_keys


class BaseConfigFrame(ttk.Frame, ABC):
    """Common contract for algorithm configuration views."""

    @abstractmethod
    def get_config(self) -> object:
        """Return algorithm-specific configuration object."""

    @abstractmethod
    def apply_defaults(self, app_config: AppConfig) -> None:
        """Refresh inputs from current application defaults."""


class SymbolsConfigFrame(BaseConfigFrame):
    """Input controls for symbol-based generation."""

    def __init__(self, master: tk.Misc, app_config: AppConfig) -> None:
        super().__init__(master, padding=12)

        self.length_var = tk.IntVar(value=app_config.symbols.length)
        self.use_upper_var = tk.BooleanVar(value=app_config.symbols.use_upper)
        self.use_digits_var = tk.BooleanVar(value=app_config.symbols.use_digits)
        self.use_punctuation_var = tk.BooleanVar(
            value=app_config.symbols.use_punctuation
        )
        self.custom_charset_var = tk.StringVar(value=app_config.symbols.custom_charset)

        ttk.Label(self, text=_("Length")).grid(row=0, column=0, sticky="w")
        ttk.Spinbox(self, from_=4, to=128, textvariable=self.length_var, width=8).grid(
            row=0, column=1, sticky="w"
        )

        ttk.Checkbutton(self, text=_("Uppercase"), variable=self.use_upper_var).grid(
            row=1, column=0, sticky="w"
        )
        ttk.Checkbutton(self, text=_("Digits"), variable=self.use_digits_var).grid(
            row=1, column=1, sticky="w"
        )
        ttk.Checkbutton(
            self, text=_("Punctuation"), variable=self.use_punctuation_var
        ).grid(row=1, column=2, sticky="w")

        ttk.Label(self, text=_("Custom charset (optional)")).grid(
            row=2, column=0, sticky="w", columnspan=2, pady=(8, 0)
        )
        ttk.Entry(self, textvariable=self.custom_charset_var, width=36).grid(
            row=3, column=0, columnspan=3, sticky="ew"
        )
        self.columnconfigure(2, weight=1)

    def get_config(self) -> SymbolsConfig:
        """Build `SymbolsConfig` from current controls.

        Returns
        -------
        SymbolsConfig
            Runtime generation settings.
        """

        return SymbolsConfig(
            length=max(4, self.length_var.get()),
            use_upper=self.use_upper_var.get(),
            use_digits=self.use_digits_var.get(),
            use_punctuation=self.use_punctuation_var.get(),
            custom_charset=self.custom_charset_var.get().strip(),
        )

    def apply_defaults(self, app_config: AppConfig) -> None:
        """Load frame values from app defaults.

        Parameters
        ----------
        app_config : AppConfig
            Source defaults.
        """

        self.length_var.set(app_config.symbols.length)
        self.use_upper_var.set(app_config.symbols.use_upper)
        self.use_digits_var.set(app_config.symbols.use_digits)
        self.use_punctuation_var.set(app_config.symbols.use_punctuation)
        self.custom_charset_var.set(app_config.symbols.custom_charset)


class WordsConfigFrame(BaseConfigFrame):
    """Input controls for random-word generation."""

    def __init__(self, master: tk.Misc, app_config: AppConfig) -> None:
        super().__init__(master, padding=12)

        self.count_var = tk.IntVar(value=app_config.words.word_count)
        self.separator_var = tk.StringVar(value=app_config.words.separator)
        self.language_var = tk.StringVar(value=app_config.words.language)

        ttk.Label(self, text=_("Word count")).grid(row=0, column=0, sticky="w")
        ttk.Spinbox(self, from_=2, to=16, textvariable=self.count_var, width=8).grid(
            row=0, column=1, sticky="w"
        )

        ttk.Label(self, text=_("Separator")).grid(
            row=1, column=0, sticky="w", pady=(8, 0)
        )
        ttk.Entry(self, textvariable=self.separator_var, width=8).grid(
            row=1, column=1, sticky="w", pady=(8, 0)
        )

        ttk.Label(self, text=_("Dictionary")).grid(
            row=2, column=0, sticky="w", pady=(8, 0)
        )
        self.dictionary_combo = ttk.Combobox(
            self,
            values=available_dictionary_keys(app_config.wordlists),
            state="readonly",
            textvariable=self.language_var,
            width=8,
        )
        self.dictionary_combo.grid(row=2, column=1, sticky="w", pady=(8, 0))

    def get_config(self) -> WordsConfig:
        """Build `WordsConfig` from current controls.

        Returns
        -------
        WordsConfig
            Runtime generation settings.
        """

        separator = self.separator_var.get()
        return WordsConfig(
            word_count=max(2, self.count_var.get()),
            separator=separator if separator else "-",
            language=self.language_var.get() or "en",
        )

    def apply_defaults(self, app_config: AppConfig) -> None:
        """Load frame values from app defaults.

        Parameters
        ----------
        app_config : AppConfig
            Source defaults.
        """

        self.count_var.set(app_config.words.word_count)
        self.separator_var.set(app_config.words.separator)
        values = available_dictionary_keys(app_config.wordlists)
        self.dictionary_combo.configure(values=values)
        self.language_var.set(app_config.words.language)
        if self.language_var.get() not in values:
            self.language_var.set(values[0])


class AlternatingConfigFrame(BaseConfigFrame):
    """Input controls for alternating words+symbols generation."""

    def __init__(self, master: tk.Misc, app_config: AppConfig) -> None:
        super().__init__(master, padding=12)

        self.count_var = tk.IntVar(value=app_config.alternating.word_count)
        self.group_var = tk.IntVar(value=app_config.alternating.symbols_per_group)
        self.language_var = tk.StringVar(value=app_config.alternating.language)
        self.use_digits_var = tk.BooleanVar(value=app_config.alternating.use_digits)

        ttk.Label(self, text=_("Word count")).grid(row=0, column=0, sticky="w")
        ttk.Spinbox(self, from_=2, to=16, textvariable=self.count_var, width=8).grid(
            row=0, column=1, sticky="w"
        )

        ttk.Label(self, text=_("Symbols per group")).grid(
            row=1, column=0, sticky="w", pady=(8, 0)
        )
        ttk.Spinbox(self, from_=1, to=12, textvariable=self.group_var, width=8).grid(
            row=1, column=1, sticky="w", pady=(8, 0)
        )

        ttk.Label(self, text=_("Dictionary")).grid(
            row=2, column=0, sticky="w", pady=(8, 0)
        )
        self.dictionary_combo = ttk.Combobox(
            self,
            values=available_dictionary_keys(app_config.wordlists),
            state="readonly",
            textvariable=self.language_var,
            width=8,
        )
        self.dictionary_combo.grid(row=2, column=1, sticky="w", pady=(8, 0))

        ttk.Checkbutton(
            self, text=_("Include digits"), variable=self.use_digits_var
        ).grid(row=3, column=0, sticky="w", pady=(8, 0), columnspan=2)

    def get_config(self) -> AlternatingConfig:
        """Build `AlternatingConfig` from current controls.

        Returns
        -------
        AlternatingConfig
            Runtime generation settings.
        """

        return AlternatingConfig(
            word_count=max(2, self.count_var.get()),
            symbols_per_group=max(1, self.group_var.get()),
            language=self.language_var.get() or "en",
            use_digits=self.use_digits_var.get(),
        )

    def apply_defaults(self, app_config: AppConfig) -> None:
        """Load frame values from app defaults.

        Parameters
        ----------
        app_config : AppConfig
            Source defaults.
        """

        self.count_var.set(app_config.alternating.word_count)
        self.group_var.set(app_config.alternating.symbols_per_group)
        values = available_dictionary_keys(app_config.wordlists)
        self.dictionary_combo.configure(values=values)
        self.language_var.set(app_config.alternating.language)
        if self.language_var.get() not in values:
            self.language_var.set(values[0])
        self.use_digits_var.set(app_config.alternating.use_digits)
