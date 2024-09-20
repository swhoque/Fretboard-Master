import sqlite3
import bcrypt
from datetime import datetime

def register_user(conn, user_name, password):
    """
    Register a new user in the user_logins table.

    Args:
        conn (sqlite3.Connection): The database connection object.
        user_name (str): The username of the new user.
        password (str): The password of the new user.

    Returns:
        None
    """
    try:
        with conn:
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            # Insert a new row into the user_logins table
            conn.execute('''INSERT INTO user_logins (user_name, password, session_time, total_time, login_date)
                            VALUES (?, ?, 0, 0, ?)''', 
                            (user_name, hashed_password, datetime.now().date()))
            user_id = conn.execute('''SELECT user_id FROM user_logins WHERE user_name = ?''', (user_name,)).fetchone()[0]
            conn.execute('''INSERT INTO note_stats (user_id, notes_mastered, total_notes_hit, total_notes_missed) VALUES (?, 0, 0, 0)''', (user_id,))
            conn.execute('''INSERT INTO chord_stats (user_id, chords_mastered, total_chords_hit, total_chords_missed) VALUES (?, 0, 0, 0)''', (user_id,))
            conn.execute('''INSERT INTO scale_stats (user_id, scales_mastered, total_scales_hit, total_scales_missed) VALUES (?, 0, 0, 0)''', (user_id,))

            conn.commit()
        # Print a success message
        print("User registered successfully!")
        return True
    except sqlite3.IntegrityError:
        # Print an error message if the username already exists
        return None


def login_user(conn, user_name, password):
    """
    Login a user with the given username and password.

    Args:
        conn (sqlite3.Connection): The database connection object.
        user_name (str): The username of the user.
        password (str): The password of the user.

    Returns:
        tuple or None: The user information if login is successful, None otherwise.
    """
    # Create a cursor object to execute SQL queries
    cur = conn.cursor()

    # Execute a SELECT query to find the user with the given username and password
    cur.execute('''SELECT * FROM user_logins WHERE user_name = ?''', 
                (user_name,))

    # Fetch the first row (user) from the result set
    user = cur.fetchone()

    # If user exists, update the session_time and login_date in the user_logins table
    if user and bcrypt.checkpw(password.encode('utf-8'), user[1]):
        # Get the current timestamp
        session_start_time = int(datetime.now().timestamp())

        # Execute an UPDATE query to update the session_time and login_date
        cur.execute('''UPDATE user_logins 
                       SET session_time = ?, login_date = ? 
                       WHERE user_name = ?''', 
                       (session_start_time, datetime.now().date(), user_name))

        # Commit the changes to the database
        conn.commit()

        # Print a success message
        print("Login successful!")

        # Return the user information
        return user

    # If user does not exist, print an error message and return None
    else:
        print("Invalid username or password.")
        return None

def check_consecutive_logins(conn, user_id):
    """
    Check if a user has logged in consecutively.

    Args:
        conn (sqlite3.Connection): The database connection object.
        user_id (int): The ID of the user.

    Returns:
        bool: True if the user logged in consecutively, False otherwise.
    """

    # Create a cursor object to execute SQL queries
    cur = conn.cursor()

    # Execute a SELECT query to get the last login date of the user
    cur.execute('''SELECT login_date FROM user_logins WHERE user_id = ? ORDER BY login_date DESC LIMIT 1''', 
                (user_id,))
    
    # Fetch the last login date from the result set
    last_login_date = cur.fetchone()
    
    # If no login date is found, return False
    if last_login_date is None:
        return False
    
    # Convert the last login date to a datetime object
    last_login_date = datetime.strptime(last_login_date[0], '%Y-%m-%d').date()
    
    # Calculate the number of days between the current date and the last login date
    days_difference = (datetime.now().date() - last_login_date).days
    
    # If the number of days is 1, the user logged in consecutively
    if days_difference == 1:
        print("User logged in consecutively!")
        return True
    else:
        print("Not a consecutive login.")
        return False

def get_total_time(conn, user_id):
    """
    Retrieve the total time spent in app for a given user.

    Parameters:
    conn (sqlite3.Connection): The database connection object.
    user_id (int): The ID of the user.

    Returns:
    int: The total time of the user. Returns 0 if user not found.
    """
    cur = conn.cursor()
    cur.execute('''SELECT total_time FROM user_logins WHERE user_id = ?''', (user_id,))
    total_time = cur.fetchone()
    
    if total_time is None:
        print("User not found.")
        return 0
    
    return total_time[0]

def update_total_time(conn, user_id):
    """
    Update the total time spent in app for a user by adding the session time.

    Args:
        conn (sqlite3.Connection): The database connection object.
        user_id (int): The ID of the user.

    Returns:
        None
    """
    cur = conn.cursor()
    cur.execute('''SELECT session_time FROM user_logins WHERE user_id = ?''', (user_id,))
    session_start_time = cur.fetchone()
    
    # Check if user_id exists in the database
    if session_start_time is None:
        print("User not found.")
        return
    
    session_start_time = session_start_time[0]
    
    # Check if session_start_time is not None
    if session_start_time is None:
        print("Session start time not found for user.")
        return
    
    # Calculate the session duration
    try:
        session_duration = int(datetime.now().timestamp()) - session_start_time
        print(f"Session duration: {session_duration}")
    except (ValueError, TypeError) as e:
        print(f"Error calculating session duration: {e}")
        return
    
    # Calculate the new total time
    try:
        current_time_spent = get_total_time(conn, user_id) + session_duration
        print(f"Current total time: {current_time_spent}")
    except TypeError as e:
        print(f"Error calculating total time: {e}")
        return
    
    # Update the user_logins table
    cur.execute('''UPDATE user_logins 
                   SET total_time = ?, session_time = 0
                   WHERE user_id = ?''', 
                   (current_time_spent, user_id))
    conn.commit()
    print("Total time updated successfully!")

