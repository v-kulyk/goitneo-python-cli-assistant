from datetime import datetime
from contacts.validators import email, phone


class Record:
    searchable_fields = {
        '': 'Everywhere',
        'full_name': 'Full name',
        'first_name': 'First name',
        'last_name': 'Last name',
        'emails': 'Emails',
        'phones': 'Phones',
    }

    orderable_fields = {
        'full_name': 'Full name',
        'first_name': 'First name',
        'last_name': 'Last name',
        'id': 'ID',
    }

    def __init__(self) -> None:
        self.__id = id(self)
        self.__created_at = datetime.now()

        self._first_name = None
        self._last_name = None
        self._birthday = None
        self._address = None
        self._emails = []
        self._phones = []

    def __str__(self) -> str:
        rows = [f"Name: {self.full_name}"]

        if self._birthday:
            rows.append(f"Birthday: {self._birthday.strftime('%d.%m.%Y')}")

        if self._emails:
            rows.append("Emails: " + ', '.join(self._emails))

        if self._phones:
            rows.append("Phones: " + ', '.join(self._phones))

        return '\n'.join(rows)

    @property
    def id(self):
        return self.__id

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        if not value:
            raise ValueError

        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = value

    @property
    def full_name(self) -> str:
        return self._first_name + ' ' + self._last_name

    @property
    def birthday(self) -> datetime:
        return self._birthday

    @birthday.setter
    def birthday(self, value: str):
        self._birthday = datetime.strptime(value, "%d.%m.%Y")

    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, value: str):
        self._address = value

    @property
    def emails(self) -> list:
        return self._emails.copy()

    @emails.setter
    def emails(self, value: str):
        if not value:
            return
        if not email(value):
            raise ValueError

        self._emails.append(value)

    def remove_email(self, email: str):
        self._emails.remove(email)

    @property
    def phones(self) -> list:
        return self._phones.copy()

    @phones.setter
    def phones(self, value: str):
        if not value:
            return
        if not phone(value):
            raise ValueError

        self._phones.append(value)

    def remove_phone(self, phone: str):
        self._phones.remove(phone)

    def get_writable_attributes(self):
        # get all attributes (properties and methods) of the instance
        attributes = dir(self)

        # get only public properties
        writable_attributes = []

        for attr in attributes:
            if callable(getattr(self, attr)) or attr.startswith("_"):
                continue

            writable_attributes.append(attr)

        return writable_attributes
