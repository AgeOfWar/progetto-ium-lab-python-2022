from tkinter import *
from tkinter import ttk

class Window(Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title)

class Label(ttk.Label):
    def __init__(self, parent, text):
        super().__init__(parent, text=text, font=('Montserrat', 10))

class ScrollbarFrame(ttk.Frame):
    def __init__(self, parent, widget_init):
        super().__init__(parent)
        widget = widget_init(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=widget.yview)
        widget.configure(yscrollcommand=self.set_scrollbar)
        widget.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=LEFT, fill=Y)
        self.scrollbar = scrollbar
        self.widget = widget

    def set_scrollbar(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.scrollbar.pack_forget()
        else:
            self.scrollbar.pack(side=LEFT, fill=Y)
        self.scrollbar.set(lo, hi)

def clear_window(widget):
    window = widget.winfo_toplevel()
    for child in window.winfo_children():
        child.destroy()
    return window
