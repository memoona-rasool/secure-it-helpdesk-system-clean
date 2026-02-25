from __future__ import annotations

from src.repositories import tickets_repo
from src.services.auth_service import AuthUser
from src.utils.validators import require_non_empty


VALID_PRIORITIES = {"low", "medium", "high", "urgent"}


def create_ticket(current_user: AuthUser, title: str, description: str, priority: str) -> int:
    title_n = require_non_empty(title, "Title")
    desc_n = require_non_empty(description, "Description")
    pr = priority.strip().lower()

    if pr not in VALID_PRIORITIES:
        raise ValueError("Priority must be one of: low, medium, high, urgent")

    return tickets_repo.create_ticket(title_n, desc_n, pr, current_user.id)


def list_tickets(current_user: AuthUser):
    if current_user.role in {"support", "admin"}:
        return tickets_repo.list_all_tickets()
    return tickets_repo.list_tickets_for_user(current_user.id)
