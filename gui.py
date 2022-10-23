from tkinter import *

from view.widgets import Window 
from view import dictionaries_widget
from view import dictionary_loading_widget

from dictionaries import exists_dictionary
from preferences import read_or_create_preferences

def main():
    preferences = read_or_create_preferences()
    window = Window("Parole")
    start_dicionary = preferences["start_dictionary"]
    if start_dicionary == None or not exists_dictionary(start_dicionary):
        dictionaries_widget.setup_window(window)
    else:
        dictionary_loading_widget.setup_window(window, start_dicionary)
    window.mainloop()

if __name__ == "__main__":
    main()
