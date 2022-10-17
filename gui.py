from tkinter import *

from view.widgets import Window 
from view import dictionaries_widget

def main():
    window = Window("Parole")
    dictionaries_widget.setup_window(window)
    window.mainloop()

if __name__ == "__main__":
    main()
