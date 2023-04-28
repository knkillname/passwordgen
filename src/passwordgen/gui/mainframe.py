"""The main frame for the password generator GUI."""
import tkinter as tk
from tkinter import ttk


class MainFrame(ttk.Frame):  # pylint: disable=too-many-ancestors
    """The main frame for the password generator GUI.

    This class is the main frame for the password generator GUI. It
    contains all the widgets and methods for the GUI.
    """

    def __init__(self, master: tk.Misc, **kwargs) -> None:
        """Initialize the main frame."""
        super().__init__(master=master, **kwargs)
        self.password_var: tk.StringVar = tk.StringVar()
        self.strength_var: tk.IntVar = tk.IntVar()
        self.method_var: tk.StringVar = tk.StringVar()

        self.password_entry: ttk.Entry
        self.strength_label: ttk.Label
        self.strength_progressbar: ttk.Progressbar
        self.method_label: ttk.Label
        self.method_combobox: ttk.Combobox
        self.options_button: ttk.Button
        self.generate_button: ttk.Button
        self.copy_button: ttk.Button

        self._create_widgets()
        self._place_widgets()
        self._set_theme()

    def _create_widgets(self) -> None:
        """Create the widgets for the main frame."""
        self.password_entry = ttk.Entry(
            self, state="readonly", textvariable=self.password_var
        )
        self.strength_label = ttk.Label(self, text="Strength:")
        self.strength_progressbar = ttk.Progressbar(self, variable=self.strength_var)
        self.method_label = ttk.Label(self, text="Method:")
        self.method_combobox = ttk.Combobox(
            self, textvariable=self.method_var, state="readonly"
        )
        self.options_button = ttk.Button(self, text="Options")
        self.generate_button = ttk.Button(self, text="Generate")
        self.copy_button = ttk.Button(self, text="Copy")

    def _place_widgets(self):
        """Place the widgets in the main frame."""
        # Set the column and row weights and padding.
        for j in range(3):
            self.columnconfigure(j, weight=1, pad=8)
        for i in range(4):
            self.rowconfigure(i, weight=1, pad=8)

        # Place the widgets.
        self.password_entry.grid(row=0, column=0, columnspan=3, sticky=tk.EW)
        self.strength_label.grid(row=1, column=0, sticky=tk.W)
        self.strength_progressbar.grid(row=1, column=1, columnspan=2, sticky=tk.EW)
        self.method_label.grid(row=2, column=0, sticky=tk.W)
        self.method_combobox.grid(row=2, column=1, columnspan=2, sticky=tk.EW)
        self.options_button.grid(row=3, column=0, sticky=tk.EW)
        self.generate_button.grid(row=3, column=1, sticky=tk.EW, padx=(8, 0))
        self.copy_button.grid(row=3, column=2, sticky=tk.EW, padx=(8, 0))
        self.grid(sticky=tk.NSEW)

    def _set_theme(self) -> None:
        # Set the clam ttk theme.
        style = ttk.Style(self)
        style.theme_use("clam")
