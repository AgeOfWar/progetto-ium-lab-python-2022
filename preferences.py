import json
import os

PREFERENCES_PATH = os.path.join("config", "preferences.json")

def read_or_create_preferences(start_dictionary=None):
    if os.path.isfile(PREFERENCES_PATH):
        return read_preferences()
    else:
        return write_preferences(start_dictionary)

def read_preferences():
    with open(PREFERENCES_PATH, "r") as file:
        return json.load(file)

def write_preferences(start_dictionary=None):
    os.makedirs(os.path.dirname(PREFERENCES_PATH), exist_ok=True)
    preferences = {
        "start_dictionary": start_dictionary
    }
    with open(PREFERENCES_PATH, "w") as file:
        json.dump(preferences, file)
    return preferences
