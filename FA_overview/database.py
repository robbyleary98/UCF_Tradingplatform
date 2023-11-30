# Import necessary libraries
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Define the database name
DATABASE_NAME = 'user_portfolio.db'


# Function to create tables in the database
def create_tables():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cur = conn.cursor()
        # Create a table for users if it doesn't exist
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        ''')
        # Add more table creation statements as needed
        conn.commit()


# Function to add a new user to the database
def add_user(username, password):
    password_hash = generate_password_hash(password)
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
            conn.commit()
    except sqlite3.DatabaseError as e:
        print(f"An error occurred: {e}")


# Function to authenticate a user
def authenticate_user(username, password):
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cur = conn.cursor()
            cur.execute('SELECT user_id, password_hash FROM users WHERE username = ?', (username,))
            user = cur.fetchone()
            if user and check_password_hash(user[1], password):
                return user[0]  # Return the user_id
            else:
                return None
    except sqlite3.DatabaseError as e:
        print(f"An error occurred: {e}")
        return None


# Call the function to create tables
create_tables()
