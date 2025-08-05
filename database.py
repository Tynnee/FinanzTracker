import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                type TEXT NOT NULL,
                date TEXT NOT NULL)''')
    conn.commit()
    conn.close()


def add_transaction(amount, category, description, type):
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO transactions (amount, category, description, type, date) VALUES (?, ?, ?, ?, ?)',
                (amount, category, description, type, date))
    conn.commit()
    conn.close()


def get_transactions():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('SELECT * FROM transactions ORDER BY date DESC')
    transactions = c.fetchall()
    conn.close()
    return transactions


def delete_transaction(id):
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('DELETE FROM transactions WHERE id = ?', (id,))
    conn.commit()
    conn.close()