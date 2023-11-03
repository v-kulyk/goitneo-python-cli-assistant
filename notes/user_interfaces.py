from common import BaseInterface, SearchRequest
from notes.note import Note
from notes.notes_book import NotesBook
from common.search_request import SearchRequest
from os import system


class CommandLineInterface(BaseInterface):
    def __init__(self) -> None:
        self.items_title = 'Notes'
        self.item_title = 'Note'

    def new_item(self):
        item = Note()  # creating new instance of Note class

        # get only public properties
        writable_attributes = Note.fillable_fields

        # for each public property we as user for input
        for field, label in writable_attributes.items():
            while True:
                try:
                    user_input = self.input(
                        f"[New {self.item_title}] Please specify `{label}`:")
                    setattr(item, field, user_input)
                except ValueError:
                    self.error(f"Incorrect value for `{label}`")
                else:
                    break

        return item

    def item_added(self, item: Note):
        print(
            f"[{self.items_title}] {self.item_title} {item.title} was added to {self.items_title}.")

    def select_item(self, items: list) -> Note:
        names = list(map(lambda r: r.title, items))

        name_idx = self.choose(
            names, f"Select {self.item_title}:", f"Incorrect input, please select existing {self.item_title}.")

        return items[name_idx]

    def item_changed(self, item: Note):
        print(f"{self.item_title} was changed:")
        print(item)

    def item_removed(self):
        print("{self.item_title} was removed.")

    def get_filter_request(self, items):
        all_tags = items.get_all_tags()
        while True:
            choice = self.choose(
                all_tags,
                'Choose tag for filter:',
                'Incorrect input',
                0,
            )
            if choice is None:
                continue

            return all_tags[choice]
