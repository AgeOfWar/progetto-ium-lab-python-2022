from struct import pack, unpack
from words import WordGraph, generate_rule
from tqdm import tqdm
import os

import rules

def read_to_set(path):
    with open(path, "r") as file:
        return set(line.strip() for line in file if line.strip() != "")

def read_graph(path, active_rules=None):
    words, word_map = read_graph_words(os.path.join(path, "words.dat"))
    adjacency_list = []
    for rule in tqdm(rules.rules):
        adjacency_list += read_or_generate_graph_rule(path, rule, words, word_map)
    return WordGraph(words, adjacency_list, active_rules)

def read_or_generate_graph_rule(path, rule, words, word_map):
    rule_path = os.path.join(path, rule.__name__ + ".dat")
    if os.path.isfile(rule_path):
        return read_graph_rule(rule_path, words, rule)
    else:
        generated = list(generate_rule(words, rule))
        write_graph_rule(rule_path, rule, word_map, generated)
        return generated

def read_graph_words(path):
    words = []
    word_map = {}
    with open(path, "rb") as file:
        nodes_len = _unpack_int(file)
        for i in range(nodes_len):
            word = _unpack_string(file)
            words.append(word)
            word_map[word] = i
    return words, word_map

def write_graph_words(path, words):
    with open(path, "wb") as file:
        file.write(_pack_int(len(words)))
        for word in words:
            file.write(_pack_string(word))

def read_graph_rule(path, words, rule):
    adjacency_list = []
    with open(path, "rb") as file:
        adjacency_list_len = _unpack_int(file)
        for _ in range(adjacency_list_len):
            w1 = words[_unpack_int(file)]
            w2 = words[_unpack_int(file)]
            match_type = rules.rules[rule]
            if match_type == int:
                adjacency_list.append((w1, w2, {"rule": rule, "match": _unpack_int(file)}))
            elif match_type == None:
                adjacency_list.append((w1, w2, {"rule": rule, "match": True}))
    return adjacency_list

def write_graph_rule(path, rule, word_map, adjacency_list):
    with open(path, "wb") as file:
        file.write(_pack_int(len(adjacency_list)))
        for source, target, attributes in adjacency_list:
            file.write(_pack_int(word_map[source]))
            file.write(_pack_int(word_map[target]))
            match = attributes["match"]
            match_type = rules.rules[rule]
            if match_type == int:
                file.write(_pack_int(match))

def _unpack_string(file):
    buffer = file.read(1)
    if buffer == '':
        return None
    s_len, = unpack("B", buffer)
    return unpack(str(s_len) + "s", file.read(s_len))[0].decode()

def _unpack_int(file):
    buffer = file.read(4)
    if buffer == '':
        return None
    return unpack("I", buffer)[0]

def _pack_string(s):
    b = s.encode()
    return pack("B", len(b)) + b

def _pack_int(n):
    return pack("I", n)
