import simpleaudio as sa
import tkinter as tk
from tkinter import ttk
from Fretboard import Fretboard
from Screen import Screen

if __name__ == "__main__":
    main_screen = Screen()

    main_screen.configure_styles()
    main_screen.main_screen()
    
    main_screen.window.mainloop()
