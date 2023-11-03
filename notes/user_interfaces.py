from common import BaseInterface, SearchRequest
from notes.note import Note
from notes.notes_book import NotesBook
from common.search_request import SearchRequest
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


    def get_search_request(self):
        search_request = SearchRequest()

        while True:
            if len(search_request.search) < 2:
                search_request.search = self.input(
                    "[Search]: please, input at least 2 characters\n")
                continue

            if search_request.field is None:
                choice = self.choose(
                    list(Note.searchable_fields.values()),
                    '[Field]: choose where to search:',
                    'Incorrect input',
                    0,
                )
                search_request.field = list(
                    Note.searchable_fields.keys())[choice]
                continue

            if search_request.sort_by is None:
                choice = self.choose(
                    list(Note.orderable_fields.values()),
                    '[Field]: choose the sorting criteria:',
                    'Incorrect input',
                    0,
                )
                search_request.sort_by = list(
                    Note.orderable_fields.keys())[choice]
                continue

            if search_request.is_descending is None:
                choice = self.choose(
                    ['Normal', 'Inverted'],
                    '[Field]: choose the sorting order:',
                    'Incorrect input',
                    0,
                )
                search_request.is_descending = choice > 0
                continue

            return search_request

    def get_filter_request(self, items):       
        all_tags = items.get_all_tags();
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
    

    def show_items(self, items: list):
        print('')

        if not items:
            print('No items found')
            return

        for item in items:
            print(item)
            print('')

    def clear(self):
        system('clear')


    def __set_completer(self, options: list):
        #completer = Completer(options)
        #readline.set_completer(completer.complete)
        #readline.parse_and_bind('tab: complete')
        pass

    def __unset_completer(self):
        #readline.set_completer(None)
        pass
