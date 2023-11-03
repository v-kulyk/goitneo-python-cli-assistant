from collections import UserDict, defaultdict
from notes.note import Note
from contacts.search_request import SearchRequest
from datetime import datetime, timedelta




class NotesBook(UserDict):
    def add(self, item: Note):
        self.data[item.id] = item

    def find(self, search_request: SearchRequest) -> list:
        items = list(filter(lambda r: search_request.is_found(r), self.data.values()))
        return search_request.sort(items)

    def delete(self, id):
        self.data.pop(id)

