import os

from files import *

DICTIONARIES_PATH = os.path.join("config", "dictionaries")

def dictionary_path(name, *paths):
    return os.path.join(DICTIONARIES_PATH, name, *paths)

def find_dictionaries():
    if not os.path.isdir(DICTIONARIES_PATH):
        return
    for name in os.listdir(DICTIONARIES_PATH):
        if os.path.isdir(dictionary_path(name)):
            words_path = dictionary_path(name, "words.dat")
            if os.path.isfile(words_path):
                with open(words_path, "rb") as words_file:
                    words_count = unpack_int(words_file)
                yield (name, words_count)

def delete_dictionary(name):
    rmtree(dictionary_path(name))

def rename_dictionary(old_name, new_name):
    os.rename(dictionary_path(old_name), dictionary_path(new_name))

def parse_dictionary(path):
    return sorted(read_to_set(path))

def create_dictionary(name, words):
    os.makedirs(dictionary_path(name), exist_ok=True)
    with open(dictionary_path(name, "words.dat"), "wb") as file:
        file.write(pack_int(len(words)))
        for word in words:
            file.write(pack_string(word))
    return (name, len(words))

def read_dictionary(name):
    words = []
    word_map = {}
    with open(dictionary_path(name, "words.dat"), "rb") as file:
        nodes_len = unpack_int(file)
        for i in range(nodes_len):
            word = unpack_string(file)
            words.append(word)
            word_map[word] = i
    return words, word_map

def exists_dictionary(name):
    return os.path.isfile(dictionary_path(name, "words.dat"))