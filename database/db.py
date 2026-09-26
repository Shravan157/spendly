import sqlite3
from werkzeug.security import generate_password_hash

DATABASE_PATH = 'spendly.db'

def get_db():
    """
    Returns a SQLite connection with row_factory set to sqlite3.Row
    and foreign keys enabled.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def create_user(name, email, password_hash):
    """
    Creates a new user in the database.
    Returns the ID of the created user.
    """
    with get_db() as conn:
        cursor = conn.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
            (name, email, password_hash)
        )
        conn.commit()
        return cursor.lastrowid

def get_user_by_email(email):
    """
    Retrieves a user by their email address.
    Returns a sqlite3.Row object if found, otherwise None.
    """
    with get_db() as conn:
        return conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

def init_db():
    """
    Initializes the database by creating all necessary tables.
    """
    with get_db() as conn:
        # Users table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        ''')

        # Expenses table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        conn.commit()

def seed_db():
    """
    Seeds the database with a demo user and sample expenses.
    Prevents duplicate seeding.
    """
    with get_db() as conn:
        # Check if users already exist
        cursor = conn.execute('SELECT id FROM users LIMIT 1')
        if cursor.fetchone():
            return

        # Insert demo user
        demo_password = generate_password_hash('demo123')
        cursor = conn.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
            ('Demo User', 'demo@spendly.com', demo_password)
        )
        user_id = cursor.lastrowid

        # Fixed categories list
        categories = ['Food', 'Transport', 'Bills', 'Health', 'Entertainment', 'Shopping', 'Other']

        # Sample expenses (8 total, covering all categories)
        sample_expenses = [
            (user_id, 5.50, 'Food', '2026-09-01', 'Morning Latte'),
            (user_id, 12.00, 'Transport', '2026-09-02', 'Bus Pass'),
            (user_id, 60.00, 'Bills', '2026-09-05', 'Internet Bill'),
            (user_id, 25.00, 'Health', '2026-09-08', 'Pharmacy'),
            (user_id, 15.00, 'Entertainment', '2026-09-12', 'Movie Ticket'),
            (user_id, 45.00, 'Shopping', '2026-09-15', 'New Shirt'),
            (user_id, 10.00, 'Other', '2026-09-18', 'Miscellaneous'),
            (user_id, 12.50, 'Food', '2026-09-20', 'Lunch Sandwich'),
        ]

        conn.executemany(
            'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
            sample_expenses
        )

        conn.commit()
