from tkinter import *
from view.widgets import *

def setup_window(window, dictionary):
    window.title("Parole - Caricamento " + dictionary)
    window.geometry("540x360")
    window.minsize(420, 180)
    LoadingFrame(window).pack(fill=BOTH, expand=True, padx=10, pady=10)

class LoadingFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        Label(self, "ciao").pack()