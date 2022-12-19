import rules
from tkinter import *
from view.widgets import *

from view import dictionaries_widget, word_graph_settings_widget

from preferences import write_preferences

def setup_window(window, dictionary, graph, initial_words=None):
    window.title("Parole - " + dictionary)
    window.geometry("600x400")
    window.minsize(600, 400)
    WordGraphFrame(window, dictionary, graph, initial_words).pack(fill=BOTH, expand=True, padx=10, pady=10)

class WordGraphFrame(Frame):
    def __init__(self, parent, dictionary, graph, initial_words):
        super().__init__(parent)
        self.dictionary = dictionary
        self.graph = graph
        self.path_index = 0
        self.old_w1 = None
        self.old_w2 = None
        self.paths = []
        self.words_frame = Frame(self)
        self.w1 = TextField(self.words_frame, on_tab=lambda _: focus(self.w2))
        self.w2 = TextField(self.words_frame, on_tab=lambda _: focus(self.random_button))
        self.remember_new = CheckBox(self, "ricorda parole nuove", on_tab=lambda _: focus(self.find_button))
        self.random_button_image = PhotoImage(file="assets/random.png")
        self.random_button = Button(self.words_frame, None, image=self.random_button_image, command=self.random_words, width=40, height=40, on_tab=lambda _: focus(self.remember_new))
        self.random_button.pack(side=RIGHT, anchor=NE, padx=(10,0))
        self.find_button = Button(self, "Trova", command=self.find_path, on_tab=lambda _: focus(self.settings_button))
        self.alternatives_label = Label(self, "")
        self.result = ResultFrame(self, graph)
        self.actions_frame = Frame(self)
        self.settings_button = Button(self.actions_frame, "Impostazioni", command=self.settings, on_tab=lambda _: focus(self.back_button))
        self.back_button = Button(self.actions_frame, "Indietro", command=self.back, on_tab=lambda _: focus(self.w1))
        self.words_frame.pack(fill=X)
        self.w1.pack(fill=X)
        self.w2.pack(fill=X)
        self.remember_new.pack(anchor=W)
        self.find_button.pack(pady=(10, 0))
        self.alternatives_label.pack(anchor=W)
        self.result.pack(fill=BOTH, expand=True, pady=(0, 10))
        self.actions_frame.pack(fill=X)
        self.settings_button.pack(side=LEFT)
        self.back_button.pack(side=RIGHT)
        if initial_words == None:
            self.random_words()
        else:
            self.w1.set_text(initial_words[0])
            self.w2.set_text(initial_words[1])
            self.find_path()
        

    def random_words(self):
        self.w1.set_text(self.graph.random_word())
        self.w2.set_text(self.graph.random_word())
        self.find_path()

    def find_path(self):
        w1 = self.w1.get().strip()
        w2 = self.w2.get().strip()
        if w1 == "" or w2 == "":
            return
        if self.old_w1 != w1 or self.old_w2 != w2:
            self.result.clear()
            self.paths = self.graph.find_paths(w1, w2, remember_new=self.remember_new.get())
            self.path_index = 0
        self.old_w1 = w1
        self.old_w2 = w2
        if self.paths == []:
            path = None
            self.alternatives_label.set_text("")
        else:
            path = self.paths[self.path_index]
            if len(self.paths) == 1:
                self.alternatives_label.set_text("")
            else:
                self.alternatives_label.set_text(f"alternativa {self.path_index + 1}/{len(self.paths)}")
            self.path_index += 1
            self.path_index %= len(self.paths)
        self.result.show_path(path)

    def settings(self):
        initial_words = (self.w1.get(), self.w2.get())
        window = clear_window(self)
        word_graph_settings_widget.setup_window(window, self.dictionary, self.graph, initial_words)

    def back(self):
        window = clear_window(self)
        write_preferences(start_dictionary=None)
        dictionaries_widget.setup_window(window)

