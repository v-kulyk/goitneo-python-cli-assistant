import re


def email(value: str):
    return bool(re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', value))


def phone(value: str) -> bool:
    return bool(re.fullmatch(r"^\\+?[1-9][0-9]{7,14}$", value))