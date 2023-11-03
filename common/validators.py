import re


def email(value: str):
    return bool(re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', value))


def phone(value: str) -> bool:
    return bool(re.fullmatch(r"^[+]?\d{10,14}$", value))
