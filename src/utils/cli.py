from __future__ import annotations

import getpass


def prompt(text: str) -> str:
    return input(text).strip()


def prompt_password(text: str) -> str:
    return getpass.getpass(text).strip()
