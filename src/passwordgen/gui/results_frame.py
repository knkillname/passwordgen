"""Results panel showing generated passwords and strength information."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from secure_passwords.i18n import _
from secure_passwords.strength import PasswordStrengthEvaluator


def _format_crack_time(seconds: float) -> str:
    """Return a human-readable crack-time string.

    Parameters
    ----------
    seconds : float
        Estimated brute-force time in seconds.

    Returns
    -------
    str
        Compact human-readable duration.
    """

    if seconds == float("inf"):
        return _("centuries")

    total_seconds = max(1, int(seconds))
    minute = 60
    hour = 60 * minute
    day = 24 * hour
    week = 7 * day
    month = int((365 / 12) * day)
    year = 365 * day
    century = 100 * year

    def _unit(
        value: int,
        singular_template: str,
        plural_template: str,
    ) -> str:
        template = singular_template if value == 1 else plural_template
        return _(template).format(value=value)

    units = [
        (century, "{value} century", "{value} centuries"),
        (year, "{value} year", "{value} years"),
        (month, "{value} month", "{value} months"),
        (week, "{value} week", "{value} weeks"),
        (day, "{value} day", "{value} days"),
        (hour, "{value} hour", "{value} hours"),
        (minute, "{value} minute", "{value} minutes"),
    ]
    for threshold, singular_template, plural_template in units:
        if total_seconds >= threshold:
            value = total_seconds // threshold
            if threshold == century and value > 1:
                return _("centuries")
            return _unit(value, singular_template, plural_template)
    return _unit(total_seconds, "{value} second", "{value} seconds")


class ResultsFrame(ttk.Frame):
    """Display generated passwords, selected strength and clipboard actions."""

    def __init__(
        self,
        master: tk.Misc,
        evaluator: PasswordStrengthEvaluator,
        attempts_per_second: int = 1000,
    ) -> None:
        super().__init__(master, padding=12)
        self._evaluator = evaluator
        self._passwords: list[str] = []
        self._attempts_per_second = attempts_per_second

        scroll = ttk.Scrollbar(self, orient="vertical")
        self.listbox = tk.Listbox(
            self,
            yscrollcommand=scroll.set,
            height=8,
            activestyle="dotbox",
            selectmode="single",
            font=("TkDefaultFont", 10),
        )
        scroll.configure(command=self.listbox.yview)
        self.listbox.grid(row=0, column=0, columnspan=3, sticky="nsew")
        scroll.grid(row=0, column=3, sticky="ns")
        self.listbox.bind("<<ListboxSelect>>", self._on_selection_change)

        self.strength_var = tk.StringVar(value=_("Strength: -"))
        self.strength_label = ttk.Label(self, textvariable=self.strength_var)
        self.strength_label.grid(row=1, column=0, sticky="w", pady=(8, 0))

        self.progress = ttk.Progressbar(
            self, orient="horizontal", mode="determinate", maximum=100
        )
        self.progress.grid(row=1, column=1, sticky="ew", padx=(8, 8), pady=(8, 0))

        self.copy_button = ttk.Button(
            self, text=_("Copy selected"), command=self.copy_selected
        )
        self.copy_button.grid(row=1, column=2, sticky="e", pady=(8, 0))

        self.status_var = tk.StringVar(value="")
        ttk.Label(
            self, textvariable=self.status_var, foreground="gray", anchor="w"
        ).grid(row=2, column=0, columnspan=4, sticky="ew", pady=(4, 0))

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def set_attempts_per_second(self, attempts: int) -> None:
        """Update attacker speed used for crack-time labels.

        Parameters
        ----------
        attempts : int
            Guesses per second.
        """

        self._attempts_per_second = max(1, attempts)

    def set_passwords(self, passwords: list[str]) -> None:
        """Replace displayed passwords.

        Parameters
        ----------
        passwords : list[str]
            New generated passwords.
        """

        self._passwords = list(passwords)
        self.listbox.delete(0, "end")
        for password in self._passwords:
            self.listbox.insert("end", password)
        if self._passwords:
            self.listbox.selection_set(0)
            self.listbox.activate(0)
            self._update_strength(self._passwords[0])
        else:
            self.strength_var.set(_("Strength: -"))
            self.status_var.set("")
            self.progress["value"] = 0

    def copy_selected(self) -> None:
        """Copy selected password to clipboard."""

        selected = self._selected_password()
        if not selected:
            return
        root = self.winfo_toplevel()
        root.clipboard_clear()
        root.clipboard_append(selected)

    def _selected_password(self) -> str:
        """Return current selected password.

        Returns
        -------
        str
            Selected password or empty string.
        """

        indices: tuple[int, ...] = self.listbox.curselection()  # type: ignore[no-untyped-call]
        if not indices:
            return ""
        idx = int(indices[0])
        if idx >= len(self._passwords):
            return ""
        return self._passwords[idx]

    def _on_selection_change(self, _event: tk.Event[tk.Misc]) -> None:
        """Recompute strength when listbox selection changes.

        Parameters
        ----------
        _event : tk.Event[tk.Misc]
            Tkinter event object.
        """

        selected = self._selected_password()
        if selected:
            self._update_strength(selected)

    def _update_strength(self, password: str) -> None:
        """Update strength widgets.

        Parameters
        ----------
        password : str
            Password to evaluate.
        """

        result = self._evaluator.evaluate(password)
        self.progress["value"] = result.score
        level_text = _(result.level.name.replace("_", " ").title())
        self.strength_var.set(
            _("Strength: {level} ({score}/100)").format(
                level=level_text,
                score=result.score,
            )
        )
        crack = _format_crack_time(result.crack_seconds(self._attempts_per_second))
        self.status_var.set(
            _(
                "{bits:.1f} bits  ·  crack time ({attempts:,} attempts/s): {crack}"
            ).format(
                bits=result.entropy_bits,
                attempts=self._attempts_per_second,
                crack=crack,
            )
        )
