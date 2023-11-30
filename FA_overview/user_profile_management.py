# user_profile_management.py
import sqlite3
from werkzeug.security import generate_password_hash
import json

DATABASE_NAME = 'user_portfolio.db'


def create_tables():
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    financial_goal TEXT,
                    risk_tolerance TEXT,
                    investment_preference TEXT
                )
            ''')
            conn.commit()
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def add_user(username, password, financial_goal=None, risk_tolerance=None, investment_preference=None):
    password_hash = generate_password_hash(password)
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO users (username, password_hash, financial_goal, risk_tolerance, investment_preference) 
                VALUES (?, ?, ?, ?, ?)
            ''', (username, password_hash, financial_goal, risk_tolerance, investment_preference))
            conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"A user with that username already exists: {e}")
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def update_user_profile(user_id, financial_goal=None, risk_tolerance=None, investment_preference=None):
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cur = conn.cursor()
            cur.execute('''
                UPDATE users SET financial_goal = ?, risk_tolerance = ?, investment_preference = ? WHERE user_id = ?
            ''', (financial_goal, risk_tolerance, investment_preference, user_id))
            conn.commit()
            if cur.rowcount == 0:
                print("User not found.")
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_user_profile(user_id):
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cur = conn.cursor()
            cur.execute('''
                SELECT username, financial_goal, risk_tolerance, investment_preference FROM users WHERE user_id = ?
            ''', (user_id,))
            profile = cur.fetchone()
            return profile if profile else None
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def add_user_risk_profile(user_id, answers_json):
    answers = json.loads(answers_json)
    risk_score = calculate_risk_score(answers)
    risk_profile = categorize_risk_profile(risk_score)
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cur = conn.cursor()
            cur.execute('''
                UPDATE users SET risk_tolerance = ? WHERE user_id = ?
            ''', (risk_profile, user_id))
            conn.commit()
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def calculate_risk_score(answers):
    score = sum(answers.values())
    return score


def categorize_risk_profile(risk_score):
    if risk_score <= 10:
        return 'Low'
    elif risk_score <= 15:
        return 'Medium'
    else:
        return 'High'


# Initialize the database tables
create_tables()
