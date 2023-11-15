# portfolio.py
import sqlite3
from datetime import datetime
from .transaction_history import TransactionHistoryManager  # Make sure to import TransactionHistoryManager

DATABASE_NAME = 'user_portfolio.db'


class PortfolioManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.transaction_history_manager = TransactionHistoryManager(user_id)  # Initialize TransactionHistoryManager

    def get_portfolio_tickers(self):
        tickers_query = 'SELECT DISTINCT ticker FROM portfolio WHERE user_id = ?'
        tickers_data = self._execute_db(tickers_query, (self.user_id,))
        return [ticker[0] for ticker in tickers_data]

    def _execute_db(self, query, parameters=(), fetchone=False, commit=False):
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            if commit:
                conn.commit()
            if fetchone:
                return cursor.fetchone()
            return cursor.fetchall()

    def buy_stock(self, ticker, num_shares, price_per_share):
        transaction_time = datetime.now()
        buy_query = '''
        INSERT INTO portfolio 
        (user_id, ticker, shares, price_per_share, transaction_time, type)
        VALUES (?, ?, ?, ?, ?, ?);
        '''
        self._execute_db(
            buy_query,
            (self.user_id, ticker, num_shares, price_per_share, transaction_time, 'buy'),
            commit=True
        )
        # Log the transaction using TransactionHistoryManager
        self.transaction_history_manager.log_transaction(ticker, num_shares, price_per_share, 'buy')

    def sell_stock(self, ticker, num_shares, price_per_share):
        transaction_time = datetime.now()
        # Fetch the number of shares owned
        shares_owned = self._execute_db(
            'SELECT SUM(shares) FROM portfolio WHERE user_id = ? AND ticker = ? AND type = "buy"',
            (self.user_id, ticker),
            fetchone=True
        )

        if shares_owned and shares_owned[0] >= num_shares:
            sell_query = '''
            INSERT INTO portfolio 
            (user_id, ticker, shares, price_per_share, transaction_time, type)
            VALUES (?, ?, ?, ?, ?, ?);
            '''
            self._execute_db(
                sell_query,
                (self.user_id, ticker, -num_shares, price_per_share, transaction_time, 'sell'),
                commit=True
            )
            # Log the sell transaction
            self.transaction_history_manager.log_transaction(ticker, -num_shares, price_per_share, 'sell')

    def calculate_gain_loss(self):
        gain_loss_query = '''
        SELECT ticker, SUM(shares * price_per_share) as total,
        (SELECT price_per_share FROM portfolio WHERE ticker = portfolio.ticker AND user_id = ? AND type = "sell" ORDER BY transaction_time DESC LIMIT 1) as last_sell_price
        FROM portfolio 
        WHERE user_id = ? AND type = "buy"
        GROUP BY ticker;
        '''
        results = self._execute_db(gain_loss_query, (self.user_id, self.user_id))
        gain_loss = {}
        for row in results:
            ticker, total_buy, last_sell_price = row
            current_value = self._execute_db(
                'SELECT shares * price_per_share FROM portfolio WHERE user_id = ? AND ticker = ? AND type = "buy"',
                (self.user_id, ticker),
                fetchone=True
            )
            total_gain_loss = (last_sell_price if last_sell_price else 0) - (current_value[0] if current_value else 0)
            gain_loss[ticker] = total_gain_loss
        return gain_loss
