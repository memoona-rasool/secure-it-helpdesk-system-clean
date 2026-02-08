from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from src.repositories import users_repo
from src.utils.security import hash_password, verify_password


@dataclass(frozen=True)
class AuthUser:
    id: int
    name: str
    email: str
    role: str


def bootstrap_admin_if_needed() -> Optional[AuthUser]:
    if users_repo.count_users() > 0:
        return None

    name = "Admin"
    email = "admin@local"
    password = "admin12345"
    password_hash = hash_password(password)

    user_id = users_repo.create_user(name, email, password_hash, "admin")
    return AuthUser(id=user_id, name=name, email=email, role="admin")


def login(email: str, password: str) -> Optional[AuthUser]:
    row = users_repo.get_user_by_email(email)
    if row is None:
        return None

    if not verify_password(password, row["password_hash"]):
        return None

    users_repo.update_last_login(int(row["id"]))
    return AuthUser(
        id=int(row["id"]),
        name=str(row["name"]),
        email=str(row["email"]),
        role=str(row["role"]),
    )
