from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.repositories.db import init_db
from src.repositories import users_repo
from src.utils.security import hash_password

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 scripts/reset_user_password.py <email> <new_password>")
        raise SystemExit(1)

    email = sys.argv[1].strip().lower()
    new_password = sys.argv[2].strip()

    if len(new_password) < 8:
        raise SystemExit("New password must be at least 8 characters")

    init_db()

    row = users_repo.get_user_by_email(email)
    if row is None:
        raise SystemExit("User not found")

    new_hash = hash_password(new_password)
    users_repo.update_password_hash(int(row["id"]), new_hash)

    print("Password reset successfully.")
    print(f"Email: {email}")

if __name__ == "__main__":
    main()
