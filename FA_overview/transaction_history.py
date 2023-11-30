# transaction_history.py
import sqlite3
from datetime import datetime

DATABASE_NAME = 'user_portfolio.db'


class TransactionHistoryManager:
    def __init__(self, user_id):
        self.user_id = user_id

    def _execute_db(self, query, parameters=(), fetchone=False, commit=False):
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            if commit:
                conn.commit()
            if fetchone:
                return cursor.fetchone()
            return cursor.fetchall()

    def log_stock_transaction(self, ticker, shares, price_per_share, transaction_type):
        transaction_time = datetime.now()
        log_query = '''
        INSERT INTO transaction_history
        (user_id, ticker, shares, price_per_share, transaction_type, transaction_time)
        VALUES (?, ?, ?, ?, ?, ?);
        '''
        self._execute_db(
            log_query,
            (self.user_id, ticker, shares, price_per_share, transaction_type, transaction_time),
            commit=True
        )

    def log_cash_transaction(self, amount, transaction_type):
        transaction_time = datetime.now()
        log_query = '''
        INSERT INTO cash_transactions
        (user_id, amount, transaction_type, transaction_time)
        VALUES (?, ?, ?, ?);
        '''
        self._execute_db(
            log_query,
            (self.user_id, amount, transaction_type, transaction_time),
            commit=True
        )

    def get_transaction_history(self):
        history_query = '''
        SELECT ticker, shares, price_per_share, transaction_type, transaction_time
        FROM transaction_history
        WHERE user_id = ?
        ORDER BY transaction_time DESC;
        '''
        return self._execute_db(history_query, (self.user_id,))

    def get_cash_transaction_history(self):
        history_query = '''
        SELECT amount, transaction_type, transaction_time
        FROM cash_transactions
        WHERE user_id = ?
        ORDER BY transaction_time DESC;
        '''
        return self._execute_db(history_query, (self.user_id,))


# The following function should be called to ensure the transaction history tables exist.
def create_transaction_history_tables():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        # Create stock transaction history table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transaction_history (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            ticker TEXT,
            shares INTEGER,
            price_per_share REAL,
            transaction_type TEXT,
            transaction_time DATETIME,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        ''')
        # Create cash transaction history table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS cash_transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            transaction_type TEXT,
            transaction_time DATETIME,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        ''')
        conn.commit()


# Make sure to create tables on initialization
create_transaction_history_tables()
