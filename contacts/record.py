from datetime import datetime
from contacts.validators import email,phone


class Record:
    def __init__(self) -> None:
        self.__id = id(self)
        self.__created_at = datetime.now()

        self._first_name = None
        self._last_name = None
        self._birthday = None
        self._address = None
        self._emails = []
        self._phones = []
        
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
    def birthday(self) -> datetime:
        return self._birthday

    @birthday.setter
    def birthday(self, value: str):
        self._birthday = datetime.strptime(value, "%d.%m.%Y")
        
    @property
    def address(self) -> str:
        return self._address
    
    @address.setter
    def address(self, value:str):
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

        self._emails.append(email)

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

        self._phones.append(phone)

    def remove_phone(self, phone: str):
        self._phones.remove(phone)
        
    def get_writable_attributes(self):
        attributes = dir(self) #get all attributes (properties and methods) of the instance

        #get only public properties
        writable_attributes = []
        
        for attr in attributes:
            if callable(getattr(self, attr)) or attr.startswith("_"):
                continue

            writable_attributes.append(attr)

        return writable_attributes
