import rules
from active_rules import *
from tkinter import *
from view.widgets import *

from view import word_graph_widget

def setup_window(window, dictionary, graph, initial_words):
    window.title("Parole - Impostazioni " + dictionary)
    window.geometry("600x400")
    window.minsize(600, 450)
    SettingsFrame(window, dictionary, graph, initial_words).pack(fill=BOTH, expand=True, padx=10, pady=10)

all_rules = {
        rules.change_letter: "cambia una lettera",
        rules.change_first_letter: "cambia la prima lettera",
        rules.change_last_letter: "cambia l'ultima lettera",
        rules.add_letter: "aggiungi una lettera",
        rules.add_first_letter: "aggiungi una lettera all'inizio",
        rules.add_last_letter: "aggiungi una lettera alla fine",
        rules.remove_letter: "rimuovi una lettera",
        rules.remove_first_letter: "rimuovi la prima lettera",
        rules.remove_last_letter: "rimuovi l'ultima lettera",
        rules.anagram: "anagramma",
        rules.swap_two_letters: "scambia due lettere"
    }

class SettingsFrame(ttk.Frame):
    def __init__(self, parent, dictionary, graph, initial_words):
        super().__init__(parent)
        self.initial_words = initial_words
        self.dictionary = dictionary
        self.graph = graph
        self.grid = Frame(self)
        self.checkboxes = dict((rule, CheckBox(self.grid, description, selected=graph.active_rules[rule] != None, on_switch=lambda value, rule=rule: self._on_rule_switch(rule, value))) for rule, description in all_rules.items())
        self.example_labels = dict((rule, Label(self.grid, " → ".join(graph.random_example(rule)))) for rule in all_rules)
        self.weight_fields = dict((rule, IntField(self.grid, graph.active_rules[rule], width=3, validation=lambda value, rule=rule: self._weight_validation(rule, value))) for rule in all_rules)
        self.actions_frame = Frame(self)
        self.cancel_button = Button(self.actions_frame, "Annulla", command=self.cancel)
        self.apply_button = Button(self.actions_frame, "Applica", command=self.apply)
        self.defaults_button = Button(self.actions_frame, "Predefiniti", command=self.defaults)
        self.grid.columnconfigure(0, weight=1)
        self.grid.columnconfigure(1, minsize=200)
        self.grid.pack(anchor=N, fill=X, expand=True)
        Label(self.grid, "Regola", fontsize=14).grid(row=0, column=0, sticky=W)
        Label(self.grid, "Esempio", fontsize=14).grid(row=0, column=1, sticky=W)
        Label(self.grid, "Peso", fontsize=14).grid(row=0, column=2, sticky=W)
        for index, rule in enumerate(all_rules):
            self.checkboxes[rule].grid(row=index + 1, column=0, sticky=W, padx=(20,0) if len(rules.supersets(rule)) > 0 else 0)
            self.example_labels[rule].grid(row=index + 1, column=1, sticky=W)
            self.weight_fields[rule].grid(row=index + 1, column=2, sticky=W)
        self.actions_frame.pack(side=BOTTOM, fill=X)
        self.apply_button.pack(side=RIGHT)
        self.cancel_button.pack(side=RIGHT, padx=10)
        self.defaults_button.pack(side=LEFT)

    def _weight_validation(self, rule, value):
        if not hasattr(self, "weight_fields"):
            return True
        if value == None:
            self.checkboxes[rule].deselect()
            return True
        if value < 1 or value > 999:
            return False
        for super in rules.supersets(rule):
            weight = self.weight_fields[super]
            if weight.get() != None:
                weight.set_value(max(weight.get(), value))
        for subset in rules.subsets(rule):
            weight = self.weight_fields[subset]
            if weight.get() != None:
                weight.set_value(min(weight.get(), value))
        self.checkboxes[rule].select()
        return True

    def _on_rule_switch(self, rule, value):
        self.weight_fields[rule].set_value(1 if value else None)

    def defaults(self):
        for weight in self.weight_fields.values():
            weight.set_value(1)

    def apply(self):
        self.graph.active_rules = dict((rule, self.weight_fields[rule].get()) for rule in rules.rules)
        write_active_rules(self.dictionary, self.graph.active_rules)
        window = clear_window(self)
        word_graph_widget.setup_window(window, self.dictionary, self.graph, initial_words=self.initial_words)

    def cancel(self):
        window = clear_window(self)
        word_graph_widget.setup_window(window, self.dictionary, self.graph, initial_words=self.initial_words)