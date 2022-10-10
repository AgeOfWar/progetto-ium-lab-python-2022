from networkx import MultiDiGraph, all_shortest_paths, NetworkXNoPath
from tqdm import tqdm

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

def generate_rule(words, rule):
    adjacency_list = []
    for w1 in tqdm(words, miniters=10, desc=rule.__name__):
        len_w1 = len(w1)
        for w2 in words:
            if w1 != w2:
                len_w2 = len(w2)
                match = rule(w1, w2, len_w1, len_w2)
                if match != None:
                    adjacency_list.append((w1, w2, {"rule": rule, "match": match}))
    return adjacency_list