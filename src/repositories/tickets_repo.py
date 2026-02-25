from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Optional

from src.repositories.db import get_connection


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def create_ticket(
    title: str,
    description: str,
    priority: str,
    created_by: int,
) -> int:
    now = _now_iso()
    with get_connection() as conn:
        cur = conn.execute(
            """
            INSERT INTO tickets (title, description, status, priority, created_by, assigned_to, created_at, updated_at)
            VALUES (?, ?, 'open', ?, ?, NULL, ?, ?)
            """,
            (title, description, priority, created_by, now, now),
        )
        conn.commit()
        return int(cur.lastrowid)


def get_ticket_by_id(ticket_id: int) -> Optional[sqlite3.Row]:
    with get_connection() as conn:
        cur = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
        return cur.fetchone()


def list_tickets_for_user(user_id: int) -> list[sqlite3.Row]:
    with get_connection() as conn:
        cur = conn.execute(
            """
            SELECT id, title, status, priority, created_by, assigned_to, created_at, updated_at
            FROM tickets
            WHERE created_by = ?
            ORDER BY id DESC
            """,
            (user_id,),
        )
        return cur.fetchall()


def list_all_tickets() -> list[sqlite3.Row]:
    with get_connection() as conn:
        cur = conn.execute(
            """
            SELECT id, title, status, priority, created_by, assigned_to, created_at, updated_at
            FROM tickets
            ORDER BY id DESC
            """
        )
        return cur.fetchall()
