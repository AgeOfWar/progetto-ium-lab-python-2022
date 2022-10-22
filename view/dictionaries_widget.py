from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from view.widgets import *

from view import dictionary_loading_widget

from dictionaries import *

def setup_window(window):
    window.title("Parole - Scelta dizionario")
    window.geometry("540x360")
    window.minsize(420, 300)
    DictionaryManager(window).pack(fill=BOTH, expand=True, padx=10, pady=10)

class DictionaryManager(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        Label(self, "Scegli il dizionario o creane uno nuovo.").pack(anchor=W)
        check_button = CheckBox(self, "ricorda la scelta", selected=True)
        DictionariesView(self, check_button).pack(fill=BOTH, expand=True)
        check_button.pack(anchor=W)

class DictionariesView(Frame):
    def __init__(self, parent, remember_choice):
        super().__init__(parent)
        dictionaries = ScrollbarFrame(self, lambda parent: Dictionaries(parent, remember_choice))
        dictionaries.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))
        Actions(self, dictionaries.widget).pack(side=LEFT, fill=Y, padx=(5, 0))

class Dictionaries(Treeview):
    def __init__(self, parent, remember_choice):
        self.remember_choice = remember_choice
        super().__init__(parent, columns=("name", "word_count"))
        self.heading("name", text="Nome", anchor=W)
        self.heading("word_count", text="Parole", anchor=W)
        self.column("name", stretch=YES, anchor=W)
        self.column("word_count", width=60, stretch=NO, anchor=W)
        for dictionary in find_dictionaries():
            self.insert("", END, values=dictionary)
        self.bind("<Button-1>", self._no_stretch)
        self.bind("<ButtonRelease-1>", self._no_stretch)
        self.bind("<Motion>", self._no_stretch)
        self.bind("<Button-3>", self.options)
        self.bind("<Double-1>", self.on_item_selection)
        self.bind("<Return>", self.on_item_selection)
        self.winfo_toplevel().bind("<Button-1>", self._deselect_all)

    def on_item_selection(self, event):
        item = self.identify_row(event.y)
        if item:
            self.context_menu_choice(item)

    def options(self, event):
        item = self.identify_row(event.y)
        if item:
            self.selection_set(item)
            self.context_menu(item).post(event.x_root, event.y_root)

    def context_menu(self, item):
        menu = Menu(self, tearoff=False)
        menu.add_command(label="Scegli", command=lambda: self.context_menu_choice(item))
        menu.add_separator()
        menu.add_command(label="Elimina", command=lambda: self.context_menu_delete(item))
        menu.add_command(label="Rinomina", command=lambda: self.context_menu_rename(item))
        return menu

    def context_menu_choice(self, item):
        name, _ = self.item(item)["values"]
        dictionary_loading_widget.setup_window(clear_window(self), name)

    def context_menu_delete(self, item):
        delete_dictionary(self.item(item)["values"][0])
        self.delete(item)

    def context_menu_rename(self, item):
        old_name, word_count = self.item(item)["values"]
        x, y, width, height = self.bbox(item, 0)
        entry = EntryPopup(self, old_name, lambda new_name: self.rename(item, old_name, new_name, word_count))
        entry.place(x=x, y=y+height//2, width=width, height=height, anchor=W)
    
    def rename(self, item, old_name, new_name, word_count):
        if old_name == new_name or len(new_name.strip()) == 0:
            return
        try:
            rename_dictionary(old_name, new_name)
            self.item(item, values=(new_name, word_count))
        except FileExistsError:
            messagebox.showerror("Impossibile rinominare", "Il nome '" + new_name + "' è già in uso.")

    def add(self, item, name, words):
        try:
            create_dictionary(name, words)
            self.item(item, values=(name, len(words)))
            self.selection_set(item)
        except FileExistsError:
            print("WHAT")
            self.delete(item)
            messagebox.showerror("Impossibile creare", "Il nome '" + name + "' è già in uso.")

    def _no_stretch(self, event):
        if self.identify_region(event.x, event.y) == "separator":
            self.config(cursor="arrow")
            return "break"

    def _deselect_all(self, event):
        item = self.identify_element(event.x, event.y)
        if not item:
            if len(self.selection()) > 0:
                self.selection_remove(self.selection()[0])

class Actions(Frame):
    def __init__(self, parent, dictionaries):
        super().__init__(parent)
        Button(self, "CREA", command=self.on_new).pack()
        self.dictionaries = dictionaries

    def on_new(self):
        path = filedialog.askopenfilename(initialdir=".", filetypes=(
            ("Text files", "*.txt"),
            ("CSV files", "*.csv"),
            ("All files", "*.*")
        ))
        if len(path) == 0:
            return
        words = parse_dictionary(path)
        new_item = self.dictionaries.insert("", END, values=("", len(words)))
        x, y, width, height = self.dictionaries.bbox(new_item, 0)
        entry = EntryPopup(self.dictionaries, "", lambda new_name: self.new_dictionary(new_name, new_item, words), on_cancel=lambda: self.dictionaries.delete(new_item))
        entry.place(x=x, y=y+height//2, width=width, height=height, anchor=W)
    
    def new_dictionary(self, new_name, new_item, words):
        if len(new_name.strip()) == 0:
            self.dictionaries.delete(new_item)
            return
        self.dictionaries.add(new_item, new_name, words)


class EntryPopup(Entry):
    def __init__(self, parent, text, on_submit, on_cancel=None):
        super().__init__(parent)
        self.done = False
        self._on_submit = on_submit
        self._on_cancel = on_cancel
        self.insert(0, text) 
        self["exportselection"] = False

        self.focus_force()
        self.bind("<Return>", self.on_return)
        self.bind("<Control-a>", self.select_all)
        self.bind("<Escape>", self.on_cancel)
        self.bind("<FocusOut>", self.on_cancel)

    def on_return(self, _):
        self.done = True
        self._on_submit(self.get())
        self.destroy()

    def select_all(self, _):
        self.selection_range(0, END)
        return "break"

    def on_cancel(self, _):
        if not self.done:
            self.destroy()
            if self._on_cancel != None:
                self._on_cancel()
