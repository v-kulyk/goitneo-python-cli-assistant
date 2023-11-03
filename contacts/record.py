from datetime import datetime, date
from common import Item
from common.validators import email as email_validator, phone as phone_validator


class Record(Item):
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
    
    validators = {
        'emails': email_validator,
        'phones': phone_validator,
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

        emails = value.split(",")

        valid_emails = filter(lambda email: email_validator(email), emails)

        if len(valid_emails) != len(emails):
            raise ValueError

        self._emails.extend(valid_emails)
        self._emails.sort()

    def remove_email(self, email: str):
        self._emails.remove(email)

    def replace_email(self, old_email: str, new_email: str):
        idx = self._emails.index(old_email)

        if not old_email or idx < 0:
            return
        if not email_validator(new_email):
            raise ValueError

        self._emails[idx] = new_email

    @property
    def phones(self) -> list:
        return self._phones.copy()

    @phones.setter
    def phones(self, value: str):
        if not value:
            return

        phones = value.split(",")

        valid_phones = filter(lambda phone: phone_validator(phone), phones)

        if len(valid_phones) != len(phones):
            raise ValueError

        self._phones.extend(valid_phones)
        self._phones.sort()

    def remove_phone(self, phone: str):
        self._phones.remove(phone)

    def replace_phone(self, old_phone: str, new_phone: str):
        idx = self._phones.index(old_phone)

        if not new_phone or idx < 0:
            return
        if not phone_validator(new_phone):
            raise ValueError

        self._phones[idx] = new_phone
