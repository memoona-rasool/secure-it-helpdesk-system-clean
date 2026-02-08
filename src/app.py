from src.repositories.db import init_db


def main():
    init_db()
    print("Secure IT Helpdesk System - database initialised")


if __name__ == "__main__":
    main()
