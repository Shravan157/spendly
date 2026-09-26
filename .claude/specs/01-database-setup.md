# Spec: Database Setup (Step 1)

## 1. Overview
Replace the stub in `database/db.py` with a working SQLite implementation to establish the data layer foundation for the Spendly application.

## 2. Database Schema

### A. `users` Table
| Column | Type | Constraints |
| --- | --- | --- |
| id | INTEGER | Primary key, autoincrement |
| name | TEXT | Not null |
| email | TEXT | Unique, not null |
| password_hash | TEXT | Not null |
| created_at | TEXT | Default datetime('now') |

### B. `expenses` Table
| Column | Type | Constraints |
| --- | --- | --- |
| id | INTEGER | Primary key, autoincrement |
| user_id | INTEGER | Foreign key → users.id, not null |
| amount | REAL | Not null |
| category | TEXT | Not null |
| date | TEXT | Not null (YYYY-MM-DD format) |
| description | TEXT | Nullable |
| created_at | TEXT | Default datetime('now') |

## 3. Functions to Implement (`database/db.py`)

### `get_db()`
- Opens connection to the database file in project root.
- Sets `row_factory = sqlite3.Row`.
- Executes `PRAGMA foreign_keys = ON`.
- Returns the connection.

### `init_db()`
- Creates both tables using `CREATE TABLE IF NOT EXISTS`.
- Safe to call multiple times.

### `seed_db()`
- Checks if `users` table already contains data; returns early if it does.
- Inserts one demo user:
    - name: Demo User
    - email: demo@spendly.com
    - password: `demo123` (hashed using `werkzeug.security.generate_password_hash`).
- Inserts **8 sample expenses** linked to the demo user.
- Expenses must cover multiple categories from the fixed list, with dates spread across the current month.

## 4. Categories (Fixed List)
- Food
- Transport
- Bills
- Health
- Entertainment
- Shopping
- Other

## 5. Application Integration (`app.py`)
- Import `get_db`, `init_db`, and `seed_db`.
- Call `init_db()` and `seed_db()` inside `app.app_context()` on startup to ensure the database is ready before routes are accessed.

## 6. Implementation Rules
- **No ORMs**: Use only the standard `sqlite3` library.
- **Security**: Use **parameterized queries only** (`?` placeholders). Never use string formatting in SQL.
- **Integrity**: Enable `PRAGMA foreign_keys = ON` on every connection.
- **Types**: Store `amount` as `REAL`.
- **Dates**: Use **YYYY-MM-DD format** consistently.
- **Passwords**: Use `werkzeug.security.generate_password_hash`.

## 7. Definition of Done
- [ ] Database file is created on app startup.
- [ ] Tables exist with correct schema and constraints.
- [ ] Demo user exists with hashed password.
- [ ] 8 sample expenses exist across the fixed categories.
- [ ] No duplicate seed data on repeated runs.
- [ ] App starts without errors.
- [ ] Foreign key enforcement is functional.
- [ ] All queries use parameterized SQL.
