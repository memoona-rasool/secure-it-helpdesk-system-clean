from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Optional

from src.repositories.db import get_connection


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def create_user(name: str, email: str, password_hash: str, role: str) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            """
            INSERT INTO users (name, email, password_hash, role, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name.strip(), email.strip().lower(), password_hash, role, _now_iso()),
        )
        conn.commit()
        return int(cur.lastrowid)


def get_user_by_email(email: str) -> Optional[sqlite3.Row]:
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email.strip().lower(),),
        )
        return cur.fetchone()


def update_last_login(user_id: int) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE users SET last_login = ? WHERE id = ?",
            (_now_iso(), user_id),
        )
        conn.commit()


def count_users() -> int:
    with get_connection() as conn:
        cur = conn.execute("SELECT COUNT(*) AS c FROM users")
        row = cur.fetchone()
        return int(row["c"])


def update_password_hash(user_id: int, new_password_hash: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (new_password_hash, user_id),
        )
        conn.commit()
