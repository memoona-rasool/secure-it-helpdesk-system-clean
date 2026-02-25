import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "helpdesk.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('user', 'support', 'admin')),
                created_at TEXT NOT NULL,
                last_login TEXT
            );
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('open', 'in_progress', 'resolved', 'closed')),
                priority TEXT NOT NULL CHECK(priority IN ('low', 'medium', 'high', 'urgent')),
                created_by INTEGER NOT NULL,
                assigned_to INTEGER,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(created_by) REFERENCES users(id),
                FOREIGN KEY(assigned_to) REFERENCES users(id)
            );
            """
        )

        conn.commit()
