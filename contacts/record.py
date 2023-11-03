from datetime import datetime, date
from common.validators import email, phone


class Record:
    searchable_fields = {
        '': 'Everywhere',
        'full_name': 'Full name',
        'first_name': 'First name',
        'last_name': 'Last name',
        'emails': 'Emails',
        'phones': 'Phones',
        'address': 'Address',
    }

    orderable_fields = {
        'full_name': 'Full name',
        'first_name': 'First name',
        'last_name': 'Last name',
        'id': 'ID',
    }

    fillable_fields = {
        'first_name': 'First name',
        'last_name': 'Last name',
        'birthday': "Date of birth",
        'emails': 'Emails',
        'phones': 'Phones',
        'address': 'Address',
    }

    birthday_format = '%d.%m.%Y'

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
            rows.append(
                f"Birthday: {self._birthday.strftime(self.birthday_format)}")

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
        if self._first_name and self._last_name:
            return self._first_name + ' ' + self._last_name

    @property
    def birthday(self) -> date:
        return self._birthday

    @birthday.setter
    def birthday(self, value: str):
        self._birthday = datetime.strptime(value, self.birthday_format).date()

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

    def replace_email(self, old_email: str, new_email: str):
        idx = self._emails.index(old_email)

        if not old_email or idx < 0:
            return
        if not email(new_email):
            raise ValueError

        self._emails[idx] = new_email

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

    def replace_phone(self, old_phone: str, new_phone: str):
        idx = self._phones.index(old_phone)

        if not new_phone or idx < 0:
            return
        if not phone(new_phone):
            raise ValueError

        self._phones[idx] = new_phone
    
    # TODO: add validation for new_value
    def list_field_replace(self, field: str, old_value, new_value):
        prop_list = getattr(self, '_'+field)
        idx = prop_list.index(old_value)
        
        if not old_value or not new_value or idx < 0:
            return
        
        prop_list[idx] = new_value
        setattr(self, '_'+field, prop_list)
    
    def list_field_delete(self, field: str, value):
        prop_list = getattr(self, '_'+field)
        prop_list.remove(value)
        setattr(self, '_'+field, prop_list)
