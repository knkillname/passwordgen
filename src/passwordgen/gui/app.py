"""Main Tkinter application."""

from __future__ import annotations

import tkinter as tk
import tkinter.font as tkfont
from tkinter import messagebox, ttk

from secure_passwords.config.manager import ConfigManager
from secure_passwords.generators.alternating import AlternatingGenerator
from secure_passwords.generators.symbols import RandomSymbolsGenerator
from secure_passwords.generators.words import RandomWordsGenerator
from secure_passwords.gui.config_frames import (
    AlternatingConfigFrame,
    SymbolsConfigFrame,
    WordsConfigFrame,
)
from secure_passwords.gui.results_frame import ResultsFrame
from secure_passwords.gui.settings_dialog import SettingsDialog
from secure_passwords.i18n import _
from secure_passwords.strength import PasswordStrengthEvaluator
from secure_passwords.wordlists import WordlistLoader


class App(tk.Tk):
    """Main GUI application for password generation."""

    def __init__(self) -> None:
        super().__init__()
        self.title(_("Secure Password Generator"))
        self.geometry("900x600")

        self._config_manager = ConfigManager()
        self._app_config = self._config_manager.load()

        self._style = ttk.Style(self)
        self._apply_theme(self._app_config.theme)

        self._loader = WordlistLoader()
        self._generators = {
            "symbols": RandomSymbolsGenerator(),
            "words": RandomWordsGenerator(self._loader, self._app_config.wordlists),
            "alternating": AlternatingGenerator(
                self._loader, self._app_config.wordlists
            ),
        }

        self._evaluator = PasswordStrengthEvaluator()

        top_bar = ttk.Frame(self, padding=12)
        top_bar.pack(fill="x")

        self.batch_var = tk.IntVar(value=self._app_config.batch_size)

        ttk.Label(top_bar, text=_("Count")).pack(side="left")
        ttk.Spinbox(top_bar, from_=1, to=30, textvariable=self.batch_var, width=6).pack(
            side="left", padx=(8, 12)
        )

        ttk.Button(top_bar, text=_("Generate"), command=self._generate).pack(
            side="left"
        )
        ttk.Button(top_bar, text=_("Settings"), command=self._open_settings).pack(
            side="left", padx=(8, 0)
        )

        content = ttk.Panedwindow(self, orient="vertical")
        content.pack(fill="both", expand=True)

        generator_panel = ttk.Frame(content, padding=8)
        result_panel = ttk.Frame(content, padding=8)
        content.add(generator_panel, weight=2)
        content.add(result_panel, weight=3)

        self.notebook = ttk.Notebook(generator_panel)
        self.notebook.pack(fill="both", expand=True)

        self._frames = {
            "symbols": SymbolsConfigFrame(self.notebook, self._app_config),
            "words": WordsConfigFrame(self.notebook, self._app_config),
            "alternating": AlternatingConfigFrame(self.notebook, self._app_config),
        }

        self.notebook.add(self._frames["symbols"], text=_("Symbols"))
        self.notebook.add(self._frames["words"], text=_("Words"))
        self.notebook.add(self._frames["alternating"], text=_("Alternating"))

        self.results = ResultsFrame(
            result_panel,
            self._evaluator,
            attempts_per_second=self._app_config.crack_attempts_per_second,
        )
        self.results.pack(fill="both", expand=True)

    def _apply_theme(self, theme: str) -> None:
        """Apply ttk theme if available.

        Parameters
        ----------
        theme : str
            Theme identifier.
        """

        available = self._style.theme_names()
        chosen = theme if theme in available else "clam"
        self._style.theme_use(chosen)
        default_font = tkfont.nametofont("TkDefaultFont")
        line_height = int(default_font.metrics("linespace"))
        # Avoid clipped glyphs in Treeview rows across themes/DPIs.
        self._style.configure("Treeview", rowheight=max(22, line_height + 8))

    def _open_settings(self) -> None:
        """Open modal settings dialog."""

        SettingsDialog(
            self,
            config_manager=self._config_manager,
            app_config=self._app_config,
            on_saved=self._reload_config,
        )

    def _reload_config(self) -> None:
        """Reload configuration from JSON and refresh UI defaults."""

        self._app_config = self._config_manager.load()
        self._apply_theme(self._app_config.theme)

        self._loader.clear_cache()
        words_generator = self._generators["words"]
        alternating_generator = self._generators["alternating"]
        assert isinstance(words_generator, RandomWordsGenerator)
        assert isinstance(alternating_generator, AlternatingGenerator)
        words_generator.set_wordlists_config(self._app_config.wordlists)
        alternating_generator.set_wordlists_config(self._app_config.wordlists)

        self._frames["symbols"].apply_defaults(self._app_config)
        self._frames["words"].apply_defaults(self._app_config)
        self._frames["alternating"].apply_defaults(self._app_config)
        self.batch_var.set(self._app_config.batch_size)
        self.results.set_attempts_per_second(self._app_config.crack_attempts_per_second)

    def _generate(self) -> None:
        """Generate passwords using the selected algorithm tab."""

        count = max(1, self.batch_var.get())

        try:
            tab_id = self.notebook.select()  # type: ignore[no-untyped-call]
            current_tab = self.nametowidget(tab_id)

            passwords: list[str] = []
            if current_tab is self._frames["symbols"]:
                cfg = self._frames["symbols"].get_config()
                symbols_generator = self._generators["symbols"]
                assert isinstance(symbols_generator, RandomSymbolsGenerator)
                passwords = [symbols_generator.generate(cfg) for _ in range(count)]
            elif current_tab is self._frames["words"]:
                cfg = self._frames["words"].get_config()
                words_generator = self._generators["words"]
                assert isinstance(words_generator, RandomWordsGenerator)
                passwords = [words_generator.generate(cfg) for _ in range(count)]
            elif current_tab is self._frames["alternating"]:
                cfg = self._frames["alternating"].get_config()
                alternating_generator = self._generators["alternating"]
                assert isinstance(alternating_generator, AlternatingGenerator)
                passwords = [alternating_generator.generate(cfg) for _ in range(count)]

            self.results.set_passwords(passwords)
        except (OSError, TypeError, ValueError) as exc:
            messagebox.showerror(_("Error"), str(exc), parent=self)


def run_app() -> None:
    """Run GUI application main loop."""

    app = App()
    app.mainloop()
