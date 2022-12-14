import rules
from tkinter import *
from view.widgets import *

from view import dictionaries_widget

from preferences import write_preferences

def setup_window(window, dictionary, graph):
    window.title("Parole - " + dictionary)
    window.geometry("600x400")
    window.minsize(600, 400)
    WordGraphFrame(window, graph).pack(fill=BOTH, expand=True, padx=10, pady=10)

class WordGraphFrame(ttk.Frame):
    def __init__(self, parent, graph):
        super().__init__(parent, padding=10)
        self.graph = graph
        self.frame = ttk.Frame(self, padding=0)
        self.frame.pack(fill=X)
        self.w1 = TextField(self.frame, on_tab=lambda _: focus(self.w2))
        self.w2 = TextField(self.frame, on_tab=lambda _: focus(self.random_button))
        self.remember_new = CheckBox(self, "ricorda parole nuove", on_tab=lambda _: focus(self.find_button))
        self.random_button_image = PhotoImage(file="assets/random.png")
        self.random_button = Button(self.frame, None, image=self.random_button_image, command=self.random_words, width=40, height=40, on_tab=lambda _: focus(self.remember_new))
        self.random_button.pack(side=RIGHT, anchor=NE, padx=(10,0))
        self.find_button = Button(self, "Trova", command=self.find_path, on_tab=lambda _: focus(self.back_button))
        self.result = ResultFrame(self, graph)
        self.back_button = Button(self, "Indietro", command=self.back, on_tab=lambda _: focus(self.w1))
        self.w1.pack(fill=X)
        self.w2.pack(fill=X)
        self.remember_new.pack(anchor=W)
        self.find_button.pack(pady=10)
        self.result.pack(fill=BOTH, expand=True, pady=10)
        self.back_button.pack(side=BOTTOM, anchor=SE)
        self.random_words()

    def random_words(self):
        self.w1.set_text(self.graph.random_word())
        self.w2.set_text(self.graph.random_word())
        self.find_path()

    def find_path(self):
        w1 = self.w1.get().strip()
        w2 = self.w2.get().strip()
        paths = self.graph.find_paths(w1, w2, remember_new=self.remember_new.get())
        if paths == []:
            path = None
        else:
            path = paths[0]
        self.result.show_path(path)

    def back(self):
        window = clear_window(self)
        write_preferences(start_dictionary=None)
        dictionaries_widget.setup_window(window)

class ResultFrame(ttk.Frame):
    def __init__(self, parent, graph):
        super().__init__(parent)
        self.graph = graph
        self.explanations = {}
        self.result_label = TextArea(self, str(graph))
        self.details_label = MultiColorLabel(self)
        self.result_label.pack(fill=X, expand=True, anchor=N)
        self.details_label.pack(side=BOTTOM)
        self.result_label.bind("<Motion>", self._enter)
        self.result_label.bind("<Leave>", self._leave)

    def _enter(self, event):
        for range, explanation in self.explanations.items():
            if self.result_label.get_index(event.x, event.y) in range:
                details_len = sum(len(part[0]) for part in explanation)
                if details_len <= 20:
                    self.details_label.set_text(explanation)
                elif details_len <= 28:
                    self.details_label.set_text(explanation, fontsize=20)
                else:
                    self.details_label.set_text(explanation, fontsize=14)
                self.result_label.config(cursor="hand2")
                return "break"
        else:
            self.details_label.clear()
            self.result_label.config(cursor="")
            return "break"

    def _leave(self, _):
        self.details_label.clear()
        self.result_label.config(cursor="")
        return "break"

    def show_path(self, path):
        self.explanations = {}
        if path == None:
            self.result_label.set_text("Nessun percorso trovato.")
            return
        path, rules = path
        self.result_label.set_text(" → ".join(path))
        offset = len(path[0])
        for i in range(len(rules)):
            w1 = path[i]
            w2 = path[i + 1]
            self.explanations[range(offset, offset + 3)] = self._to_details(rules[i], w1, w2)
            offset += len(w2) + 3
    
    def _to_details(self, rule, w1, w2):
        function = rule["rule"]
        match = rule["match"]

        normal = None
        moved = "#ff7514"
        added = "green"
        removed = "red"
        to = (" → ", normal)

        if function == rules.change_first_letter:
            return [(w1[0], removed), (w1[1:], normal), to, (w2[0], added), (w2[1:], normal)]
        elif function == rules.change_last_letter:
            return [(w1[:-1], normal), (w1[-1], removed), to, (w2[:-1], normal), (w2[-1], added)]
        elif function == rules.change_letter:
            return [(w1[0:match], normal), (w1[match], removed), (w1[match+1:], normal), to, (w2[0:match], normal), (w2[match], added), (w2[match+1:], normal)]
        elif function == rules.add_first_letter:
            return [(w1, normal), to, (w2[0], added), (w2[1:], normal)]
        elif function == rules.add_last_letter:
            return [(w1, normal), to, (w2[:-1], normal), (w2[-1], added)]
        elif function == rules.add_letter:
            return [(w1, normal), to, (w2[0:match], normal), (w2[match], added), (w2[match+1:], normal)]
        elif function == rules.remove_first_letter:
            return [(w1[0], removed), (w1[1:], normal), to, (w2, normal)]
        elif function == rules.remove_last_letter:
            return [(w1[:-1], normal), (w1[-1], removed), to, (w2, normal)]
        elif function == rules.remove_letter:
            return [(w1[0:match], normal), (w1[match], removed), (w1[match+1:], normal), to, (w2, normal)]
        elif function == rules.anagram:
            return [(w1[i], moved if i in match else normal) for i in range(len(w1))] + [to] + [(w2[i], moved if i in match else normal) for i in range(len(w2))]
        elif function == rules.swap_two_letters:
            i1, i2 = match
            return [(w1[0:i1], normal), (w1[i1], moved), (w1[i1+1:i2], normal), (w1[i2], moved), (w1[i2+1:], normal), to, (w2[0:i1], normal), (w2[i1], moved), (w2[i1+1:i2], normal), (w2[i2], moved), (w2[i2+1:], normal)]
        else:
            return []


class MultiColorLabel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.widgets = []

    def clear(self):
        for widget in self.widgets:
            widget.destroy()
        self.widgets = []

    def add_text(self, text, color, fontsize=10):
        label = Label(self, text, color=color, fontsize=fontsize)
        label.config(padx=0)
        self.widgets.append(label)
        label.pack(side=LEFT)

    def set_text(self, text, fontsize=28):
        self.clear()
        for part in text:
            self.add_text(part[0], part[1], fontsize=fontsize)

