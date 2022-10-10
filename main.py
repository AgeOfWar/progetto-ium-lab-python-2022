from sys import argv, stderr
from numpy import array
import shutil

from files import *
import rules

config_path = "config"
configurations_path = os.path.join(config_path, "configurations")

def main():
    configuration, words_path = parse_arguments()
    if words_path != None:
        print("reading dictionary '" + words_path + "'...")
        words = sorted(read_to_set(words_path))
        shutil.rmtree(os.path.join(configurations_path, configuration), ignore_errors=True)
        os.makedirs(os.path.join(configurations_path, configuration))
        write_graph_words(os.path.join(configurations_path, configuration, "words.dat"), words)
    print("loading configuration '" + configuration + "'...")
    graph = read_graph(os.path.join(configurations_path, configuration))
    word = input("> ").strip()
    while word != "exit":
        if '-' in word:
            w1, w2 = word.split("-")
            c = 0
            for path in graph.find_paths(w1, w2):
                print(" -> ".join(path))
                c += 1
                if c == 5:
                    print("...")
                    break
            if c == 0:
                print("no path found")
        else:
            add_w = not graph.has_word(word)
            if add_w:
                print("(new)")
                graph.add_word(word)
            for _, target, data in graph.graph.out_edges(word, data=True):
                print(target + " (" + data["rule"].__name__ + " " + str(data["match"]) + ")")
            if add_w:
                graph.del_word(word)
        word = input("> ").strip()

def parse_arguments():
    configuration = None
    words_path = None
    for arg in argv[1:]:
        if configuration == None:
            configuration = arg
        elif words_path == None:
            words_path = arg
        else:
            print("Usage: main.py <configuration> [words_path]", file=stderr)
            exit(1)
    if configuration == None:
        print("Usage: main.py <configuration> [words_path]", file=stderr)
        exit(1)
    return configuration, words_path

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
