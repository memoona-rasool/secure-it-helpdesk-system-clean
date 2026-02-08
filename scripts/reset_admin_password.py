from __future__ import annotations

from src.repositories.db import init_db
from src.repositories import users_repo
from src.utils.security import hash_password

ADMIN_EMAIL = "admin@local"
NEW_PASSWORD = "admin12345"


def main():
    init_db()

    row = users_repo.get_user_by_email(ADMIN_EMAIL)
    if row is None:
        raise SystemExit("Admin user not found. Delete helpdesk.db to re-bootstrap.")

    new_hash = hash_password(NEW_PASSWORD)
    users_repo.update_password_hash(int(row["id"]), new_hash)

    print("Admin password reset successfully.")
    print(f"Email: {ADMIN_EMAIL}")
    print(f"Password: {NEW_PASSWORD}")


if __name__ == "__main__":
    main()
