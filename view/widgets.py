from tkinter import *
from tkinter import ttk
import threading
import gc

class Window(Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title)
        self.threads = []

    def stop_threads(self):
        for thread in self.threads:
            if thread.is_alive():
                thread.stop()

    def destroy(self):
        self.stop_threads()
        super().destroy()

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

class Label(Label):
    def __init__(self, parent, text, fontsize=10, wraptext=False, cursor=None, color=None):
        super().__init__(parent, text=text, font=("Montserrat", fontsize), cursor=cursor, fg=color)
        if wraptext:
            self.bind("<Configure>", lambda _: self.config(wraplength=self.winfo_width()))
    
    def set_text(self, new_text):
        self.config(text=new_text)

class TextArea(Text):
    def __init__(self, parent, text, fontsize=10, cursor=None):
        super().__init__(parent, font=("Montserrat", fontsize), cursor=cursor, wrap=WORD)
        self["height"] = 5
        if text:
            self.insert(END, text)
        self.config(state=DISABLED)
    
    def set_text(self, new_text):
        self.config(state=NORMAL)
        self.delete(1.0, END)
        self.insert(END, new_text)
        self.config(state=DISABLED)

    def get_index(self, x, y):
        i = self.count("1.0", "@%d,%d" % (x, y))
        if i == None:
            return 0
        else:
            return i[0]

class Button(Button):
    def __init__(self, parent, text, command=None, fontsize=10, width=12, height=None, on_tab=None, image=None):
        super().__init__(parent, text=text, command=command, width=width, height=height, font=("Montserrat", fontsize), cursor="hand2", image=image)
        self._command = command
        self.bind("<Return>", lambda _: command())
        if on_tab:
            self.bind("<Tab>", on_tab)

class Treeview(ttk.Treeview):
    def __init__(self, parent, columns):
        super().__init__(parent, columns=columns, show="headings", cursor="arrow", selectmode=BROWSE)

class ScrollbarFrame(Frame):
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

class CheckBox(Checkbutton):
    def __init__(self, parent, text, selected=False, on_tab=None):
        super().__init__(parent, text=text, command=self.on_switch, cursor="hand2")
        self.value = selected
        if selected:
            self.select()
        if on_tab:
            self.bind("<Tab>", on_tab)

    def on_switch(self):
        self.value = False if self.value else True

    def get(self):
        return self.value

class TextField(Text):
    def __init__(self, parent, text=None, width=None, on_tab=None):
        super().__init__(parent)
        self["height"] = 1
        if width:
            self["width"] = width
        if on_tab:
            self.bind("<Tab>", on_tab)
        if text:
            self.insert(END, text)
    
    def set_text(self, new_text):
        self.delete(1.0, END)
        self.insert(END, new_text)

    def get(self):
        return super().get("1.0","end-1c")

    def focus(self):
        super().focus()
        self.tag_add(SEL, "1.0", END)

class ProgressBar(Frame):
    def __init__(self, parent, function=None, on_complete=None, description=""):
        super().__init__(parent)
        progress = ttk.Progressbar(self, maximum=1)
        description_label = Label(self, description, fontsize=8)
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

def focus(widget):
    widget.focus()
    return "break"

def clear_window(widget):
    window = widget.winfo_toplevel()
    window.stop_threads()
    window.unbind("<Button-1>")
    for child in window.winfo_children():
        child.destroy()
    gc.collect() # Without this, garbage collector would cause "NotImplementedError: Call from another thread"
    return window
