from common import BaseInterface, SearchRequest
from notes.note import Note
from os import system


class CommandLineInterface(BaseInterface):
    def __init__(self, items_title, item_title) -> None:
        self.items_title = items_title
        self.item_title = item_title

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

    def __set_completer(self, options: list):
        #completer = Completer(options)
        #readline.set_completer(completer.complete)
        #readline.parse_and_bind('tab: complete')
        pass

    def __unset_completer(self):
        #readline.set_completer(None)
        pass
