"""GUI interface for the password generator."""
import tkinter as tk
from .mainframe import MainFrame


def main():
    """Run the GUI interface."""
    root = tk.Tk()
    root.title("Password Generator")
    root.resizable(False, False)
    main_frame = MainFrame(root)
    main_frame.grid(sticky=tk.NSEW, padx=8, pady=8)
    root.columnconfigure(0, weight=1, pad=8)
    root.rowconfigure(0, weight=1, pad=8)
    root.mainloop()