def get_note_stats(conn, user_id):
    """
    Retrieve the note statistics for a given user from the database.

    Args:
        conn (sqlite3.Connection): The database connection object.
        user_id (int): The ID of the user.

    Returns:
        tuple: The note statistics for the user.
                If no statistics found, returns None.

    """
    # Create a cursor object
    cur = conn.cursor()

    # Execute the SQL query to retrieve the stats
    cur.execute('''SELECT * FROM note_stats WHERE user_id = ?''', (user_id,))

    # Fetch the first (and only) row of the result
    stats = cur.fetchone()

    # If stats found, return them
    if stats:
        return stats
    # If no stats found, print a message and return None
    else:
        print("No note stats found for user.")
        return None

def get_chord_stats(conn, user_id):
    """
    Get the chord statistics for a user from the database.

    Args:
        conn (sqlite3.Connection): The database connection object.
        user_id (int): The ID of the user.

    Returns:
        tuple: The chord statistics for the user.
                If no statistics found, returns None.
    """
    cur = conn.cursor()
    # Execute the SQL query to retrieve the stats
    cur.execute('''SELECT * FROM chord_stats WHERE user_id = ?''', (user_id,))
    # Fetch the first (and only) row of the result
    stats = cur.fetchone()
    # If stats found, return them
    if stats:
        return stats
    # If no stats found, print a message and return None
    else:
        print("No chord stats found for user.")
        return None

def get_scale_stats(conn, user_id):
    """
    Get the scale statistics for a user from the database.

    Args:
        conn (sqlite3.Connection): The database connection object.
        user_id (int): The ID of the user.

    Returns:
        tuple: The scale statistics for the user.
                If no statistics found, returns None.
    """
    cur = conn.cursor()
    # Execute the SQL query to retrieve the stats
    cur.execute('''SELECT * FROM scale_stats WHERE user_id = ?''', (user_id,))
    # Fetch the first (and only) row of the result
    stats = cur.fetchone()
    # If stats found, return them
    if stats:
        return stats
    # If no stats found, print a message and return None
    else:
        print("No scale stats found for user.")
        return None

def update_note_stats(conn, user_id, mastered=0, hit=0, missed=0):
    try:
        if conn is None:
            raise ValueError("Database connection is not established.")
        
        cur = conn.cursor()

        # Debugging: Print current values
        if mastered == 0 and hit == 0 and missed == 0:
            print("No changes made to note stats.")
        else:
            cur.execute('''
                UPDATE note_stats SET notes_mastered = notes_mastered + ?,
                    total_notes_hit = total_notes_hit + ?,
                    total_notes_missed = total_notes_missed + ?
                WHERE user_id = ?
            ''', (mastered, hit, missed, user_id))

            # Debugging: Check how many rows were affected
            print(f"Rows affected: {cur.rowcount}")

            conn.commit()
            print("Note stats updated successfully!")
        cur.close()
    except sqlite3.Error as e:
        print(f"Error updating note stats: {e}")
    except ValueError as e:
        print(e)

def update_chord_stats(conn, user_id, mastered=0, hit=0, missed=0):
    """
    Update the chord statistics for a user in the database.

    Args:
        conn (sqlite3.Connection): The database connection object.
        user_id (int): The ID of the user.
        mastered (int, optional): The number of chords mastered. Defaults to None.
        hit (int, optional): The number of chords hit. Defaults to None.
        missed (int, optional): The number of chords missed. Defaults to None.
    """
    # Create a cursor object
    cur = conn.cursor()

    # Execute update statement if there are any updates to make
    if mastered == 0 or hit == 0 or missed == 0:
        print("No updates to make.")
    else:
        cur.execute(f'''UPDATE chord_stats 
                        SET chords_mastered = chords_mastered + ?,
                        total_chords_hit = total_chords_hit + ?,
                        total_chords_missed = total_chords_missed + ? 
                        WHERE user_id = ?''', 
                        (mastered, hit, missed, user_id))
        conn.commit()
        print("Chord stats updated successfully!")
    cur.close()

def update_scale_stats(conn, user_id, mastered=0, hit=0, missed=0):
    """
    Update the scale statistics for a user in the database.

    Args:
        conn (sqlite3.Connection): The database connection object.
        user_id (int): The ID of the user.
        mastered (int, optional): The number of scales mastered. Defaults to None.
        hit (int, optional): The number of scales hit. Defaults to None.
        missed (int, optional): The number of scales missed. Defaults to None.

    Returns:
        None
    """
    # Create a cursor object
    cur = conn.cursor()

    # Execute update statement if there are any updates to make
    if mastered == 0 and hit == 0 and missed == 0:
        print("No updates to make.")
    else:
        cur.execute(f'''UPDATE scale_stats 
                        SET scales_mastered = scales_mastered + ?,
                        total_scales_hit = total_scales_hit + ?,
                        total_scales_missed = total_scales_missed + ? 
                        WHERE user_id = ?''', 
                        (mastered, hit, missed, user_id))
        conn.commit()
        print("Scale stats updated successfully!")
    cur.close()

