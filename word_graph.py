from networkx import MultiDiGraph, all_shortest_paths, NetworkXNoPath
import os

from dictionaries import *
from files import *
import rules

class WordGraph:
    def __init__(self, words, adjacency_list, active_rules=None):
        if active_rules == None:
            active_rules = dict.fromkeys(rules.rules, 1)
        graph = MultiDiGraph()
        graph.add_nodes_from(words)
        graph.add_edges_from(adjacency_list)
        self.graph = graph
        self.active_rules = active_rules

    def add_word(self, word):
        adjacency_list = []
        len_word = len(word)
        for other in self.graph:
            len_other = len(other)
            for rule in rules.rules:
                match = rule(word, other, len_word, len_other)
                if match != None:
                    adjacency_list.append((word, other, {"rule": rule, "match": match}))
                match = rule(other, word, len_other, len_word)
                if match != None:
                    adjacency_list.append((other, word, {"rule": rule, "match": match}))
        self.graph.add_node(word)
        self.graph.add_edges_from(adjacency_list)

    def del_word(self, word):
        self.graph.remove_node(word)

    def has_word(self, word):
        return self.graph.has_node(word)

    def find_paths(self, w1, w2, remember_new=False):
        add_w1 = not self.has_word(w1)
        add_w2 = not self.has_word(w2)
        if add_w1:
            self.add_word(w1)
        if add_w2:
            self.add_word(w2)
        try:
            paths = all_shortest_paths(self.graph, w1, w2, weight=self._calculate_weight)
            paths = list(paths)
        except NetworkXNoPath:
            paths = []
        if add_w1 and not remember_new:
            self.del_word(w1)
        if add_w2 and not remember_new:
            self.del_word(w2)
        return paths

    def _calculate_weight(self, w1, w2, rules):
        return min((self.active_rules[rule["rule"]] for rule in rules.values() if rule["rule"] in self.active_rules), default=None)

def generate_rule(words, rule, detail_progress, stop_event):
    detail_progress.request_reset()
    detail_progress.request_set_maximum(len(words))
    for w1 in words:
        detail_progress.request_set_description(w1 + " ")
        len_w1 = len(w1)
        for w2 in words:
            if stop_event.is_set():
                return
            if w1 != w2:
                len_w2 = len(w2)
                match = rule(w1, w2, len_w1, len_w2)
                if match != None:
                    yield (w1, w2, {"rule": rule, "match": match})
        detail_progress.request_progress()

def read_or_create_graph(name, progress, detail_progress, stop_event, active_rules=None):
    words, word_map = read_dictionary(name)
    adjacency_list = []
    progress.request_set_maximum(len(rules.rules))
    for rule in rules.rules:
        if stop_event.is_set():
            return
        progress.request_set_description(rule.__name__ + " ")
        adjacency_list += read_or_create_graph_rule(name, rule, words, word_map, detail_progress, stop_event)
        progress.request_progress()
    return WordGraph(words, adjacency_list, active_rules)

def read_or_create_graph_rule(name, rule, words, word_map, detail_progress, stop_event):
    if os.path.isfile(dictionary_path(name, rule.__name__ + ".dat")):
        return read_graph_rule(name, rule, words, detail_progress, stop_event)
    else:
        generated = list(generate_rule(words, rule, detail_progress, stop_event))
        if stop_event.is_set():
            return []
        write_graph_rule(name, rule, word_map, generated)
        return generated

def read_graph_rule(name, rule, words, detail_progress, stop_event):
    adjacency_list = []
    with open(dictionary_path(name, rule.__name__ + ".dat"), "rb") as file:
        adjacency_list_len = unpack_int(file)
        detail_progress.request_reset()
        detail_progress.request_set_maximum(adjacency_list_len)
        detail_progress.request_set_description(rule.__name__ + ".dat ")
        for _ in range(adjacency_list_len):
            if stop_event.is_set():
                return []
            w1 = words[unpack_int(file)]
            w2 = words[unpack_int(file)]
            match_type = rules.rules[rule]
            if match_type == int:
                adjacency_list.append((w1, w2, {"rule": rule, "match": unpack_int(file)}))
            elif match_type == None:
                adjacency_list.append((w1, w2, {"rule": rule, "match": True}))
            detail_progress.request_progress()
    return adjacency_list

def write_graph_rule(name, rule, word_map, adjacency_list):
    with open(dictionary_path(name, rule.__name__ + ".dat"), "wb") as file:
        file.write(pack_int(len(adjacency_list)))
        for source, target, attributes in adjacency_list:
            file.write(pack_int(word_map[source]))
            file.write(pack_int(word_map[target]))
            match = attributes["match"]
            match_type = rules.rules[rule]
            if match_type == int:
                file.write(pack_int(match))