class ResultFrame(ttk.Frame):
    def __init__(self, parent, graph):
        super().__init__(parent)
        self.graph = graph
        self.details = None
        self.explanations = {}
        self.result_label = TextArea(self, str(graph))
        self.details_label = MultiColorLabel(self)
        self.result_label.pack(fill=X, anchor=N)
        self.details_label.pack(fill=Y, expand=True)
        self.result_label.bind("<Motion>", self._enter)
        self.result_label.bind("<Leave>", self._leave)

    def _enter(self, event):
        for range, explanation in self.explanations.items():
            if self.result_label.get_index(event.x, event.y) in range:
                self.details_label.set_text(explanation)
                self.result_label.config(cursor="hand2")
                return "break"
        else:
            self.details_label.set_text(self.details)
            self.result_label.config(cursor="")
            return "break"

    def _leave(self, _):
        self.details_label.set_text(self.details)
        self.result_label.config(cursor="")
        return "break"

    def clear(self):
        self.explanations = {}
        self.details = None
        self.result_label.set_text("")
        self.details_label.set_text(None)

    def show_path(self, path):
        self.explanations = {}
        self.details = None
        if path == None:
            self.result_label.set_text("Nessun percorso trovato.")
            return
        path, rules = path
        self.result_label.set_text(" → ".join(path))
        offset = len(path[0])
        weight = 0
        for i in range(len(rules)):
            weight += self.graph.active_rules[rules[i]["rule"]]
            w1 = path[i]
            w2 = path[i + 1]
            self.explanations[range(offset, offset + 3)] = self._to_details(rules[i], w1, w2)
            offset += len(w2) + 3
        self.details = [(path[0], None), (" →", None), (str(weight), None, 8), (" ", None), (path[-1], None)]
        self.details_label.set_text(self.details)
    
    def _to_details(self, rule, w1, w2):
        function = rule["rule"]
        match = rule["match"]
        weight = self.graph.active_rules[function]

        normal = None
        moved = "#ff7514"
        added = "green"
        removed = "red"
        to = [(" →", None), (str(weight), None, 8), (" ", None)]

        if function == rules.change_first_letter:
            return [(w1[0], removed), (w1[1:], normal)] + to + [(w2[0], added), (w2[1:], normal)]
        elif function == rules.change_last_letter:
            return [(w1[:-1], normal), (w1[-1], removed)] + to + [(w2[:-1], normal), (w2[-1], added)]
        elif function == rules.change_letter:
            return [(w1[0:match], normal), (w1[match], removed), (w1[match+1:], normal)] + to + [(w2[0:match], normal), (w2[match], added), (w2[match+1:], normal)]
        elif function == rules.add_first_letter:
            return [(w1, normal)] + to + [(w2[0], added), (w2[1:], normal)]
        elif function == rules.add_last_letter:
            return [(w1, normal)] + to + [(w2[:-1], normal), (w2[-1], added)]
        elif function == rules.add_letter:
            return [(w1, normal)] + to + [(w2[0:match], normal), (w2[match], added), (w2[match+1:], normal)]
        elif function == rules.remove_first_letter:
            return [(w1[0], removed), (w1[1:], normal)] + to + [(w2, normal)]
        elif function == rules.remove_last_letter:
            return [(w1[:-1], normal), (w1[-1], removed)] + to + [(w2, normal)]
        elif function == rules.remove_letter:
            return [(w1[0:match], normal), (w1[match], removed), (w1[match+1:], normal)] + to + [(w2, normal)]
        elif function == rules.anagram:
            return [(w1[i], moved if i in match else normal) for i in range(len(w1))] + to + [(w2[i], moved if i in match else normal) for i in range(len(w2))]
        elif function == rules.swap_two_letters:
            i1, i2 = match
            return [(w1[0:i1], normal), (w1[i1], moved), (w1[i1+1:i2], normal), (w1[i2], moved), (w1[i2+1:], normal)] + to + [(w2[0:i1], normal), (w2[i1], moved), (w2[i1+1:i2], normal), (w2[i2], moved), (w2[i2+1:], normal)]
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

    def set_text(self, text):
        self.clear()
        if text == None:
            return
        text_len = sum(len(part[0]) for part in text)
        if text_len <= 20:
            fontsize = 28
        elif text_len <= 28:
            fontsize = 20
        else:
            fontsize = 14
        for part in text:
            if (len(part) >= 3):
                self.add_text(part[0], part[1], fontsize=part[2])
            else:
                self.add_text(part[0], part[1], fontsize=fontsize)
