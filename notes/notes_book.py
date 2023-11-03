from collections import UserDict
from notes.note import Note
from common.search_request import SearchRequest


class NotesBook(UserDict):
    def add(self, item: Note):
        self.data[item.id] = item

    def find(self, search_request: SearchRequest) -> list:
        items = list(
            filter(lambda r: search_request.is_found(r), self.data.values()))
        return search_request.sort(items)

    def filter(self, tag):
        items = []
        for item in self.data.values():
            if tag in item.tags:
                items.append(item)
        return items

    def get_all_tags(self):
        tags = []
        for item in self.data.values():
            if len(item.tags):
                if len(item.tags) == 1:
                    tags.append(item.tags[0])
                else:
                    tags.extend(item.tags)
        return list(set(tags))

    def delete(self, id):
        self.data.pop(id)
