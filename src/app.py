from __future__ import annotations

from src.repositories.db import init_db
from src.services.auth_service import (
    bootstrap_admin_if_needed,
    login,
    create_user_as_admin,
    change_password,
)
from src.utils.cli import prompt, prompt_password


def main():
    init_db()

    bootstrapped = bootstrap_admin_if_needed()
    if bootstrapped:
        print("Admin account created:")
        print("Email: admin@local")
        print("Password: admin12345")
        print("Log in and change this password soon.")
        print()

    print("Secure IT Helpdesk System")
    print()

    email = prompt("Email: ")
    password = prompt_password("Password: ")

    user = login(email, password)
    if not user:
        print("Login failed")
        return

    print(f"Login successful. Welcome {user.name}. Role: {user.role}")
    print()

    if user.role == "admin":
        admin_menu(user)
    else:
        print("User menu coming next (tickets).")


def admin_menu(current_user):
    while True:
        print("Admin menu")
        print("1. Create support user")
        print("2. Create normal user")
        print("3. Change my password")
        print("4. Exit")
        choice = prompt("Choose: ")

        if choice == "1":
            create_user_flow(current_user, "support")
        elif choice == "2":
            create_user_flow(current_user, "user")
        elif choice == "3":
            change_password_flow(current_user)
        elif choice == "4":
            print("Goodbye")
            return
        else:
            print("Invalid choice")

        print()


def create_user_flow(current_user, role: str):
    name = prompt("Name: ")
    email = prompt("Email: ")
    password = prompt_password("Temp password: ")

    try:
        user_id = create_user_as_admin(current_user, name, email, password, role)
        print(f"Created {role} user with id {user_id}")
    except Exception as e:
        print(f"Error: {e}")


def change_password_flow(current_user):
    old_pw = prompt_password("Old password: ")
    new_pw = prompt_password("New password: ")

    try:
        change_password(current_user, old_pw, new_pw)
        print("Password changed successfully")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
