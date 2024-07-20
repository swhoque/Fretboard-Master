import simpleaudio as sa

class Fretboard:
    def __init__(self):
        self.num_strings = 6
        self.num_frets = 12
        self.notes_hit = list()
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
    
    def get_chord_at(self, notes):
        match notes:
            case [(5, 2), (4, 2)]:
                return "Em"
            case [(3, 1), (5, 2), (4, 2)]:
                return "E"
            case [(2, 1), (4, 2), (3, 2)]:
                return "Am"
            case [(2, 1), (4, 2), (5, 3)]:
                return "C"
            case [(5, 2), (6, 3), (1, 3)]:
                return "G"
            case [(3, 2), (1, 2), (2, 3)]:
                return "D"
            case [(4, 2), (3, 2), (2, 2)]:
                return "A"
            case [(1, 1), (2, 1), (3, 2), (4, 3)]:
                return "F"
            case [(4, 1), (5, 2), (3, 2), (1, 2)]:
                return "B7"
            case [(1, 1), (3, 2), (2, 3)]:
                return "Dm"
            case [(2, 1), (4, 2), (6, 3), (5, 3)]:
                return "C/G"
            case [(1, 1), (2, 1), (3, 2), (5, 3), (4, 3), (6, 1)]:
                return "F(Barre)"
            case [(5, 2), (3, 2), (1, 2)]:
                return "Bm7"
            case [(1, 2), (2, 3), (3, 4)]:
                return "Bm(v1)"
            case [(1, 2), (4, 4), (3, 4), (2, 4)]:
                return "B"
            case [(2, 1), (3, 2), (1, 2)]:
                return "D7"
            case [(4, 2), (2, 2)]:
                return "A7"

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
        self.play_obj = self.wav_obj.from_wave_file("Assets/" + note + ".wav").play()

    def play_chord(self, notes):
        chord = self.get_chord_at(notes)
        self.play_obj = self.wav_obj.from_wave_file("Assets/" + chord + ".wav").play()

    def practice_note(self, targ_note, note):
        if targ_note == note:
            self.played = True
        else: self.played = False

    def practice_chord(self, targ_chord, notes):
        if targ_chord == notes:
            self.played = True
        else: self.played = False
