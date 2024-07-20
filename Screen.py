import tkinter as tk
from tkinter import ttk
from Fretboard import Fretboard
import random

chords = [[(4, 2), (2, 2)], [(2, 1), (3, 2), (1, 2)], [(1, 2), (4, 4), (3, 4), (2, 4)],
        [(1, 2), (2, 3), (3, 4)], [(5, 2), (3, 2), (1, 2)], [(1, 1), (2, 1), (3, 2), (5, 3), (4, 3), (6, 1)], [(2, 1), (4, 2), (6, 3), (5, 3)], 
        [(1, 1), (3, 2), (2, 3)], [(4, 1), (5, 2), (3, 2), (1, 2)], [(1, 1), (2, 1), (3, 2), (4, 3)], [(3, 2), (1, 2), (2, 3)], [(5, 2), (6, 3), (1, 3)],
        [(2, 1), (4, 2), (5, 3)], [(5, 2), (4, 2)], [(3, 1), (5, 2), (4, 2)]]

class Screen:
    def __init__(self):
        self.fretboard = Fretboard()
        self.window = tk.Tk()
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.style = ttk.Style()
        self.prac_label = ttk.Label()

    def configure_styles(self):

        self.window.configure(
            background="#DEB887"
        )

        self.style.configure(
            "TLabel",
            background="#DEB887",
            foreground="#FFFFFF"
        )

        self.style.configure(
            "Correct.TButton",
            background="#004206",
            foreground="white"
        )

        self.style.configure(
            "Incorrect.TButton",
            background="#dd1923",
            foreground="white"
        )
    
        self.style.configure(
            "TButton",
            font=('Oswald', 12),
            background="#C0C0C0",
            foreground="#F8F8FF",
            height=50,
            width=30
        )

        self.style.configure(
            "String.TButton",
            background="#C0C0C0",
            foreground="#F8F8FF",
        )

        self.style.configure(
            "TEntry",
            font=('Oswald', 12),
        )

        self.style.configure(
            "TFrame",
            background="#DEB887"
        )

    # Main Screens that redirect to a users choice
    def main_screen(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        label = ttk.Label(self.window, text="Fretboard Master", font=("Oswald", 100))
        label.place(x=self.screen_width/2, y=self.screen_height/4, anchor='center')
        self.window.title("Fretboard Master")

        center_x = int(self.screen_width/2 - self.screen_width / 2)
        center_y = int(self.screen_height/2 - self.screen_height / 2)
        self.window.geometry(f'{self.screen_width}x{self.screen_height}+{center_x}+{center_y}')
        self.window.resizable(False, False)

        jam_button = ttk.Button(self.window, text="Jam?", command= lambda: self.jam_screen(), width=20)
        practice_button = ttk.Button(self.window, text="Practice", command= lambda: self.practice_screen(), width=20)
        learn_button = ttk.Button(self.window, text="Learn", command= lambda: self.learn_screen(), width=20)
        exit_button = ttk.Button(self.window, text="Exit", command= lambda: self.window.quit(), width=20)

        jam_button.place(x=self.screen_width/2, y=self.screen_height/2 + 20, anchor='center')
        practice_button.place(x=self.screen_width/2, y=self.screen_height/2 + 60, anchor='center')
        learn_button.place(x=self.screen_width/2, y=self.screen_height/2 + 100, anchor='center')
        exit_button.place(x=self.screen_width/2, y=self.screen_height/2 + 140, anchor='center')

    def jam_screen(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.window.title("Jam!")
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(expand=True, fill='both')
        screen_height = self.screen_height/4

        fretboard_frame = ttk.Frame(main_frame, padding=f'{screen_height}')
        fretboard_frame.pack()

        label = ttk.Label(fretboard_frame, text="Jam!", font=("Oswald", 24))
        label.grid(row=0, column=6, columnspan=2, pady=2, padx=2)

        for fret in range(self.fretboard.num_frets + 1):
            ttk.Label(fretboard_frame, text=str(fret)).grid(row=1, column=fret + 1, padx=2, pady=2)

        buttons = []
        for string in range(1, self.fretboard.num_strings+1):
            ttk.Label(fretboard_frame, text=["KEK", "e", "B", "G", "D", "A", "E"][string]).grid(row=string + 1, column=0, padx=2, pady=2)
            
            row_buttons = []
            for fret in range(self.fretboard.num_frets + 1):
                button = ttk.Button(fretboard_frame, text=f'{self.fretboard.get_note_at(string, fret)}', width=7, command=lambda s=string, f=fret: (self.fretboard.play_note(s, f), self.fretboard.notes_hit.append((s, f))), style="String.TButton")
                button.grid(row=string + 1, column=fret + 1, padx=2, pady=2)
                row_buttons.append(button)
            buttons.append(row_buttons)


        back_button_frame = ttk.Frame(main_frame)
        back_button_frame.pack()
        submit_button = ttk.Button(back_button_frame, text="Submit", command= lambda: self.fretboard.play_chord(self.fretboard.notes_hit), width=20)
        submit_button.pack(pady=(0, 20))
        back_button = ttk.Button(back_button_frame, text="Back", command= lambda: (self.main_screen(), self.fretboard.play_obj.stop()), width=20)
        back_button.pack()

    def practice_screen(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        
        self.window.title("Practice")
        screen_height = self.screen_height/3
        label = ttk.Label(self.window, text="Practice", font=("Oswald", 24))
        label.grid(row=0, column=0, columnspan=2, pady=screen_height/2)

        note_button = ttk.Button(self.window, text="Practice Notes", command=lambda: self.user_entry(), width=20)
        chord_button = ttk.Button(self.window, text="Practice Chords", command=lambda: self.practice_chord_screen(), width=20)
        scales_button = ttk.Button(self.window, text="Practice Scales", command=lambda: self.learn_screen(), width=20)
        back_button = ttk.Button(self.window, text="Back", command=lambda: self.main_screen(), width=20)

        note_button.grid(row=1, column=0, columnspan=2, pady=10)
        chord_button.grid(row=2, column=0, columnspan=2, pady=10)
        scales_button.grid(row=3, column=0, columnspan=2, pady=10)
        back_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

    def learn_screen(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.window.title("Learn")
        label = ttk.Label(self.window, text="Learn", font=("Oswald", 24))
        label.place(x=self.screen_width/2, y=self.screen_height/4 - 50, anchor='center')

        note_button = ttk.Button(self.window, text="Learn Notes", command=lambda: self.user_entry(), width=20)
        chord_button = ttk.Button(self.window, text="Learn Chords", command=lambda: self.practice_screen(), width=20)
        scales_button = ttk.Button(self.window, text="Learn Scales", command=lambda: self.learn_screen(), width=20)
        back_button = ttk.Button(self.window, text="Back", command=lambda: self.main_screen(), width=20)

        note_button.grid(row=1, column=0, columnspan=2, pady=10)
        chord_button.grid(row=2, column=0, columnspan=2, pady=10)
        scales_button.grid(row=3, column=0, columnspan=2, pady=10)
        back_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

    # Secondary screens users are redirected to after selecting an option
    def practice_note_screen(self, u_note):
        note = u_note.get().upper()
        for widget in self.window.winfo_children():
            widget.destroy()

        self.window.title("Practicing Notes")
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(expand=True, fill='both')
        screen_height = self.screen_height/9

        label_frame = ttk.Frame(main_frame)
        label_frame.pack(pady=f'{screen_height}')
        self.prac_label = ttk.Label(label_frame, text=f'Find {note}', font=("Oswald", 100))
        self.prac_label.grid(row=0, column=6, columnspan=2, pady=2, padx=2)

        fretboard_frame = ttk.Frame(main_frame, padding=f'{screen_height/3}')
        fretboard_frame.pack()
    
        for i in range(self.fretboard.num_frets + 2):
            fretboard_frame.columnconfigure(i, weight=1)
        for i in range(self.fretboard.num_strings + 2):
            fretboard_frame.rowconfigure(i, weight=1)


        for fret in range(self.fretboard.num_frets + 1):
            ttk.Label(fretboard_frame, text=str(fret)).grid(row=1, column=fret + 1, padx=2, pady=2)

        buttons = []
        for string in range(1, self.fretboard.num_strings+1):
            ttk.Label(fretboard_frame, text=["KEK", "e", "B", "G", "D", "A", "E"][string]).grid(row=string + 1, column=0, padx=2, pady=2)
            
            row_buttons = []
            for fret in range(self.fretboard.num_frets + 1):
                button = ttk.Button(fretboard_frame, text=f'{fret}', width=7, style="String.TButton")
                button.configure(command=lambda b=button, s=string, f=fret: self.prac_note_button_pressed(b, note, s, f))
                button.grid(row=string + 1, column=fret + 1, padx=2, pady=2)
                row_buttons.append(button)
            buttons.append(row_buttons)

        back_button_frame = ttk.Frame(main_frame, padding="-300")
        back_button_frame.pack()
        back_button = ttk.Button(back_button_frame, text="Back", command= lambda: (self.practice_screen(), self.fretboard.play_obj.stop()), width=20)
        back_button.pack()

    def practice_chord_screen(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        targ_chord = random.choice(chords)

        self.window.title("Practicing Chords")
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(expand=True, fill='both')
        screen_height = self.screen_height/9

        label_frame = ttk.Frame(main_frame)
        label_frame.pack(pady=f'{screen_height}')
        self.prac_label = ttk.Label(label_frame, text=f'Find {self.fretboard.get_chord_at(targ_chord)}', font=("Oswald", 100))
        self.prac_label.grid(row=0, column=6, columnspan=2, pady=2, padx=2)

        fretboard_frame = ttk.Frame(main_frame, padding=f'{screen_height/3}')
        fretboard_frame.pack()


        for fret in range(self.fretboard.num_frets + 1):
            ttk.Label(fretboard_frame, text=str(fret)).grid(row=1, column=fret + 1, padx=2, pady=2)

        buttons = []
        for string in range(1, self.fretboard.num_strings+1):
            ttk.Label(fretboard_frame, text=["KEK", "e", "B", "G", "D", "A", "E"][string]).grid(row=string + 1, column=0, padx=2, pady=2)
            
            row_buttons = []
            for fret in range(self.fretboard.num_frets + 1):
                button = ttk.Button(fretboard_frame, text=f'{self.fretboard.get_note_at(string, fret)}', width=7, command=lambda s=string, f=fret: (self.fretboard.play_note(s, f), self.fretboard.notes_hit.append((s, f))), style="String.TButton")
                button.grid(row=string + 1, column=fret + 1, padx=2, pady=2)
                row_buttons.append(button)
            buttons.append(row_buttons)


        back_button_frame = ttk.Frame(main_frame)
        back_button_frame.pack()
        submit_button = ttk.Button(back_button_frame, text="Submit", command= lambda: self.prac_chord_button_pressed(targ_chord, self.fretboard.notes_hit), width=20)
        submit_button.pack(pady=(0, 20))
        back_button = ttk.Button(back_button_frame, text="Back", command= lambda: (self.practice_screen(), self.fretboard.play_obj.stop()), width=20)
        back_button.pack()



    # Helper Functions for various screens
    def user_entry(self):
        entry_window = tk.Toplevel(self.window, bg="#DEB887")
        entry_window.title("Note Entry")

        entry_label = ttk.Label(entry_window, text="Enter Note:")
        entry_label.pack(padx=10, pady=5)
        
        note_entry = ttk.Entry(entry_window)
        note_entry.pack(padx=10, pady=5)
        note_entry.focus_set()

        submit_button = ttk.Button(entry_window, text="Submit", command=lambda: self.practice_note_screen(note_entry))
        submit_button.pack(padx=10, pady=5)

        entry_window.bind("<Return>", lambda event: self.practice_note_screen(note_entry))
    
    def prac_note_button_pressed(self, button, note, string, fret):
        self.fretboard.play_note(string, fret)
        self.fretboard.practice_note(note, self.fretboard.get_note_at(string, fret))
        if self.fretboard.played:
            button.configure(style="Correct.TButton")
            self.prac_label.config(text="Correct!")
        else:
            button.configure(style="Incorrect.TButton")
            correct_fret = self.fretboard.get_note_index(string, note)[1]
            self.prac_label.config(text=f"Incorrect! It's at fret {correct_fret}")

    def prac_chord_button_pressed(self, chord, notes):
        self.fretboard.practice_chord(chord, self.fretboard.notes_hit)
        if self.fretboard.played:
            self.fretboard.play_chord(notes)
            self.prac_label.config(text="Correct!")
            self.fretboard.notes_hit.clear()
        else:
            self.prac_label.config(text=f"Incorrect! The finger placement(s) are at {chord}", font=("Oswald", 100))
