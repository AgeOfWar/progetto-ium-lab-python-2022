from tkinter import *
from tkinter import ttk
import threading

class Window(Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title)
        self.threads = []
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        for thread in self.threads:
            if thread.is_alive():
                thread.stop()
        self.destroy()

    class Thread(threading.Thread):
        def __init__(self, window, target):
            super().__init__(target=target, daemon=True)
            window.threads.append(self)
            self.window = window

        def run(self):
            self.stop_event = threading.Event()
            self._target(self.stop_event)
            self.window.threads.remove(self)

        def stop(self):
            self.stop_event.set()


class Label(ttk.Label):
    def __init__(self, parent, text, font_size=10):
        super().__init__(parent, text=text, font=("Montserrat", font_size))

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

class ProgressBar(ttk.Frame):
    def __init__(self, parent, function=None, on_complete=None, description=""):
        super().__init__(parent)
        progress = ttk.Progressbar(self, maximum=1)
        description_label = Label(self, description, font_size=8)
        progress.pack(anchor=W, fill=X, pady=5)
        description_label.pack(anchor=W)
        self.progress = progress
        self.description = description_label
        self.new_maximum = 1
        self.new_description = description
        self.new_progress = 0
        self.result_wrapper = []
        self.on_complete = on_complete
        self.update()
        if function != None:
            Window.Thread(self.winfo_toplevel(), target=lambda stop_event: self.result_wrapper.append(function(self, stop_event))).start()
    
    def request_set_description(self, new_description):
        self.new_description = new_description

    def request_set_maximum(self, maximum):
        self.new_maximum = maximum

    def request_progress(self):
        self.new_progress += 1

    def request_reset(self):
        self.new_progress = 0

    def update(self):
        if len(self.result_wrapper) == 0:
            self.description.config(text=self.new_description + "(" + str(self.new_progress) + "/" + str(self.new_maximum) + ")")
            self.progress.config(maximum=self.new_maximum)
            self.progress["value"] = self.new_progress
            self.after(100, self.update)
        else:
            self.on_complete(self.result_wrapper[0])

    def finish(self):
        self.result_wrapper.append(None)

def clear_window(widget):
    window = widget.winfo_toplevel()
    for child in window.winfo_children():
        child.destroy()
    return window
