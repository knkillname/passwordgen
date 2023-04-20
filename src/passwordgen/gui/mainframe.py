from collections.abc import Sequence
import tkinter as tk
import tkinter.ttk as ttk


# The main frame class for the password generator
class MainFrame(ttk.Frame):
    """The main frame for the password generator GUI.

    This class is the main frame for the password generator GUI. It
    contains all the widgets and methods for the GUI.
    """

    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.password_var: tk.StringVar = tk.StringVar()
        self.password_label: ttk.Label
        self.strength_label: ttk.Label
        self.strength_bar: ttk.Progressbar
        self.generate_button: ttk.Button
        self.copy_button: ttk.Button
        self.options_frame: ttk.Frame
        self.method_label: ttk.Label
        self.method_selector: ttk.Combobox

        self._create_widgets()
        self._place_widgets()
        self._use_theme()

    def _create_widgets(self) -> None:
        """Create all the widgets for the GUI."""
        self.password_label = ttk.Label(self, textvariable=self.password_var)
        self.strength_label = ttk.Label(self, text="Password Strength")
        self.strength_bar = ttk.Progressbar(
            self, orient=tk.HORIZONTAL, length=4, mode="determinate"
        )
        self.generate_button = ttk.Button(self, text="Generate Password")
        self.copy_button = ttk.Button(self, text="Copy to Clipboard")
        self.options_frame = ttk.Frame(self)
        self.method_label = ttk.Label(self.options_frame, text="Method")
        self.method_selector = ttk.Combobox(self.options_frame, values=[])

    def _place_widgets(self):
        """Place all the widgets for the GUI."""
        # Place the password label on the first row
        self.password_label.grid(row=0, column=0, columnspan=2, sticky="ew")
        # Place the strength progress bar to the right of the password label
        self.strength_bar.grid(row=0, column=1, sticky="ew")
        # Place the strength label below the strength progress bar
        self.strength_label.grid(row=1, column=1, sticky="ew")
        # Place the method label on the next row and then the method selector
        self.method_label.grid(row=2, column=0, sticky="ew")
        self.method_selector.grid(row=2, column=1, sticky="ew")
        # Place the options frame below
        self.options_frame.grid(row=3, column=0, columnspan=2, sticky="ew")
        # Place the generate and copy buttons below
        self.generate_button.grid(row=4, column=0, sticky="ew")
        self.copy_button.grid(row=4, column=1, sticky="ew")

        # Set the weights for the rows and columns
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def _use_theme(self) -> None:
        """Use the theme for the GUI."""
        style = ttk.Style()
        style.theme_use("clam")

    def set_method_names(self, names: Sequence[str]) -> None:
        """Set the names of the password generation methods."""
        if not isinstance(names, Sequence):
            raise TypeError(f"Expected a sequence, got {type(names)}")
        for name in names:
            if not isinstance(name, str):
                raise TypeError(f"Expected a sequence of str, got {type(name)}")
        self.method_selector["values"] = list(names)
