from datetime import datetime

class Note:
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

    def replace_tag(self, old_tag: str, new_tag: str):
        idx = self._tags.index(old_tag)

        if not old_tag or idx < 0:
            return
    
        self._tags[idx] = new_tag



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
