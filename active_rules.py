import rules
import json
import os

from dictionaries import dictionary_path

def read_or_create_active_rules(dictionary, active_rules):
    if os.path.isfile(active_rules_path(dictionary)):
        return read_active_rules(dictionary)
    else:
        return write_active_rules(dictionary, active_rules)

def read_active_rules(dictionary):
    with open(active_rules_path(dictionary), "r") as file:
        return dict((getattr(rules, rule), weight) for rule, weight in json.load(file).items())

def write_active_rules(dictionary, active_rules):
    os.makedirs(os.path.dirname(active_rules_path(dictionary)), exist_ok=True)
    with open(active_rules_path(dictionary), "w") as file:
        json.dump(dict((rule.__name__, weight) for rule, weight in active_rules.items()), file, indent=2)
    return active_rules

def active_rules_path(dictionary):
    return os.path.join(dictionary_path(dictionary), "active_rules.json")
