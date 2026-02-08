from src.repositories.db import init_db
from src.services.auth_service import bootstrap_admin_if_needed, login


def main():
    init_db()

    bootstrapped = bootstrap_admin_if_needed()
    if bootstrapped:
        print("Admin account created:")
        print("Email: admin@local")
        print("Password: admin12345")

    user = login("admin@local", "admin12345")
    if user:
        print(f"Login successful. Role: {user.role}")
    else:
        print("Login failed")


if __name__ == "__main__":
    main()
