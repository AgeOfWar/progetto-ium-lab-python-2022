from tkinter import *
from view.widgets import *

from view import word_graph_widget, dictionaries_widget

from word_graph import read_or_create_graph
from preferences import write_preferences

def setup_window(window, dictionary):
    window.title("Parole - Caricamento regole " + dictionary)
    window.geometry("600x400")
    window.minsize(600, 400)
    LoadingFrame(window, dictionary).pack(fill=BOTH, expand=True, padx=10, pady=10)

class LoadingFrame(Frame):
    def __init__(self, parent, dictionary):
        super().__init__(parent)
        detail_progress = ProgressBar(self)
        progress = ProgressBar(self, function=lambda p, stop_event: read_or_create_graph(dictionary, p, detail_progress, stop_event), on_complete=lambda graph: self.on_complete(dictionary, graph))
        progress.pack(anchor=W, fill=X, pady=5)
        detail_progress.pack(anchor=W, fill=X, pady=5)
        Label(self,"\nQuesta operazione potrebbe richiedere diversi minuti\n\nSe torni indietro il caricamento riprenderà da dove si è interrotto", justify=LEFT, wraplength=580).pack(anchor=W, pady=5)
        Button(self, "Indietro", command=self.back).pack(side=BOTTOM, anchor=E, pady=5)

    def on_complete(self, dictionary, graph):
        word_graph_widget.setup_window(clear_window(self), dictionary, graph)

    def back(self):
        window = clear_window(self)
        write_preferences(start_dictionary=None)
        dictionaries_widget.setup_window(window)

        