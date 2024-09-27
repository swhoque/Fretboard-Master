import customtkinter as ctk
from tkinter import messagebox
from Fretboard import Fretboard
from Fret_Buttons import FretButton
from settings import *
from statsdb_functions import *
from statsdb_setup import *
import random
import re



ctk.set_default_color_theme("classic_theme.json")
ctk.set_appearance_mode("dark")

class Screen:
    def __init__(self, window):
        self.window = window
        self.window.title("Fret Board Master")
        self.fretboard = Fretboard()
        self.targ_note = 'A'
        self.targ_chord = 'A'
        self.targ_scale = "C Major"
        self.prac_note_label = None
        self.prac_chord_label = None
        self.prac_scale_label = None
        self.note_buttons = dict()
        self.chord_buttons = dict()
        self.scale_buttons = dict()
        self.buttons_hit = list()
        self.sf_notes = list()
        self.user = ["Guest", "None", 0, 0, 0]

        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.window.geometry(f'{self.screen_width}x{self.screen_height}+0+0')
        self.window.minsize(800, 600)

        self.prog_frame = ctk.CTkFrame(self.window)
        self.progress = ctk.CTkProgressBar(self.prog_frame, orientation="horizontal", mode="determinate", width=self.screen_width/5, height=50)
        self.progress.place(x=self.screen_width/2, y=self.screen_height/2, anchor='center')
        self.prog_frame.place(relwidth=1, relheight=1)
        self.progress.set(0)

        self.setting_frame = ctk.CTkFrame(self.window)
        self.login_frame = ctk.CTkFrame(self.window)
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

        self.conn = create_connection("USER_STATS.db")
        
        self.prog_frame.tkraise()

        self.load_screens()

    def load_screens(self):
        screens = [
            self.setup_settings_screen,
            self.setup_login_screen,
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
        self.prog_frame.destroy()

    # Setup the screens
    def setup_settings_screen(self):
        self.setting_frame.place(relwidth=1, relheight=1)

        label = ctk.CTkLabel(self.setting_frame, text="Settings")
        label.pack(pady=120)

        settings_tabs = ctk.CTkTabview(master=self.setting_frame)
        settings_tabs.add("Resolution")
        settings_tabs.add("Theme")
        settings_tabs.pack()

        resolution_label = ctk.CTkLabel(settings_tabs.tab("Resolution"), text="Resolution", font=("Playfair Display", 100))
        resolution_label.pack(pady=20)

        resolution_dropdown = ctk.CTkOptionMenu(settings_tabs.tab("Resolution"), values=["--select a resolution--", "1200x900", "1920x1080", "2560x1440"], command=lambda selected:self.window.geometry(selected))
        resolution_dropdown.pack(pady=20)

        theme_label = ctk.CTkLabel(settings_tabs.tab("Theme"), text="Theme", font=("Playfair Display", 100))
        theme_label.pack(pady=20)

        theme_dropdown = ctk.CTkOptionMenu(settings_tabs.tab("Theme"), values=["--select a theme--", "dark", "light"], command=lambda selected: ctk.set_appearance_mode(selected))
        theme_dropdown.pack(pady=20)

        back_button = ctk.CTkButton(self.setting_frame, text="Back", command= lambda:self.main_screen())
        back_button.pack()

        self.setting_frame.bind("<Escape>", lambda event: self.main_screen())

    def setup_login_screen(self):
        self.login_frame.place(relwidth=1, relheight=1)

        login_tabs = ctk.CTkTabview(self.login_frame)
        login_tabs.add("Login")
        login_tabs.add("Register")
        login_tabs.pack()

        login_frame = ctk.CTkFrame(login_tabs.tab("Login"))
        login_frame.pack()

        label = ctk.CTkLabel(login_frame, text="Login", font=("Playfair Display", 100))
        label.pack(pady=120)

        username_entry_login = ctk.CTkEntry(login_frame, placeholder_text="Username", width=200, height=40)
        username_entry_login.pack(pady=12)

        password_entry_login = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*", width=200, height=40)
        password_entry_login.pack(pady=12)

        username_entry_login.bind("<Return>", lambda event: self.login(username_entry_login.get(), password_entry_login.get()))
        password_entry_login.bind("<Return>", lambda event: self.login(username_entry_login.get(), password_entry_login.get()))

        login_button = ctk.CTkButton(login_frame, text="Login", command=lambda:self.login(username_entry_login.get(), password_entry_login.get()))
        login_button.pack(pady=12)

        back_button = ctk.CTkButton(login_frame, text="Back", command=self.main_screen)
        back_button.pack()

        register_frame = ctk.CTkFrame(login_tabs.tab("Register"))
        register_frame.pack()

        label = ctk.CTkLabel(register_frame, text="Register", font=("Playfair Display", 100))
        label.pack(pady=120)

        username_entry_reg = ctk.CTkEntry(register_frame, placeholder_text="Username", width=200, height=40)
        username_entry_reg.pack(pady=12)

        password_entry_reg = ctk.CTkEntry(register_frame, placeholder_text="Password", show="*", width=200, height=40)
        password_entry_reg.pack(pady=12)

        username_entry_reg.bind("<Return>", lambda event: self.register(username_entry_reg.get(), password_entry_reg.get()))
        password_entry_reg.bind("<Return>", lambda event: self.register(username_entry_reg.get(), password_entry_reg.get()))

        pw_label = ctk.CTkLabel(register_frame, text="Must include at least 8 characters, one uppercase letter, one lowercase letter, one number, and one special character", font=("Playfair Display", 13), wraplength=150, text_color="#E6E6FA")
        pw_label.pack()

        register_button = ctk.CTkButton(register_frame, text="Register", command=lambda:self.register(username_entry_reg.get(), password_entry_reg.get()))
        register_button.pack(pady=12)

        back_button = ctk.CTkButton(register_frame, text="Back", command=self.main_screen)
        back_button.pack()

    def setup_main_screen(self):
            self.main_frame.place(relwidth=1, relheight=1)
            
            self.user_label = ctk.CTkLabel(self.main_frame, text="Currently logged in as Guest", font=("Playfair Display", 30))
            self.user_label.place(x=self.screen_width/7, y=self.screen_height/12, anchor='center')
            label = ctk.CTkLabel(self.main_frame, text="Fret Board Master", font=("Playfair Display", 100))
            label.place(x=self.screen_width/2, y=self.screen_height/4, anchor='center')

            jam_button = ctk.CTkButton(self.main_frame, text="Jam?", width=240, height=60, command=self.jam_screen)
            practice_button = ctk.CTkButton(self.main_frame, text="Practice", width=240, height=60, command=self.practice_screen)
            learn_button = ctk.CTkButton(self.main_frame, text="Learn", width=240, height=60, command=self.learn_screen)
            login_button = ctk.CTkButton(self.main_frame, text="Login/Register", width=240, height=60, command=self.login_screen)
            self.settings_button = ctk.CTkButton(self.main_frame, text="Settings", width=240, height=60, command=self.settings_screen)
            exit_button = ctk.CTkButton(self.main_frame, text="Exit", width=240, height=60, command=self.exit_program)

            jam_button.place(x=self.screen_width/2.5-24, y=self.screen_height/1.8 + 20, anchor='center')
            practice_button.place(x=self.screen_width/2.5+256, y=self.screen_height/1.8 + 20, anchor='center')
            learn_button.place(x=self.screen_width/2.5+536, y=self.screen_height/1.8 + 20, anchor='center')
            login_button.place(x=self.screen_width/2.5+96, y=self.screen_height/1.8 + 100, anchor='center')
            self.settings_button.place(x=self.screen_width/2.5+416, y=self.screen_height/1.8 + 100, anchor='center')
            exit_button.place(x=self.screen_width/2.5+256, y=self.screen_height/1.8 + 180, anchor='center')

    def setup_jam_screen(self):
        self.jam_frame.place(relwidth=1, relheight=1)
        
        label_frame = ctk.CTkFrame(self.jam_frame, width=self.screen_width)
        label_frame.pack(pady=(20, 50))

        label = ctk.CTkLabel(label_frame, text='Jam!', font=("Playfair Display", 100))
        label.grid(row=0, column=6, columnspan=2, pady=2, padx=2)

        fretboard_frame = ctk.CTkFrame(self.jam_frame)
        fretboard_frame.pack(side="top", pady=(200, 50), ipadx=20, ipady=20)

        for data in FRET_POSITIONS.values():
            button = FretButton(fretboard_frame, text=data["col"] - 1, row=data['row'], col=data['col'], func=None)
            button.configure(fg_color='#C0C0C0', width=140, command=lambda string=data['row'], fret=data['col'] - 1: self.fretboard.play_note(string, fret))
        for data in STRING_POSITIONS.values():
            ctk.CTkLabel(fretboard_frame, text=data['note']).grid(row=data['row'], column=data['col'], padx=2, pady=2)

        back_button_frame = ctk.CTkFrame(self.jam_frame)
        back_button_frame.pack()
        submit_button = ctk.CTkButton(back_button_frame, text="Submit", width=200, height=40, command=lambda: self.fretboard.play_chord(self.fretboard.notes_hit))
        submit_button.pack(pady=(0, 20))
        back_button = ctk.CTkButton(back_button_frame, text="Back", width=200, height=40, command=lambda:(self.main_screen(), self.fretboard.play_obj.stop()))
        back_button.pack()

    def setup_practice_screen(self):
        self.practice_frame.place(relwidth=1, relheight=1)

        label = ctk.CTkLabel(self.practice_frame, text="Practice", font=("Playfair Display", 100))
        label.place(x=self.window.winfo_screenwidth()/2, y=self.window.winfo_screenheight()/4 - 50, anchor='center')

        note_button = ctk.CTkButton(self.practice_frame, text="Practice Notes", width=230, height=40, command=self.practice_note_screen)
        chord_button = ctk.CTkButton(self.practice_frame, text="Practice Chords", width=230, height=40, command=self.practice_chord_screen)
        scales_button = ctk.CTkButton(self.practice_frame, text="Practice Scales", width=230, height=40, command=self.practice_scale_screen)
        back_button = ctk.CTkButton(self.practice_frame, text="Back", width=230, height=40, command=self.main_screen)

        note_button.place(x=self.window.winfo_screenwidth()/2, y=self.window.winfo_screenheight()/2 + 20, anchor='center')
        chord_button.place(x=self.window.winfo_screenwidth()/2, y=self.window.winfo_screenheight()/2 + 80, anchor='center')
        scales_button.place(x=self.window.winfo_screenwidth()/2, y=self.window.winfo_screenheight()/2 + 140, anchor='center')
        back_button.place(x=self.window.winfo_screenwidth()/2, y=self.window.winfo_screenheight()/2 + 200, anchor='center')
    
    def setup_learn_screen(self):
        self.learn_frame.place(relwidth=1, relheight=1)

        label = ctk.CTkLabel(self.learn_frame, text="Learn", font=("Playfair Display", 100))
        label.place(x=self.screen_width/2, y=self.screen_height/4 - 50, anchor='center')

        note_button = ctk.CTkButton(self.learn_frame, text="Learn Notes", width=230, height=40, command=self.learn_note_screen)
        chord_button = ctk.CTkButton(self.learn_frame, text="Learn Chords", width=230, height=40, command=self.learn_chord_screen)
        scales_button = ctk.CTkButton(self.learn_frame, text="Learn Scales", width=230, height=40, command=self.learn_scale_screen)
        back_button = ctk.CTkButton(self.learn_frame, text="Back", width=230, height=40, command=self.main_screen)

        note_button.place(x=self.screen_width/2, y=self.screen_height/2 + 20, anchor='center')
        chord_button.place(x=self.screen_width/2, y=self.screen_height/2 + 80, anchor='center')
        scales_button.place(x=self.screen_width/2, y=self.screen_height/2 + 140, anchor='center')
        back_button.place(x=self.screen_width/2, y=self.screen_height/2 + 200, anchor='center')

    def setup_practice_note_screen(self):
        self.prac_note_frame.place(relwidth=1, relheight=1)
        screen_height = self.screen_height/9

        label_frame = ctk.CTkFrame(self.prac_note_frame)
        label_frame.pack(pady=f'{screen_height}')
        self.prac_note_label = ctk.CTkLabel(label_frame, text="Practice Notes", font=("Playfair Display", 100))
        self.prac_note_label.grid(row=0, column=6, columnspan=2, pady=2, padx=2)

        options = ["--select a note--", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
        dropdown = ctk.CTkOptionMenu(self.prac_note_frame, values=options, command=lambda selected: (self.prac_note_label.configure(text=f"Practice {selected}"), setattr(self, 'targ_note', selected), self.reset_button_colors()))
        dropdown.pack(pady=(0, 20))

        fretboard_frame = ctk.CTkFrame(self.prac_note_frame)
        fretboard_frame.pack(side="top", pady=(200, 50), ipadx=20, ipady=20)
    
        for data in FRET_POSITIONS.values():
            button = FretButton(fretboard_frame, text=data["col"] - 1, row=data['row'], col=data['col'], func=None)
            button.configure(fg_color='#C0C0C0', width=140, command=lambda button=button, string=data['row'], fret=data['col'] - 1: (self.prac_note_button_pressed(button, self.targ_note, string, fret), self.buttons_hit.append(button)))
            self.note_buttons[(data["row"], data["col"] - 1)] = button # allows modification of button color
        for data in STRING_POSITIONS.values():
            ctk.CTkLabel(fretboard_frame, text=data['note']).grid(row=data['row'], column=data['col'], padx=2, pady=2)

        back_button_frame = ctk.CTkFrame(self.prac_note_frame)
        back_button_frame.pack()
        back_button = ctk.CTkButton(back_button_frame, text="Back", width=200, height=40, command=lambda: (self.practice_screen(), self.fretboard.play_obj.stop(), self.reset_button_colors()))
        back_button.pack(pady=(0, 20))

    def setup_practice_chord_screen(self):
        self.prac_chord_frame.place(relwidth=1, relheight=1)
        screen_height = self.screen_height/9

        label_frame = ctk.CTkFrame(self.prac_chord_frame)
        label_frame.pack(pady=f'{screen_height}')
        self.prac_chord_label = ctk.CTkLabel(label_frame, text=f'Select a chord:', font=("Playfair Display", 100))
        self.prac_chord_label.grid(row=0, column=6, columnspan=2, pady=2, padx=2)

        options = ["--select a chord--", 'E', 'Em', 'A', 'Am', 'D', 'Dm', 'G', 'C']
        dropdown = ctk.CTkOptionMenu(self.prac_chord_frame, values=options, command=lambda selected: (self.prac_chord_label.configure(text=f"Practice {selected}"), setattr(self, 'targ_chord', selected), self.reset_button_colors()))
        dropdown.pack(pady=(0, 20))

        fretboard_frame = ctk.CTkFrame(self.prac_chord_frame)
        fretboard_frame.pack(side="top", pady=(200, 50), ipadx=20, ipady=20)

        # notes_hit tracks notes user hits to check against practice_chord() method
        for data in FRET_POSITIONS.values():
            button = FretButton(fretboard_frame, text=data['note'], row=data['row'], col=data['col'], func=None)
            button.configure(fg_color='#C0C0C0', width=140, command=lambda button=button, string=data['row'], fret=data['col'] - 1: (self.fretboard.play_note(string, fret), self.fretboard.notes_hit.append((string, fret)), self.buttons_hit.append(button)))
            self.chord_buttons[(data["row"], data["col"] - 1)] = button # allows modification of button color
        for data in STRING_POSITIONS.values():
            ctk.CTkLabel(fretboard_frame, text=data['note']).grid(row=data['row'], column=data['col'], padx=2, pady=2)

        back_button_frame = ctk.CTkFrame(self.prac_chord_frame)
        back_button_frame.pack()
        submit_button = ctk.CTkButton(back_button_frame, text="Submit", width=200, height=40, command= lambda: self.prac_chord_button_pressed(CHORD_MAP[self.targ_chord]))
        submit_button.pack(pady=(0, 20))
        back_button = ctk.CTkButton(back_button_frame, text="Back", width=200, height=40, command=lambda: (self.practice_screen(), self.fretboard.play_obj.stop(), self.reset_button_colors()))
        back_button.pack()

    def setup_practice_scale_screen(self):
        self.prac_scale_frame.place(relwidth=1, relheight=1)
        screen_height = self.screen_height/9

        label_frame = ctk.CTkFrame(self.prac_scale_frame)
        label_frame.pack(pady=f'{screen_height}')
        self.prac_scale_label = ctk.CTkLabel(label_frame, text=f'Select a scale:', font=("Playfair Display", 100))
        self.prac_scale_label.grid(row=0, column=6, columnspan=2, pady=2, padx=2)

        options = ["--select a scale--", "E Minor Pentatonic", "A Minor Pentatonic", "C Major"]
        dropdown = ctk.CTkOptionMenu(self.prac_scale_frame, values=options, command=lambda selected: (self.prac_scale_label.configure(text=f"Practice {selected}"), setattr(self, 'targ_scale', selected), self.reset_button_colors()))
        dropdown.pack(pady=(0, 20))

        fretboard_frame = ctk.CTkFrame(self.prac_scale_frame)
        fretboard_frame.pack(side="top", pady=(200, 50), ipadx=20, ipady=20)

        # noteshit tracks notes user hits to check against practice_scale() method
        for data in FRET_POSITIONS.values():
            button = FretButton(master=fretboard_frame, text=data['note'], row=data['row'], col=data['col'], func= None)
            button.configure(fg_color='#C0C0C0', width=140, command=lambda button=button, string=data['row'], fret=data['col'] - 1:(self.fretboard.play_note(string, fret), self.fretboard.notes_hit.append((string, fret)), self.buttons_hit.append(button)))
            self.scale_buttons[(data["row"], data["col"] - 1)] = button # allows modification of button color
        for data in STRING_POSITIONS.values():
            ctk.CTkLabel(fretboard_frame, text=data['note']).grid(row=data['row'], column=data['col'], padx=2, pady=2)

        back_button_frame = ctk.CTkFrame(self.prac_scale_frame)
        back_button_frame.pack()
        submit_button = ctk.CTkButton(back_button_frame, text="Submit", width=200, height=40, command=lambda: self.prac_scale_button_pressed(SCALES_MAP[self.targ_scale]))
        submit_button.pack(pady=(0, 20))
        back_button = ctk.CTkButton(back_button_frame, text="Back", width=200, height=40, command=lambda: (self.practice_screen(), self.fretboard.play_obj.stop(), self.reset_button_colors()))
        back_button.pack()
    
    def setup_learn_note_screen(self):
        self.learn_note_frame.place(relwidth=1, relheight=1)
        screen_height = self.screen_height/9

        label_frame = ctk.CTkFrame(self.learn_note_frame)
        label_frame.pack(pady=f'{screen_height}')
        learn_note_label = ctk.CTkLabel(label_frame, text=f'Learn the notes on the fretboard!', font=("Playfair Display", 100))
        learn_note_label.pack(pady=(0, 20))

        learning_tabs = ctk.CTkTabview(self.learn_note_frame)
        learning_tabs.pack(pady=(20, 20))

        learning_tabs.add("Why you should learn the notes")
        learning_tabs.add("Patterns")

        why_label = ctk.CTkLabel(learning_tabs.tab("Why you should learn the notes"), text= "Learning the notes on the fretboard is essential to becoming a better musician.\n"
                                                                                            "It allows you to understand the music you're playing, and it makes it easier to learn new songs.\n"
                                                                                            "It also helps you to communicate with other musicians and write your own music.",
                                                                                            justify="left", wraplength=1000)
        why_label.pack(padx=20, pady=20)
        patterns_label = ctk.CTkLabel(learning_tabs.tab("Patterns"), text="There are many patterns that can help you learn the notes on the fretboard. \n"
                                                                          "One pattern is to use the natural notes (A, B, C, D, E, F, G) as a reference point. Starting from A they follow a W-H-W-W-H-W,-\n"
                                                                          "where W is 2 frets apart and H is 1 fret apart. If you're on the B string and you want to find G, following the pattern you should move 8 frets.\n"
                                                                          "Another pattern is the 5th fret of the current string is the open string of the string below it. For example, the 5th fret of the low E string A and the 5th fret of A is D.\n"
                                                                          "For the reverse the 7th fret is where you'll find the open string. For example, the 7th fret of D is A and the 7th fret of A is E",
                                                                          justify="left", wraplength=1000)
        patterns_label.pack(padx=20, pady=20)

        back_button_frame = ctk.CTkFrame(self.learn_note_frame)
        back_button_frame.pack()
        back_button = ctk.CTkButton(back_button_frame, text="Back", width=200, height=40, command= lambda: self.learn_screen())
        back_button.pack()

    def setup_learn_chord_screen(self):
        self.learn_chord_frame.place(relwidth=1, relheight=1)
        screen_height = self.screen_height/9

        label_frame = ctk.CTkFrame(self.learn_chord_frame)
        label_frame.pack(pady=f'{screen_height}')
        learn_chord_label = ctk.CTkLabel(label_frame, text=f'Learn the chords on the fretboard!', font=("Playfair Display", 100))
        learn_chord_label.pack(pady=(0, 20))

        learning_tabs = ctk.CTkTabview(self.learn_chord_frame)
        learning_tabs.pack(pady=(20, 20))

        learning_tabs.add("Why you should learn chords")
        learning_tabs.add("Transition Tricks")
        learning_tabs.add("Learn Chord positions")

        why_label = ctk.CTkLabel(learning_tabs.tab("Why you should learn chords"), text= "-Chords are used in many songs.\n"
                                                                                         "-They help you learn the notes on the fretboard.\n"
                                                                                         "-You can improve your finger dexterity and strength",
                                                                                         justify="left")
        why_label.pack(padx=20, pady=20)
        tricks_label = ctk.CTkLabel(learning_tabs.tab("Transition Tricks"), text= "There are many tricks that can help you transition between chords.\n"
                                                                                  "-Anticipate the next chord and place your fingers such that you can keep as many finger on the same fret as possible.\n"
                                                                                  "For example, the Am to C transition, you can keep your 1st and 2nd fingers in the same positions and move your third finger to the 3rd fret of the A string.\n"
                                                                                  "-When you're practicing use a metronome to force yourself to form a different chord in a limited time frame.",
                                                                                  justify="left", wraplength=1000)
        tricks_label.pack(padx=20, pady=20)
        positions_dropdown = ctk.CTkOptionMenu(learning_tabs.tab("Learn Chord positions"), values=["--select a chord--", 'E', 'Em', 'A', 'Am', 'D', 'Dm', 'G', 'C', 'F(Partial barre)'], command=lambda selected: self.chord_position_label.configure(text=f'{CHORD_MAP[selected]}'))
        positions_dropdown.pack(pady=(20, 20))

        self.chord_position_label = ctk.CTkLabel(learning_tabs.tab("Learn Chord positions"), text="Select a chord to learn the finger positions.")
        self.chord_position_label.pack(pady=(20, 20))
        positions_help_label = ctk.CTkLabel(learning_tabs.tab("Learn Chord positions"), text="-Select a chord to learn the finger positions. Finger placement are in order from 1st finger to 4th.\n"
                                                                                        "For example, ((5, 2), (4, 2)) means 1st finger on the 5th string 2nd fret. The 2nd finger on the 4th string 2nd fret.\n"
                                                                                        "Make sure to click open strings as well starting from the first open string (if applicable).\n"
                                                                                        "For Em you'd hit ((5, 2), (4, 2), (1, 0), (2, 0), (3, 0), (6, 0))\n"
                                                                                        "-For barres like F(Barre), your first finger goes on all strings 1st fret and follow the same rules as above.\n"
                                                                                        "-For partial barres like F(Partial barre), your first finger goes on strings that have the same frets, so 1st and 2nd string. You follow the same rules as above for the rest.",
                                                                                        justify="left", wraplength=1000)
        positions_help_label.pack(padx=20, pady=20)

        back_button_frame = ctk.CTkFrame(self.learn_chord_frame)
        back_button_frame.pack()
        back_button = ctk.CTkButton(back_button_frame, text="Back", width=200, height=40, command= lambda: self.learn_screen())
        back_button.pack()

    def setup_learn_scale_screen(self):
        self.learn_scale_frame.place(relwidth=1, relheight=1)
        screen_height = self.screen_height/9

        label_frame = ctk.CTkFrame(self.learn_scale_frame)
        label_frame.pack(pady=f'{screen_height}')
        learn_scale_label = ctk.CTkLabel(label_frame, text=f'Learn the scales on the fretboard!', font=("Playfair Display", 100))
        learn_scale_label.pack(pady=(0, 20))

        learning_tabs = ctk.CTkTabview(self.learn_scale_frame)
        learning_tabs.pack(pady=(20, 20))

        learning_tabs.add("Why you should learn scales")
        learning_tabs.add("Learn Scale positions")

        why_label = ctk.CTkLabel(learning_tabs.tab("Why you should learn scales"), text= "-They help you learn the notes on the fretboard.\n"
                                                                                         "-You can improve your finger dexterity and strength\n"
                                                                                         "-Practice the chromatic scale to familiarize yourself with all the notes on the fretboard!",
                                                                                         anchor='e')
        why_label.pack(padx=20, pady=20)
        position_dropdown = ctk.CTkOptionMenu(learning_tabs.tab("Learn Scale positions"), values=["--select a scale--", "E Minor Pentatonic", "A Minor Pentatonic", "C Major"], command=lambda selected: self.scale_positions_label.configure(text=f'{SCALES_MAP[selected]}'))
        position_dropdown.pack(pady=(20, 20))
        self.scale_positions_label = ctk.CTkLabel(learning_tabs.tab("Learn Scale positions"), text="Select a scale to learn the finger positions.")
        self.scale_positions_label.pack(padx=20, pady=20)

        back_button_frame = ctk.CTkFrame(self.learn_scale_frame)
        back_button_frame.pack()
        back_button = ctk.CTkButton(back_button_frame, text="Back", width=200, height=40, command= lambda: self.learn_screen())
        back_button.pack()

    # Actually display the screens
    # Hides all other screens except the desired one
    def settings_screen(self):
        self.main_frame.place_forget()
        self.setting_frame.place(relwidth=1, relheight=1)

    def login_screen(self):
        self.main_frame.place_forget()
        self.jam_frame.place_forget()
        self.practice_frame.place_forget()
        self.learn_frame.place_forget()
        self.prac_note_frame.place_forget()
        self.prac_chord_frame.place_forget()
        self.prac_scale_frame.place_forget()
        self.learn_note_frame.place_forget()
        self.learn_chord_frame.place_forget()
        self.learn_scale_frame.place_forget()

        self.login_frame.place(relwidth=1, relheight=1)

    def main_screen(self):
        self.setting_frame.place_forget()
        self.login_frame.place_forget()
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

        self.jam_frame.place(relwidth=1, relheight=1)

    def practice_screen(self):
        self.main_frame.place_forget()
        self.prac_note_frame.place_forget()
        self.prac_chord_frame.place_forget()
        self.prac_scale_frame.place_forget()

        self.practice_frame.place(relwidth=1, relheight=1)
    
    def learn_screen(self):
        self.main_frame.place_forget()
        self.learn_note_frame.place_forget()
        self.learn_chord_frame.place_forget()
        self.learn_scale_frame.place_forget()
        
        self.learn_frame.place(relwidth=1, relheight=1)
    
    def practice_note_screen(self):
        self.practice_frame.place_forget()

        self.prac_note_label.configure(text=f'Select a note:')
        self.prac_note_frame.place(relwidth=1, relheight=1)

    def practice_chord_screen(self):
        self.practice_frame.place_forget()
        
        self.prac_chord_label.configure(text=f'Select a chord:')
        self.prac_chord_frame.place(relwidth=1, relheight=1)
    
    def practice_scale_screen(self):
        self.practice_frame.place_forget()

        self.prac_scale_label.configure(text=f'Select a scale:')
        self.prac_scale_frame.place(relwidth=1, relheight=1)
    
    def learn_note_screen(self):
        self.learn_frame.place_forget()

        self.learn_note_frame.place(relwidth=1, relheight=1)

    def learn_chord_screen(self):
        self.learn_frame.place_forget()

        self.learn_chord_frame.place(relwidth=1, relheight=1)

    def learn_scale_screen(self):
        self.learn_frame.place_forget()

        self.learn_scale_frame.place(relwidth=1, relheight=1)

    # Helper Functions
    def exit_program(self):
        update_total_time(self.conn, self.user[2])
        self.window.quit()

    def validate_password(self, password):
        """Validate the password with specific criteria."""
        if len(password) < 8:
            messagebox.showwarning("Password Error", "Password must be at least 8 characters long.")
            return False
        if not re.search(r'[A-Z]', password):
            messagebox.showwarning("Password Error", "Password must contain at least one uppercase letter.")
            return False
        if not re.search(r'[a-z]', password):
            messagebox.showwarning("Password Error", "Password must contain at least one lowercase letter.")
            return False
        if not re.search(r'[0-9]', password):
            messagebox.showwarning("Password Error", "Password must contain at least one digit.")
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            messagebox.showwarning("Password Error", "Password must contain at least one special character.")
            return False
        return True

    def login(self, username, password):
        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password")
            return
        
        try:
            user = login_user(self.conn, username, password)

            if user is None:
                messagebox.showerror("Error", "Invalid username or password")
            else:
                self.user = user
                self.user_label.configure(text=f'Currently logged in as {username}')
                self.main_screen()
        except sqlite3.OperationalError:
            messagebox.showerror("Error", "Invalid username or password")
    
    def register(self, username, password):
        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password")
            return
        
        if not self.validate_password(password):
            return
        
        initialize_database(self.conn)

        if register_user(self.conn, username, password):
            messagebox.showinfo("Success", "User registered successfully")
            self.user_label.configure(text=f'Currently logged in as {username}')
            self.main_screen()
        else:
            messagebox.showerror("Error", "Username already exists")

    # finds the matching button for the correct note
    def correct_note(self, string, note):
        self.sf_notes.append(self.note_buttons[(string, note)])

    # finds a matching button for each note in the chord
    def correct_chord(self, notes):
        for note in notes:
            self.sf_notes.append(self.chord_buttons[note])
    
    # finds a matching button for each note in the scale
    def correct_scale(self, notes):
        for note in notes:
            self.sf_notes.append(self.scale_buttons[note])

    # played(bool) is used to determine if the note/chord/scale was played correctly

    def prac_note_button_pressed(self, button, note, string, fret):
        self.fretboard.play_note(string, fret)
        self.fretboard.practice_note(note, self.fretboard.get_note_at(string, fret))
        if self.fretboard.played:
            button.configure(fg_color="green", text_color="#E6E6FA")
            self.prac_note_label.configure(text=f"{random.choice(FEEDBACK_MSG_POSITIVE)}")
        else:
            correct_fret = self.fretboard.get_note_index(string, note)[1]
            self.correct_note(string, correct_fret)
            button.configure(fg_color="red", text_color="#E6E6FA")
            self.sf_notes[-1].configure(fg_color="green", text_color="#E6E6FA") # sf_notes isn't cleared until user is finished with the note
            self.prac_note_label.configure(text=f"{random.choice(FEEDBACK_MSG_NEGATIVE)}\nIt's at fret {correct_fret}")
        self.fretboard.notes_hit.clear()

    def prac_chord_button_pressed(self, chord_pos):
        self.fretboard.practice_chord(chord_pos, self.fretboard.notes_hit)
        if self.fretboard.played:
            self.prac_chord_label.configure(text=f'{random.choice(FEEDBACK_MSG_POSITIVE)}')
            self.fretboard.play_chord(chord_pos)
            for button in self.buttons_hit:
                button.configure(fg_color="green", text_color="#E6E6FA")
        else:
            self.correct_chord(chord_pos)
            self.prac_chord_label.configure(text=f"{random.choice(FEEDBACK_MSG_NEGATIVE)}\nThe finger placement(s) are at {chord_pos}", font=("Oswald", 50))
            for button in self.buttons_hit:
                button.configure(fg_color="red", text_color="#E6E6FA")
            for button in self.sf_notes:
                button.configure(fg_color="green", text_color="#E6E6FA")
        self.fretboard.notes_hit.clear()

    def prac_scale_button_pressed(self, scale_pos):
        self.fretboard.practice_scale(scale_pos, self.fretboard.notes_hit)
        if self.fretboard.played:
            self.prac_scale_label.configure(text=f'{random.choice(FEEDBACK_MSG_POSITIVE)}')
            for button in self.buttons_hit:
                button.configure(fg_color="green", text_color="#E6E6FA")
        else:
            self.correct_scale(scale_pos)
            self.prac_scale_label.configure(text=f"{random.choice(FEEDBACK_MSG_NEGATIVE)}\nThe finger placement(s) are at {scale_pos}", font=("Oswald", 30))
            for button in self.buttons_hit:
                button.configure(fg_color="red", text_color="#E6E6FA")
            for button in self.sf_notes:
                button.configure(fg_color="green", text_color="#E6E6FA")
        self.fretboard.notes_hit.clear()

    def reset_button_colors(self):
        all_buttons = set(self.buttons_hit + self.sf_notes)
        for button in all_buttons:
            button.configure(fg_color='#C0C0C0', text_color="#626D71")
        self.buttons_hit.clear()
        self.sf_notes.clear()
