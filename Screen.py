import customtkinter as ctk
from Fretboard import Fretboard
from Fret_Buttons import FretButton
from settings import *



ctk.set_default_color_theme("classic_theme.json")

class Screen:
    def __init__(self, window):
        self.window = window
        self.window.title("Fretboard Master")
        self.fretboard = Fretboard()
        self.user_note = None
        self.targ_chord = None
        self.targ_scale = None
        self.prac_note_label = None
        self.prac_chord_label = None
        self.prac_scale_label = None
        self.learn_note_label = None
        self.buttons = list()

        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.window.geometry(f'{self.screen_width}x{self.screen_height}+0+0')
        self.window.minsize(800, 600)
        self.window.maxsize(self.screen_width, self.screen_height)

        self.prog_frame = ctk.CTkFrame(self.window)
        self.progress = ctk.CTkProgressBar(self.prog_frame, orientation="horizontal", mode="determinate", width=self.screen_width/5, height=50)
        self.progress.place(x=self.screen_width/2, y=self.screen_height/2, anchor='center')
        self.prog_frame.place(relwidth=1, relheight=1)
        self.progress.set(0)

        self.main_frame = ctk.CTkFrame(self.window)
        self.jam_frame = ctk.CTkFrame(self.window)
        self.practice_frame = ctk.CTkFrame(self.window)
        self.learn_frame = ctk.CTkFrame(self.window)
        self.prac_note_frame = ctk.CTkFrame(self.window)
        self.prac_chord_frame = ctk.CTkFrame(self.window)
        self.prac_scale_frame = ctk.CTkFrame(self.window)
        self.learn_note_frame = ctk.CTkFrame(self.window)
        self.learn_chord_frame = ctk.CTkFrame(self.window)
        self.learn_scale_frame = ctk.CTkFrame(self.window)

        self.prog_frame.tkraise()
        self.load_screens()

    def load_screens(self):
        screens = [
            self.setup_main_screen,
            self.setup_jam_screen,
            self.setup_practice_screen,
            self.setup_learn_screen,
            self.setup_practice_note_screen,
            self.setup_practice_chord_screen,
            self.setup_practice_scale_screen,
            self.setup_learn_note_screen,
            self.setup_learn_chord_screen,
            self.setup_learn_scale_screen
        ]

        total_screens = len(screens)

        for i, setup_screen in enumerate(screens):
            setup_screen()
            self.progress.set((i + 1) / total_screens)
        self.prog_frame.place_forget()

    # Setup the screens
    def setup_main_screen(self):
            self.main_frame.place(relwidth=1, relheight=1)
            label = ctk.CTkLabel(self.main_frame, text="Fretboard Master", font=("Oswald", 100))
            label.place(x=self.screen_width/2, y=self.screen_height/4, anchor='center')

            jam_button = ctk.CTkButton(self.main_frame, text="Jam?", command=self.jam_screen)
            practice_button = ctk.CTkButton(self.main_frame, text="Practice", command=self.practice_screen)
            learn_button = ctk.CTkButton(self.main_frame, text="Learn", command=self.learn_screen)
            exit_button = ctk.CTkButton(self.main_frame, text="Exit", command=self.window.quit)

            jam_button.place(x=self.screen_width/2, y=self.screen_height/2 + 20, anchor='center')
            practice_button.place(x=self.screen_width/2, y=self.screen_height/2 + 60, anchor='center')
            learn_button.place(x=self.screen_width/2, y=self.screen_height/2 + 100, anchor='center')
            exit_button.place(x=self.screen_width/2, y=self.screen_height/2 + 140, anchor='center')

    def setup_jam_screen(self):
        self.jam_frame.place(relwidth=1, relheight=1)
        
        label_frame = ctk.CTkFrame(self.jam_frame, width=self.screen_width)
        label_frame.pack(pady=(20, 50))
        label = ctk.CTkLabel(label_frame, text='Jam!', font=("Oswald", 100))
        label.grid(row=0, column=6, columnspan=2, pady=2, padx=2)

        fretboard_frame = ctk.CTkFrame(self.jam_frame)
        fretboard_frame.pack(side="top", pady=(200, 50), ipadx=20, ipady=20)

        for data in FRET_POSITIONS.values():
            button = FretButton(fretboard_frame, text=data["col"] - 1, row=data['row'], col=data['col'], func=None)
            button.configure(fg_color='#C0C0C0', text_color="black", command=lambda string=data['row'], fret=data['col'] - 1: self.fretboard.play_note(string, fret))
        for data in STRING_POSITIONS.values():
            ctk.CTkLabel(fretboard_frame, text=data['note']).grid(row=data['row'], column=data['col'], padx=2, pady=2)

        back_button_frame = ctk.CTkFrame(self.jam_frame)
        back_button_frame.pack()
        submit_button = ctk.CTkButton(back_button_frame, text="Submit", command=lambda: self.fretboard.play_chord(self.fretboard.notes_hit), width=20)
        submit_button.pack(pady=(0, 20))
        back_button = ctk.CTkButton(back_button_frame, text="Back", command=lambda:(self.main_screen(), self.fretboard.play_obj.stop()), width=20)
        back_button.pack()

    def setup_practice_screen(self):
        self.practice_frame.place(relwidth=1, relheight=1)

        label = ctk.CTkLabel(self.practice_frame, text="Practice", font=("Oswald", 24))
        label.place(x=self.window.winfo_screenwidth()/2, y=self.window.winfo_screenheight()/4 - 50, anchor='center')

        note_button = ctk.CTkButton(self.practice_frame, text="Practice Notes", command=self.practice_note_screen, width=20)
        chord_button = ctk.CTkButton(self.practice_frame, text="Practice Chords", command=self.practice_chord_screen, width=20)
        scales_button = ctk.CTkButton(self.practice_frame, text="Practice Scales", command=self.practice_scale_screen, width=20)
        back_button = ctk.CTkButton(self.practice_frame, text="Back", command=self.main_screen, width=20)

        note_button.place(x=self.window.winfo_screenwidth()/2, y=self.window.winfo_screenheight()/2 + 20, anchor='center')
        chord_button.place(x=self.window.winfo_screenwidth()/2, y=self.window.winfo_screenheight()/2 + 60, anchor='center')
        scales_button.place(x=self.window.winfo_screenwidth()/2, y=self.window.winfo_screenheight()/2 + 100, anchor='center')
        back_button.place(x=self.window.winfo_screenwidth()/2, y=self.window.winfo_screenheight()/2 + 140, anchor='center')
    
    def setup_learn_screen(self):
        self.learn_frame.place(relwidth=1, relheight=1)

        label = ctk.CTkLabel(self.learn_frame, text="Learn", font=("Oswald", 24))
        label.place(x=self.screen_width/2, y=self.screen_height/4 - 50, anchor='center')

        note_button = ctk.CTkButton(self.learn_frame, text="Learn Notes", command=self.learn_note_screen, width=20)
        chord_button = ctk.CTkButton(self.learn_frame, text="Learn Chords", command=self.learn_chord_screen, width=20)
        scales_button = ctk.CTkButton(self.learn_frame, text="Learn Scales", command=self.learn_scale_screen, width=20)
        back_button = ctk.CTkButton(self.learn_frame, text="Back", command=self.main_screen, width=20)

        note_button.place(x=self.screen_width/2, y=self.screen_height/2 + 20, anchor='center')
        chord_button.place(x=self.screen_width/2, y=self.screen_height/2 + 60, anchor='center')
        scales_button.place(x=self.screen_width/2, y=self.screen_height/2 + 100, anchor='center')
        back_button.place(x=self.screen_width/2, y=self.screen_height/2 + 140, anchor='center')
    
    def setup_practice_note_screen(self):
        self.prac_note_frame.place(relwidth=1, relheight=1)
        screen_height = self.screen_height/9

        label_frame = ctk.CTkFrame(self.prac_note_frame)
        label_frame.pack(pady=f'{screen_height}')
        self.prac_note_label = ctk.CTkLabel(label_frame)
        self.prac_note_label.grid(row=0, column=6, columnspan=2, pady=2, padx=2)

        options = ["--select a note--", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
        dropdown = ctk.CTkOptionMenu(self.prac_note_frame, values=options, command=lambda selected: (self.prac_note_label.configure(text=f"Practice {selected}"), setattr(self, 'user_note', selected), self.reset_button_colors()))
        dropdown.pack(pady=(0, 20))

        fretboard_frame = ctk.CTkFrame(self.prac_note_frame)
        fretboard_frame.pack(side="top", pady=(200, 50), ipadx=20, ipady=20)
    
        for data in FRET_POSITIONS.values():
            button = FretButton(fretboard_frame, text=data["col"] - 1, row=data['row'], col=data['col'], func=None)
            button.configure(fg_color='#C0C0C0', text_color="black", command=lambda button=button, string=data['row'], fret=data['col'] - 1: self.prac_note_button_pressed(button, self.user_note, string, fret))
            self.buttons.append(button)
        for data in STRING_POSITIONS.values():
            ctk.CTkLabel(fretboard_frame, text=data['note']).grid(row=data['row'], column=data['col'], padx=2, pady=2)

        back_button_frame = ctk.CTkFrame(self.prac_note_frame)
        back_button_frame.pack()
        back_button = ctk.CTkButton(back_button_frame, text="Back", command= lambda: (self.practice_screen(), self.fretboard.play_obj.stop()), width=20)
        back_button.pack(pady=(0, 20))

    def setup_practice_chord_screen(self):
        self.prac_chord_frame.place(relwidth=1, relheight=1)
        screen_height = self.screen_height/9

        label_frame = ctk.CTkFrame(self.prac_chord_frame)
        label_frame.pack(pady=f'{screen_height}')
        self.prac_chord_label = ctk.CTkLabel(label_frame, text=f'Select a chord:', font=("Oswald", 100))
        self.prac_chord_label.grid(row=0, column=6, columnspan=2, pady=2, padx=2)

        options = ["--select a chord--", 'E', 'Em', 'A', 'Am', 'D', 'Dm', 'G', 'C']
        dropdown = ctk.CTkOptionMenu(self.prac_chord_frame, values=options, command=lambda selected: (self.prac_chord_label.configure(text=f"Practice {selected}"), setattr(self, 'targ_chord', selected)))
        dropdown.pack(pady=(0, 20))

        fretboard_frame = ctk.CTkFrame(self.prac_chord_frame)
        fretboard_frame.pack(side="top", pady=(200, 50), ipadx=20, ipady=20)

        for data in FRET_POSITIONS.values():
            button = FretButton(fretboard_frame, text=data['note'], row=data['row'], col=data['col'], func=None)
            button.configure(fg_color='#C0C0C0', text_color="black", command=lambda string=data['row'], fret=data['col'] - 1: (self.fretboard.play_note(string, fret), self.fretboard.notes_hit.append((string, fret))))
        for data in STRING_POSITIONS.values():
            ctk.CTkLabel(fretboard_frame, text=data['note']).grid(row=data['row'], column=data['col'], padx=2, pady=2)

        back_button_frame = ctk.CTkFrame(self.prac_chord_frame)
        back_button_frame.pack()
        submit_button = ctk.CTkButton(back_button_frame, text="Submit", command= lambda: self.prac_chord_button_pressed(CHORD_MAP[self.targ_chord]), width=20)
        submit_button.pack(pady=(0, 20))
        back_button = ctk.CTkButton(back_button_frame, text="Back", command= lambda: (self.practice_screen(), self.fretboard.play_obj.stop()), width=20)
        back_button.pack()

    def setup_practice_scale_screen(self):
        self.prac_scale_frame.place(relwidth=1, relheight=1)
        screen_height = self.screen_height/9

        label_frame = ctk.CTkFrame(self.prac_scale_frame)
        label_frame.pack(pady=f'{screen_height}')
        self.prac_scale_label = ctk.CTkLabel(label_frame, text=f'Select a scale:', font=("Oswald", 100))
        self.prac_scale_label.grid(row=0, column=6, columnspan=2, pady=2, padx=2)

        options = ["--select a scale--", "E Minor Pentatonic", "A Minor Pentatonic", "C Major"]
        dropdown = ctk.CTkOptionMenu(self.prac_scale_frame, values=options, command=lambda selected: (self.prac_scale_label.configure(text=f"Practice {selected}"), setattr(self, 'targ_scale', selected)))
        dropdown.pack(pady=(0, 20))

        fretboard_frame = ctk.CTkFrame(self.prac_scale_frame)
        fretboard_frame.pack(side="top", pady=(200, 50), ipadx=20, ipady=20)

        for data in FRET_POSITIONS.values():
            button = FretButton(fretboard_frame, text=data['note'], row=data['row'], col=data['col'], func= None)
            button.configure(fg_color='#C0C0C0', text_color="black", command=lambda string=data['row'], fret=data['col'] - 1:(self.fretboard.play_note(string, fret), self.fretboard.notes_hit.append((string, fret))))
        for data in STRING_POSITIONS.values():
            ctk.CTkLabel(fretboard_frame, text=data['note']).grid(row=data['row'], column=data['col'], padx=2, pady=2)

        back_button_frame = ctk.CTkFrame(self.prac_scale_frame)
        back_button_frame.pack()
        submit_button = ctk.CTkButton(back_button_frame, text="Submit", command= lambda: self.prac_scale_button_pressed(SCALES_MAP[self.targ_scale]), width=20)
        submit_button.pack(pady=(0, 20))
        back_button = ctk.CTkButton(back_button_frame, text="Back", command= lambda: (self.practice_screen(), self.fretboard.play_obj.stop()), width=20)
        back_button.pack()
    
    def setup_learn_note_screen(self):
        self.learn_note_frame.place(relwidth=1, relheight=1)
        screen_height = self.screen_height/9

        label_frame = ctk.CTkFrame(self.learn_note_frame)
        label_frame.pack(pady=f'{screen_height}')
        self.learn_note_label = ctk.CTkLabel(label_frame, text=f'Learn the notes on the fretboard!', font=("Oswald", 100))
        self.learn_note_label.pack(pady=(0, 20))

        learning_tabs = ctk.CTkTabview(self.learn_note_frame)
        learning_tabs.pack(pady=(20, 20))

        learning_tabs.add("Why you should learn the notes")
        learning_tabs.add("Patterns")

        why_label = ctk.CTkLabel(learning_tabs.tab("Why you should learn the notes"), text= "Learning the notes on the fretboard is essential to becoming a better musician.\n"
                                                                                            "It allows you to understand the music you're playing, and it makes it easier to learn new songs.\n"
                                                                                            "It also helps you to communicate with other musicians and write your own music.")
        why_label.pack(padx=20, pady=20)
        patterns_label = ctk.CTkLabel(learning_tabs.tab("Patterns"), text="There are many patterns that can help you learn the notes on the fretboard. \n"
                                                                          "One pattern is to use the natural notes (A, B, C, D, E, F, G) as a reference point. Starting from A they follow a W-H-W-W-H-W,-\n"
                                                                          "where W is 2 frets apart and H is 1 fret apart. If you're on the B string and you want to find G, following the pattern you should move 8 frets.\n"
                                                                          "Another pattern is the 5th fret of the current string is the open string of the string below it. For example, the 5th fret of the low E string A and the 5th fret of A is D"
                                                                          "For the reverse the 7th fret is where you'll find the open string. For example, the 7th fret of D is A and the 7th fret of A is E")
        patterns_label.pack(padx=20, pady=20)

        back_button_frame = ctk.CTkFrame(self.learn_note_frame)
        back_button_frame.pack()
        back_button = ctk.CTkButton(back_button_frame, text="Back", command= lambda: self.learn_screen(), width=20)
        back_button.pack()


    def setup_learn_chord_screen(self):
        self.learn_chord_frame.place(relwidth=1, relheight=1)
        screen_height = self.screen_height/9

        label_frame = ctk.CTkFrame(self.learn_chord_frame)
        label_frame.pack(pady=f'{screen_height}')
        self.learn_chord_label = ctk.CTkLabel(label_frame, text=f'Learn the chords on the fretboard!', font=("Oswald", 100))
        self.learn_chord_label.pack(pady=(0, 20))

        learning_tabs = ctk.CTkTabview(self.learn_chord_frame)
        learning_tabs.pack(pady=(20, 20))

        learning_tabs.add("Why you should learn chords")
        learning_tabs.add("Transition Tricks")
        learning_tabs.add("Learn Chord positions")

        why_label = ctk.CTkLabel(learning_tabs.tab("Why you should learn chords"), text= "-Chords are used in many songs.\n"
                                                                                         "-They help you learn the notes on the fretboard.\n"
                                                                                         "-You can improve your finger dexterity and strength")
        why_label.pack(padx=20, pady=20)
        tricks_label = ctk.CTkLabel(learning_tabs.tab("Transition Tricks"), text= "There are many tricks that can help you transition between chords.\n"
                                                                                  "-Anticipate the next chord and place your fingers such that you can keep as many finger on the same fret as possible.\n"
                                                                                  "For example, the Am to C transition, you can keep your 1st and 2nd fingers in the same positions and move your third finger to the 3rd fret of the A string.\n"
                                                                                  "-When you're practicing use a metronome to force yourself to form a different chord in a limited time frame.")
        tricks_label.pack(padx=20, pady=20)
        positions_dropdown = ctk.CTkOptionMenu(learning_tabs.tab("Learn Chord positions"), values=["--select a chord--", 'E', 'Em', 'A', 'Am', 'D', 'Dm', 'G', 'C', 'F(Partial barre)'], command=lambda selected: self.learn_chord_label.configure(text=f'{CHORD_MAP[selected]}'))
        positions_dropdown.pack(pady=(20, 20))
        positions_label = ctk.CTkLabel(learning_tabs.tab("Learn Chord positions"), text="-Select a chord to learn the finger positions. Finger placement are in order from 1st finger to 4th.\n"
                                                                                        "For example, ((5, 2), (4, 2)) means 1st finger on the 5th string 2nd fret. The 2nd finger on the 4th string 2nd fret.\n"
                                                                                        "-For barres like F(Barre), your first finger goes on all strings 1st fret and follow the same rules as above.\n"
                                                                                        "-For partial barres like F(Partial barre), your first finger goes on strings that have the same frets, so 1st and 2nd string. You follow the same rules as above for the rest.")
        positions_label.pack(padx=20, pady=20)

        back_button_frame = ctk.CTkFrame(self.learn_chord_frame)
        back_button_frame.pack()
        back_button = ctk.CTkButton(back_button_frame, text="Back", command= lambda: self.learn_screen(), width=20)
        back_button.pack()

    def setup_learn_scale_screen(self):
        self.learn_scale_frame.place(relwidth=1, relheight=1)
        screen_height = self.screen_height/9

        label_frame = ctk.CTkFrame(self.learn_scale_frame)
        label_frame.pack(pady=f'{screen_height}')
        self.learn_scale_label = ctk.CTkLabel(label_frame, text=f'Learn the scales on the fretboard!', font=("Oswald", 100))
        self.learn_scale_label.pack(pady=(0, 20))

        learning_tabs = ctk.CTkTabview(self.learn_scale_frame)
        learning_tabs.pack(pady=(20, 20))

        learning_tabs.add("Why you should learn scales")
        learning_tabs.add("Learn Scale positions")

        why_label = ctk.CTkLabel(learning_tabs.tab("Why you should learn scales"), text= "-They help you learn the notes on the fretboard.\n"
                                                                                         "-You can improve your finger dexterity and strength\n"
                                                                                         "-Practice the chromatic scale to familiarize yourself with all the notes on the fretboard!")
        why_label.pack(padx=20, pady=20)
        position_dropdown = ctk.CTkOptionMenu(learning_tabs.tab("Learn Scale positions"), values=["--select a scale--", "E Minor Pentatonic", "A Minor Pentatonic", "C Major"], command=lambda selected: self.learn_scale_label.configure(text=f'{SCALES_MAP[selected]}', font=("Oswald", 30)))
        position_dropdown.pack(pady=(20, 20))
        positions_label = ctk.CTkLabel(learning_tabs.tab("Learn Scale positions"), text="Select a scale to learn the finger positions.")
        positions_label.pack(padx=20, pady=20)

        back_button_frame = ctk.CTkFrame(self.learn_scale_frame)
        back_button_frame.pack()
        back_button = ctk.CTkButton(back_button_frame, text="Back", command= lambda: self.learn_screen(), width=20)
        back_button.pack()

    # Actually display the screens
    def main_screen(self):
        self.jam_frame.place_forget()
        self.practice_frame.place_forget()
        self.learn_frame.place_forget()
        self.prac_note_frame.place_forget()
        self.prac_chord_frame.place_forget()
        self.prac_scale_frame.place_forget()
        self.learn_note_frame.place_forget()
        self.learn_chord_frame.place_forget()
        self.learn_scale_frame.place_forget()

        self.main_frame.place(relwidth=1, relheight=1)

    def jam_screen(self):
        self.main_frame.place_forget()
        self.practice_frame.place_forget()
        self.learn_frame.place_forget()
        self.prac_note_frame.place_forget()
        self.prac_chord_frame.place_forget()
        self.prac_scale_frame.place_forget()
        self.learn_note_frame.place_forget()
        self.learn_chord_frame.place_forget()
        self.learn_scale_frame.place_forget()

        self.jam_frame.place(relwidth=1, relheight=1)

    def practice_screen(self):
        self.main_frame.place_forget()
        self.jam_frame.place_forget()
        self.learn_frame.place_forget()
        self.prac_note_frame.place_forget()
        self.prac_chord_frame.place_forget()
        self.prac_scale_frame.place_forget()
        self.learn_note_frame.place_forget()
        self.learn_chord_frame.place_forget()
        self.learn_scale_frame.place_forget()

        self.practice_frame.place(relwidth=1, relheight=1)
    
    def learn_screen(self):
        self.main_frame.place_forget()
        self.jam_frame.place_forget()
        self.practice_frame.place_forget()
        self.prac_note_frame.place_forget()
        self.prac_chord_frame.place_forget()
        self.prac_scale_frame.place_forget()
        self.learn_note_frame.place_forget()
        self.learn_chord_frame.place_forget()
        self.learn_scale_frame.place_forget()
        
        self.learn_frame.place(relwidth=1, relheight=1)
    
    def practice_note_screen(self):
        self.main_frame.place_forget()
        self.jam_frame.place_forget()
        self.learn_frame.place_forget()
        self.practice_frame.place_forget()
        self.prac_chord_frame.place_forget()
        self.prac_scale_frame.place_forget()
        self.learn_note_frame.place_forget()
        self.learn_chord_frame.place_forget()
        self.learn_scale_frame.place_forget()

        self.prac_note_label.configure(text=f'Select a note:', font=("Oswald", 100))
        self.prac_note_frame.place(relwidth=1, relheight=1)

    def practice_chord_screen(self):
        self.main_frame.place_forget()
        self.jam_frame.place_forget()
        self.learn_frame.place_forget()
        self.practice_frame.place_forget()
        self.prac_note_frame.place_forget()
        self.prac_scale_frame.place_forget()
        self.learn_note_frame.place_forget()
        self.learn_chord_frame.place_forget()
        self.learn_scale_frame.place_forget()
        
        self.prac_chord_label.configure(text=f'Select a chord:', font=("Oswald", 100))
        self.prac_chord_frame.place(relwidth=1, relheight=1)
    
    def practice_scale_screen(self):
        self.main_frame.place_forget()
        self.jam_frame.place_forget()
        self.learn_frame.place_forget()
        self.practice_frame.place_forget()
        self.prac_note_frame.place_forget()
        self.prac_chord_frame.place_forget()
        self.learn_note_frame.place_forget()
        self.learn_chord_frame.place_forget()
        self.learn_scale_frame.place_forget()

        self.prac_scale_label.configure(text=f'Select a scale:', font=("Oswald", 100))
        self.prac_scale_frame.place(relwidth=1, relheight=1)
    
    def learn_note_screen(self):
        self.main_frame.place_forget()
        self.jam_frame.place_forget()
        self.practice_frame.place_forget()
        self.prac_note_frame.place_forget()
        self.prac_chord_frame.place_forget()
        self.prac_scale_frame.place_forget()
        self.learn_frame.place_forget()
        self.learn_chord_frame.place_forget()
        self.learn_scale_frame.place_forget()

        self.learn_note_frame.place(relwidth=1, relheight=1)

    def learn_chord_screen(self):
        self.main_frame.place_forget()
        self.jam_frame.place_forget()
        self.practice_frame.place_forget()
        self.prac_note_frame.place_forget()
        self.prac_chord_frame.place_forget()
        self.prac_scale_frame.place_forget()
        self.learn_frame.place_forget()
        self.learn_note_frame.place_forget()
        self.learn_scale_frame.place_forget()

        self.learn_chord_frame.place(relwidth=1, relheight=1)

    def learn_scale_screen(self):
        self.main_frame.place_forget()
        self.jam_frame.place_forget()
        self.practice_frame.place_forget()
        self.prac_note_frame.place_forget()
        self.prac_chord_frame.place_forget()
        self.prac_scale_frame.place_forget()
        self.learn_frame.place_forget()
        self.learn_note_frame.place_forget()
        self.learn_chord_frame.place_forget()

        self.learn_scale_frame.place(relwidth=1, relheight=1)

    # Helper Functions
    def prac_note_button_pressed(self, button, note, string, fret):
        self.fretboard.play_note(string, fret)
        self.fretboard.practice_note(note, self.fretboard.get_note_at(string, fret))
        if self.fretboard.played:
            button.configure(fg_color="green")
            self.prac_note_label.configure(text="Correct!")
        else:
            button.configure(fg_color="red")
            correct_fret = self.fretboard.get_note_index(string, note)[1]
            self.prac_note_label.configure(text=f"Incorrect! It's at fret {correct_fret}")

    def prac_chord_button_pressed(self, chord):
        self.fretboard.practice_chord(chord, self.fretboard.notes_hit)
        if self.fretboard.played:
            self.prac_chord_label.configure(text="Correct!")
            self.fretboard.play_chord(chord)
            self.fretboard.notes_hit.clear()
        else:
            self.prac_chord_label.configure(text=f"Incorrect! The finger placement(s) are at {chord}", font=("Oswald", 50))
            self.fretboard.notes_hit.clear()

    def prac_scale_button_pressed(self, scale):
        self.fretboard.practice_scale(scale, self.fretboard.notes_hit)
        if self.fretboard.played:
            self.prac_scale_label.configure(text="Correct!")
            self.fretboard.notes_hit.clear()
        else:
            self.prac_scale_label.configure(text=f"Incorrect! The finger placement(s) are at {scale}", font=("Oswald", 30))
            self.fretboard.notes_hit.clear()

    def reset_button_colors(self):
        for button in self.buttons:
            button.configure(fg_color="#C0C0C0")