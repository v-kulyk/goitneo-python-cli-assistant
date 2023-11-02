from datetime import datetime
from contacts.validators import email, phone


class Note:
    searchable_fields = {
        '': 'Everywhere',
        'title': 'Title',
        'description': 'Description',
    }

    orderable_fields = {
        'title': 'Title',
        'description': 'Description',
        'created_at': 'Date',
        'id': 'ID',
    }

    def __init__(self) -> None:
        self.__id = id(self)
        self.__created_at = datetime.now()

        self._title = None
        self._description = None
        self._tags = []

    def __str__(self) -> str:
        rows = [f"Title: {self._title}"]

        if self._description:
            rows.append(f"Description: {self._description}")

        if self.__created_at:
            rows.append(f"Added date: {self.__created_at.strftime('%d.%m.%Y')}")

        if self._tags:
            rows.append("Tags: " + ', '.join(self._tags))

        return '\n'.join(rows)

    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value: str):
        if not value:
            raise ValueError
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value


    @property
    def tags(self) -> list:
        return self._tags.copy()

    @tags.setter
    def tags(self, value: str):
        if not value:
            return   
        self._tags.append(value)

    def remove_tag(self, value: str):
        self._tags.remove(value)


    def get_writable_attributes(self):
        # get all attributes (properties and methods) of the instance
        attributes = dir(self)
        # get only public properties
        writable_attributes = []
        for attr in attributes:
            if callable(getattr(self, attr)) or attr.startswith("_") or  attr in ['id', 'orderable_fields', 'searchable_fields']:
                continue

            writable_attributes.append(attr)
        return writable_attributes
