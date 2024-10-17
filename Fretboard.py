import simpleaudio as sa
from platform import platform
from settings import CHORD_MAP
from settings import SCALES_MAP

class Fretboard:
    def __init__(self):
        self.notes_hit = list()
        self.wav_obj = sa.WaveObject
        self.play_obj = sa.PlayObject
        self.played = False
        self.fretboard = ["This is the fretboard"]
        self.fretboard.append(["E_open", 'F_e', 'F#_e', 'G_e', 'G#_e', 'A_e', 'A#_e', 'B_e', 'C_e', 'C#_e', 'D_e', 'D#_e', 'E_12'])
        self.fretboard.append(['B_open', 'C_B', 'C#_B', 'D_B', 'D#_B', 'E_B', 'F_B', 'F#_B', 'G_B', 'G#_B', 'A_B', 'A#_B', 'B_12'])
        self.fretboard.append(['G_open', 'G#_G', 'A_G', 'A#_G', 'B_G', 'C_G', 'C#_G', 'D_G', 'D#_G', 'E_G', 'F_G', 'F#_G', 'G_12'])
        self.fretboard.append(['D_open', 'D#_D', 'E_D', 'F_D', 'F#_D', 'G_D', 'G#_D', 'A_D', 'A#_D', 'B_D', 'C_D', 'C#_D', 'D_12'])
        self.fretboard.append(['A_open', 'A#_A', 'B_A', 'C_A', 'C#_A', 'D_A', 'D#_A', 'E_A', 'F_A', 'F#_A', 'G_A', 'G#_A', 'A_12'])
        self.fretboard.append(["E6_open", 'F_E', 'F#_E', 'G_E', 'G#_E', 'A_E', 'A#_E', 'B_E', 'C_E', 'C#_E', 'D_E', 'D#_E', 'E6_12'])
        self.chord_map = CHORD_MAP
        self.scale_map = SCALES_MAP
    
    #Getters
    def get_fretboard(self):
        return self.fretboard

    def get_note_at(self, string, fret):
        if self.fretboard[string][fret][1] == "#": # If the note is sharp, return the first two characters to prevent errors
            return self.fretboard[string][fret][:2]
        else: return self.fretboard[string][fret][0]
    
    # Use list comprehension to get the notes of a chord
    def get_chord_at(self, chord):
        keys = list(self.chord_map.keys())
        vals = list(self.chord_map.values())
        pos = vals.index(chord) # Keys have the same index as the values
        return keys[pos]

    def get_note_index(self, string, note):
        for j in range(0, 13):
            if self.get_note_at(string, j) == note:
                return [string, j]
        return "Not a valid note!"
    
    def get_string_index(self, string):
        for j in range(1, 7):
            if self.get_note_at(j, 0) == string:
                return [j]
        return "Not a valid string!"

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
        os = platform()
        if "Windows" in os:
            self.play_obj = self.wav_obj.from_wave_file("Assets\\" + note + ".wav").play()
        else:
            self.play_obj = self.wav_obj.from_wave_file("Assets/" + note + ".wav").play()

    def play_chord(self, notes):
        chord = self.get_chord_at(notes)
        os = platform()
        if "Windows" in os:
            self.play_obj = self.wav_obj.from_wave_file("Assets\\" + chord + ".wav").play()
        else:
            self.play_obj = self.wav_obj.from_wave_file("Assets/" + chord + ".wav").play()
    

    def practice_note(self, targ_note, note):
        if targ_note == note:
            self.played = True
        else: self.played = False

    # Notes are cast as tuples to match the tuple format of the scales and chords
    def practice_chord(self, targ_chord, notes):
        if targ_chord == tuple(notes):
            self.played = True
        else: self.played = False

    def practice_scale(self, targ_scale, notes):
        if targ_scale == tuple(notes):
            self.played = True
        else: self.played = False
