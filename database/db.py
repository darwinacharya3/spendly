import sqlite3
from datetime import date

from werkzeug.security import generate_password_hash

DB_PATH = "expense_tracker.db"

CATEGORIES = [
    "Food",
    "Transport",
    "Bills",
    "Health",
    "Entertainment",
    "Shopping",
    "Other",
]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )
    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    return user


def get_user_by_id(user_id):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return user


def get_expense_summary(user_id):
    conn = get_db()
    row = conn.execute(
        "SELECT COUNT(*) AS count, COALESCE(SUM(amount), 0) AS total "
        "FROM expenses WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    conn.close()
    return {"count": row["count"], "total": row["total"]}


def get_expenses_by_user(user_id):
    conn = get_db()
    expenses = conn.execute(
        "SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC, id DESC",
        (user_id,),
    ).fetchall()
    conn.close()
    return expenses


def get_top_category(user_id):
    conn = get_db()
    row = conn.execute(
        "SELECT category, SUM(amount) AS total FROM expenses "
        "WHERE user_id = ? GROUP BY category ORDER BY total DESC LIMIT 1",
        (user_id,),
    ).fetchone()
    conn.close()
    if row is None:
        return None
    return {"category": row["category"], "total": row["total"]}


def get_category_breakdown(user_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT category, SUM(amount) AS total FROM expenses "
        "WHERE user_id = ? GROUP BY category ORDER BY total DESC",
        (user_id,),
    ).fetchall()
    conn.close()
    return rows


def create_expense(user_id, amount, category, expense_date, description):
    conn = get_db()
    conn.execute(
        "INSERT INTO expenses (user_id, amount, category, date, description) "
        "VALUES (?, ?, ?, ?, ?)",
        (user_id, amount, category, expense_date, description),
    )
    conn.commit()
    conn.close()


def create_user(name, email, password_hash):
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash),
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id


def seed_db():
    conn = get_db()

    existing = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if existing > 0:
        conn.close()
        return

    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
    )
    user_id = cursor.lastrowid

    today = date.today()
    expenses = [
        (120.50, "Food", 1, "Groceries"),
        (45.00, "Transport", 3, "Bus pass"),
        (1500.00, "Bills", 5, "Electricity bill"),
        (300.00, "Health", 7, "Pharmacy"),
        (600.00, "Entertainment", 9, "Movie night"),
        (899.00, "Shopping", 12, "New shoes"),
        (150.00, "Other", 15, "Miscellaneous"),
        (250.00, "Food", 20, "Dinner out"),
    ]

    for amount, category, day, description in expenses:
        expense_date = date(today.year, today.month, day).isoformat()
        conn.execute(
            """
            INSERT INTO expenses (user_id, amount, category, date, description)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, amount, category, expense_date, description),
        )

    conn.commit()
    conn.close()
