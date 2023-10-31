from datetime import datetime
from contacts.validators import email,phone


class Record:
    def __init__(self) -> None:
        self.__id = id(self)
        self.__created_at = datetime.now()

        self._first_name = None
        self._last_name = None
        self._birthday = None
        self._emails = []
        self._phones = []
        
    @property
    def id(self):
        return self.__id

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        pass

    @property
    def birthday(self):
        return self._birthday

    @last_name.setter
    def birthday(self, value: datetime):
        self._birthday = value

    @property
    def emails(self) -> list:
        return self._emails.copy()

    @email
    def add_email(self, email: str):
        self._emails.append(email)

    def remove_email(self, email: str):
        self._emails.remove(email)

    @property
    def phones(self) -> list:
        return self._phones.copy()

    @phone
    def add_phone(self, phone: str):
        self._phones.append(phone)

    def remove_email(self, phone: str):
        self._phones.remove(phone)
