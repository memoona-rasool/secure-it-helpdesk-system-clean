from __future__ import annotations

from src.repositories.db import init_db
from src.services.auth_service import (
    bootstrap_admin_if_needed,
    login,
    create_user_as_admin,
    change_password,
    list_users_as_admin,
    delete_user_as_admin,
)
from src.services.ticket_service import create_ticket, list_tickets
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
    elif user.role == "support":
        support_menu(user)
    else:
        user_menu(user)


def user_menu(current_user):
    while True:
        print("User menu")
        print("1. Create ticket")
        print("2. List my tickets")
        print("3. Exit")
        choice = prompt("Choose: ")

        if choice == "1":
            create_ticket_flow(current_user)
        elif choice == "2":
            list_tickets_flow(current_user)
        elif choice == "3":
            print("Goodbye")
            return
        else:
            print("Invalid choice")

        print()


def support_menu(current_user):
    while True:
        print("Support menu")
        print("1. List all tickets")
        print("2. Exit")
        choice = prompt("Choose: ")

        if choice == "1":
            list_tickets_flow(current_user)
        elif choice == "2":
            print("Goodbye")
            return
        else:
            print("Invalid choice")

        print()


def admin_menu(current_user):
    while True:
        print("Admin menu")
        print("1. Create support user")
        print("2. Create normal user")
        print("3. Change my password")
        print("4. List users")
        print("5. Delete user by id")
        print("6. Create ticket")
        print("7. List all tickets")
        print("8. Exit")
        choice = prompt("Choose: ")

        if choice == "1":
            create_user_flow(current_user, "support")
        elif choice == "2":
            create_user_flow(current_user, "user")
        elif choice == "3":
            change_password_flow(current_user)
        elif choice == "4":
            list_users_flow(current_user)
        elif choice == "5":
            delete_user_flow(current_user)
        elif choice == "6":
            create_ticket_flow(current_user)
        elif choice == "7":
            list_tickets_flow(current_user)
        elif choice == "8":
            print("Goodbye")
            return
        else:
            print("Invalid choice")

        print()


def create_user_flow(current_user, role: str):
    from src.utils.validators import require_non_empty, require_min_length, normalize_email

    try:
        name = require_non_empty(prompt("Name: "), "Name")
        email = normalize_email(prompt("Email: "))
        password = require_min_length(prompt_password("Temp password: "), "Temp password", 8)

        user_id = create_user_as_admin(current_user, name, email, password, role)
        label = "support user" if role == "support" else "user"
        print(f"Created {label} with id {user_id}")
    except Exception as e:
        print(f"Error: {e}")


def change_password_flow(current_user):
    from src.utils.validators import require_min_length, require_non_empty

    try:
        old_pw = require_non_empty(prompt_password("Old password: "), "Old password")
        new_pw = require_min_length(prompt_password("New password: "), "New password", 8)

        change_password(current_user, old_pw, new_pw)
        print("Password changed successfully")
    except Exception as e:
        print(f"Error: {e}")


def list_users_flow(current_user):
    try:
        rows = list_users_as_admin(current_user)
        if not rows:
            print("No users found")
            return

        print("Users")
        for r in rows:
            last_login = r["last_login"] if r["last_login"] else "-"
            print(f'{r["id"]}: {r["name"]} | {r["email"]} | {r["role"]} | created {r["created_at"]} | last login {last_login}')
    except Exception as e:
        print(f"Error: {e}")


def delete_user_flow(current_user):
    raw = prompt("User id to delete: ")
    try:
        user_id = int(raw)
        delete_user_as_admin(current_user, user_id)
        print("User deleted")
    except Exception as e:
        print(f"Error: {e}")


def create_ticket_flow(current_user):
    try:
        title = prompt("Title: ")
        description = prompt("Description: ")
        priority = prompt("Priority (low, medium, high, urgent): ")
        ticket_id = create_ticket(current_user, title, description, priority)
        print(f"Ticket created with id {ticket_id}")
    except Exception as e:
        print(f"Error: {e}")


def list_tickets_flow(current_user):
    try:
        rows = list_tickets(current_user)
        if not rows:
            print("No tickets found")
            return

        print("Tickets")
        for t in rows:
            assigned = t["assigned_to"] if t["assigned_to"] else "-"
            print(f'{t["id"]}: {t["title"]} | {t["status"]} | {t["priority"]} | created_by {t["created_by"]} | assigned_to {assigned}')
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
