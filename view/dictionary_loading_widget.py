from tkinter import *
from view.widgets import *

from threading import Thread

from word_graph import read_or_create_graph

def setup_window(window, dictionary):
    window.title("Parole - Caricamento regole '" + dictionary + "'")
    window.geometry("540x360")
    window.minsize(420, 180)
    LoadingFrame(window, dictionary).pack(fill=BOTH, expand=True, padx=10, pady=10)

class LoadingFrame(ttk.Frame):
    def __init__(self, parent, dictionary):
        super().__init__(parent, padding=10)
        detail_progress = ProgressBar(self)
        progress = ProgressBar(self, function=lambda p, stop_event: read_or_create_graph(dictionary, p, detail_progress, stop_event), on_complete=self.on_complete)
        progress.pack(anchor=W, fill=X, pady=5)
        detail_progress.pack(anchor=W, fill=X, pady=5)

    def on_complete(self, graph):
        print(graph)
        