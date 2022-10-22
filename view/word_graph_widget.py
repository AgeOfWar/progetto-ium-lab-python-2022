from tkinter import *
from view.widgets import *

def setup_window(window, dictionary, graph):
    window.title("Parole - " + dictionary)
    window.geometry("540x360")
    window.minsize(420, 300)
    WordGraphFrame(window, dictionary, graph).pack(fill=BOTH, expand=True, padx=10, pady=10)

class WordGraphFrame(ttk.Frame):
    def __init__(self, parent, dictionary, graph):
        super().__init__(parent, padding=10)
        Label(self, str(graph)).pack()