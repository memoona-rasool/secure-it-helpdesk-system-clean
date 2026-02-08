from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from src.repositories import users_repo
from src.utils.security import hash_password, verify_password
from src.utils.validators import normalize_email, require_min_length, require_non_empty


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
    email_n = email.strip().lower()
    row = users_repo.get_user_by_email(email_n)
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


def create_user_as_admin(
    current_user: AuthUser, name: str, email: str, password: str, role: str
) -> int:
    if current_user.role != "admin":
        raise PermissionError("Only admin can create users")

    name_n = require_non_empty(name, "Name")
    email_n = normalize_email(email)
    password_n = require_min_length(password, "Temp password", 8)

    if role not in {"user", "support", "admin"}:
        raise ValueError("Invalid role")

    password_hash = hash_password(password_n)
    return users_repo.create_user(name_n, email_n, password_hash, role)


def change_password(current_user: AuthUser, old_password: str, new_password: str) -> None:
    old_pw = require_non_empty(old_password, "Old password")
    new_pw = require_min_length(new_password, "New password", 8)

    row = users_repo.get_user_by_email(current_user.email)
    if row is None:
        raise ValueError("User not found")

    if not verify_password(old_pw, row["password_hash"]):
        raise PermissionError("Old password is incorrect")

    new_hash = hash_password(new_pw)
    users_repo.update_password_hash(current_user.id, new_hash)
