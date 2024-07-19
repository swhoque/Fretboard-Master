import simpleaudio as sa
import tkinter as tk
from tkinter import ttk

class Fretboard:
    def __init__(self):
        self.num_strings = 6
        self.num_frets = 12
        self.wav_obj = sa.WaveObject
        self.play_obj = sa.PlayObject
        self.played = False
        self.fretboard = ["This is the fretboard"]
        self.fretboard.append(["e_open", 'F_e', 'F#_e', 'G_e', 'G#_e', 'A_e', 'A#_e', 'B_e', 'C_e', 'C#_e', 'D_e', 'D#_e', 'E_12'])
        self.fretboard.append(['B_open', 'C_B', 'C#_B', 'D_B', 'D#_B', 'E_B', 'F_B', 'F#_B', 'G_B', 'G#_B', 'A_B', 'A#_B', 'B_12'])
        self.fretboard.append(['G_open', 'G#_G', 'A_G', 'A#_G', 'B_G', 'C_G', 'C#_G', 'D_G', 'D#_G', 'E_G', 'F_G', 'F#_G', 'G_12'])
        self.fretboard.append(['D_open', 'D#_D', 'E_D', 'F_D', 'F#_D', 'G_D', 'G#_D', 'A_D', 'A#_D', 'B_D', 'C_D', 'C#_D', 'D_12'])
        self.fretboard.append(['A_open', 'A#_A', 'B_A', 'C_A', 'C#_A', 'D_A', 'D#_A', 'E_A', 'F_A', 'F#_A', 'G_A', 'G#_A', 'A_12'])
        self.fretboard.append(["E6_open", 'F_E', 'F#_E', 'G_E', 'G#_E', 'A_E', 'A#_E', 'B_E', 'C_E', 'C#_E', 'D_E', 'D#_E', 'E_12'])
    
    #Getters
    def get_fretboard(self):
        return self.fretboard

    def get_note_at(self, string, fret):
        if self.fretboard[string][fret][1] == "#":
            return self.fretboard[string][fret][:2]
        return self.fretboard[string][fret][0]

    def get_note_index(self, string, note):
        for j in range(0, 13):
            if self.get_note_at(string, j) == note:
                return [string, j]
        return None
    
    def get_string_index(self, string):
        for j in range(1, 7):
            if self.get_note_at(j, 0) == string:
                return [j]
        return None

    def get_fret_distance(self, string,  note1, note2):
        index1 = self.get_note_index(string, note1)
        index2 = self.get_note_index(string, note2)
        return abs(index1[1] - index2[1])
    
    def get_string_distance(self, string1, string2):
        index1 = self.get_string_index(string1)
        index2 = self.get_string_index(string2)
        return abs(index1[0] - index2[0])
    
    #Helpers
    def play_note(self, string, fret):
        note = self.fretboard[string][fret]
        self.play_obj = self.wav_obj.from_wave_file("Assets/" + note + ".wav").play()

    def practice_note(self, targ_note, note):
        if targ_note == note:
            self.played = True
        else: self.played = False

class Screen:
    def __init__(self):
        self.fretboard = Fretboard()
        self.window = tk.Tk()
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.style = ttk.Style()

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
        screen_height = self.screen_height/3

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
                button = ttk.Button(fretboard_frame, text=f'{self.fretboard.get_note_at(string, fret)}', width=7, command=lambda s=string, f=fret: self.fretboard.play_note(s, f), style="String.TButton")
                button.grid(row=string + 1, column=fret + 1, padx=2, pady=2)
                row_buttons.append(button)
            buttons.append(row_buttons)

        back_button_frame = ttk.Frame(main_frame, padding="-300")
        back_button_frame.pack()
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
        chord_button = ttk.Button(self.window, text="Practice Chords", command=lambda: self.practice_screen(), width=20)
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
        screen_height = self.screen_height/3

        fretboard_frame = ttk.Frame(main_frame, padding=f'{screen_height}')
        fretboard_frame.pack()
    
        for i in range(self.fretboard.num_frets + 2):
            fretboard_frame.columnconfigure(i, weight=1)
        for i in range(self.fretboard.num_strings + 2):
            fretboard_frame.rowconfigure(i, weight=1)

        self.prac_label = ttk.Label(fretboard_frame, text=f"Find {note}", font=("Oswald", 24))
        self.prac_label.grid(row=0, column=6, columnspan=self.fretboard.num_frets+2, pady=2, padx=2, sticky='ew')

        for fret in range(self.fretboard.num_frets + 1):
            ttk.Label(fretboard_frame, text=str(fret)).grid(row=1, column=fret + 1, padx=2, pady=2)

        buttons = []
        for string in range(1, self.fretboard.num_strings+1):
            ttk.Label(fretboard_frame, text=["KEK", "e", "B", "G", "D", "A", "E"][string]).grid(row=string + 1, column=0, padx=2, pady=2)
            
            row_buttons = []
            for fret in range(self.fretboard.num_frets + 1):
                button = ttk.Button(fretboard_frame, text=f'{fret}', width=7, style="String.TButton")
                button.configure(command=lambda b=button, s=string, f=fret: self.prac_button_pressed(b, note, s, f))
                button.grid(row=string + 1, column=fret + 1, padx=2, pady=2)
                row_buttons.append(button)
            buttons.append(row_buttons)

        back_button_frame = ttk.Frame(main_frame, padding="-300")
        back_button_frame.pack()
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
    
    def prac_button_pressed(self, button, note, string, fret):
        self.fretboard.play_note(string, fret)
        self.fretboard.practice_note(note, self.fretboard.get_note_at(string, fret))
        if self.fretboard.played:
            button.configure(style="Correct.TButton")
            self.prac_label.config(text="Correct!")
        else:
            button.configure(style="Incorrect.TButton")
            correct_fret = self.fretboard.get_note_index(string, note)[1]
            self.prac_label.config(text=f"Incorrect! It's at fret {correct_fret}")


if __name__ == "__main__":
    main_screen = Screen()

    main_screen.configure_styles()
    main_screen.main_screen()
    
    main_screen.window.mainloop()
