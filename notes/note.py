from datetime import datetime
from common import Item


class Note(Item):
    searchable_fields = {
        #'': 'Everywhere',
        'title': 'Title',
        'description': 'Description',
    }

    orderable_fields = {
        'title': 'Title',
        'description': 'Description',
        'created_at': 'Date',
        'id': 'ID',
    }

    fillable_fields = {
        'title': 'Title',
        'description': 'Description',
        'tags': 'Tags',
    }

    validators = {
    }

    def __init__(self) -> None:
        self.__id = id(self)
        self.__created_at = datetime.now()

        self._title = None
        self._description = None
        self._tags = []

    def __str__(self) -> str:
        rows = [f"Title: {self._title}"]

        if self._tags:
            rows.append("Tags: " + ', '.join(self._tags))

        if self._description:
            rows.append(f"Description: {self._description}")

        if self.__created_at:
            rows.append(
                f"Added date: {self.__created_at.strftime('%d.%m.%Y')}")

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

        tags = value.split(",")

        self._tags.extend(tags)
        self._tags.sort()

    def remove_tag(self, value: str):
        self._tags.remove(value)

    def replace_tag(self, old_tag: str, new_tag: str):
        idx = self._tags.index(old_tag)

        if not old_tag or idx < 0:
            return

        self._tags[idx] = new_tag
