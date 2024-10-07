import sqlite3
from tkinter import messagebox

conn = sqlite3.connect('blackjack.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    chips INTEGER DEFAULT 100,
    restarts INTEGER DEFAULT 0
)
''')


def sign_up(username, password,chips):
    try:
        cursor.execute("INSERT INTO players (username, password, chips, restarts) VALUES (?, ?, ?, 0)", (username, password,chips))
        conn.commit()
        messagebox.showinfo("Success", "Account created successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")


def sign_in(username, password):
    cursor.execute("SELECT * FROM players WHERE username=? AND password=?", (username, password))
    player = cursor.fetchone()
    if player:
        messagebox.showinfo("Success", f"Welcome back {username}!")
        return player
    else:
        messagebox.showerror("Error", "Invalid username or password.")
        return None


def update_player_chips(username, chips):
    cursor.execute("UPDATE players SET chips=? WHERE username=?", (chips, username))
    conn.commit()


def fetch_leaderboard():
    cursor.execute("SELECT username, chips, restarts FROM players ORDER BY chips DESC")
    return cursor.fetchall()


def restarts(username):
    cursor.execute("SELECT restarts FROM players WHERE username = ?", (username,))
    current_restarts = cursor.fetchone()[0]

    new_restarts = current_restarts + 1


    cursor.execute("UPDATE players SET restarts = ? WHERE username = ?", (new_restarts, username))
    conn.commit()









