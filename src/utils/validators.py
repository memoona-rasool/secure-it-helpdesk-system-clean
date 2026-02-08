from __future__ import annotations


def require_non_empty(value: str, field_name: str) -> str:
    v = value.strip()
    if not v:
        raise ValueError(f"{field_name} cannot be empty")
    return v


def require_min_length(value: str, field_name: str, min_len: int) -> str:
    v = value.strip()
    if len(v) < min_len:
        raise ValueError(f"{field_name} must be at least {min_len} characters")
    return v


def normalize_email(email: str) -> str:
    e = email.strip().lower()
    if not e:
        raise ValueError("Email cannot be empty")
    if "@" not in e or e.startswith("@") or e.endswith("@"):
        raise ValueError("Email must be a valid email address")
    return e
