import re


def email(func):
    def inner(self, email: str) -> bool:
        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
            raise ValueError
        return func(self, email)

    return inner


def phone(func):
    def inner(self, phone: str) -> bool:
        if not re.fullmatch(r"^\\+?[1-9][0-9]{7,14}$", phone):
            raise ValueError
        return func(self, phone)

    return inner
