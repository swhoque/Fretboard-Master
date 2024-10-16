import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection established!")
    except sqlite3.Error as e:
        print(e)
    return conn

def initialize_database(conn):
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS user_logins (
                            user_name TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            session_time INTEGER,
                            total_time INTEGER,
                            login_date DATE,
                            streak INTEGER
                        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS note_stats (
                            user_id INTEGER PRIMARY KEY,
                            notes_mastered INTEGER,
                            total_notes_hit INTEGER,
                            total_notes_missed INTEGER,
                            FOREIGN KEY (user_id) REFERENCES user_logins(user_id)
                        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS chord_stats (
                            user_id INTEGER PRIMARY KEY,
                            chords_mastered INTEGER,
                            total_chords_hit INTEGER,
                            total_chords_missed INTEGER,
                            FOREIGN KEY (user_id) REFERENCES user_logins(user_id)
                        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS scale_stats (
                            user_id INTEGER PRIMARY KEY,
                            scales_mastered INTEGER,
                            total_scales_hit INTEGER,
                            total_scales_missed INTEGER,
                            FOREIGN KEY (user_id) REFERENCES user_logins(user_id)
                        )''')
