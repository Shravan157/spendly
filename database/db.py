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

def get_user_profile(user_id):
    """
    Retrieves full user details for the profile page.
    """
    with get_db() as conn:
        return conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

def get_user_expenses(user_id):
    """
    Retrieves all expenses for a user, ordered by date descending.
    """
    with get_db() as conn:
        return conn.execute(
            'SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC',
            (user_id,)
        ).fetchall()

def get_spending_summary(user_id):
    """
    Returns total spent, total transactions, and top category.
    """
    with get_db() as conn:
        # Total spent and total transactions
        summary = conn.execute(
            'SELECT SUM(amount) as total, COUNT(*) as count FROM expenses WHERE user_id = ?',
            (user_id,)
        ).fetchone()

        # Top spending category
        top_cat = conn.execute(
            'SELECT category, SUM(amount) as total FROM expenses WHERE user_id = ? GROUP BY category ORDER BY total DESC LIMIT 1',
            (user_id,)
        ).fetchone()

        return {
            "total_spent": summary["total"] or 0,
            "total_transactions": summary["count"] or 0,
            "top_category": top_cat["category"] if top_cat else "None"
        }

def get_category_breakdown(user_id):
    """
    Returns totals and percentages for each category.
    """
    with get_db() as conn:
        total_spent = conn.execute(
            'SELECT SUM(amount) FROM expenses WHERE user_id = ?',
            (user_id,)
        ).fetchone()[0] or 0

        breakdown = conn.execute(
            'SELECT category, SUM(amount) as total FROM expenses WHERE user_id = ? GROUP BY category ORDER BY total DESC',
            (user_id,)
        ).fetchall()

        results = []
        for row in breakdown:
            results.append({
                "category": row["category"],
                "amount": row["total"],
                "percentage": (row["total"] / total_spent * 100) if total_spent > 0 else 0
            })
        return results
