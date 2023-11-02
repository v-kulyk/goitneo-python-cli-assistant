from notes.note import Note
from notes.notes_book import NotesBook
from contacts.search_request import SearchRequest


class CommandLineInterface:
    def __init__(self, items_title, item_title) -> None:
        self.items_title = items_title
        self.item_title = item_title

    def input(self, prompt):
        return input(">>>" + prompt)

    def choose(self, choice_options: list, prompt: str, err_msg: str, default=None) -> str:
        prompt = prompt + "\n"

        while True:
            for i in range(len(choice_options)):
                prompt += f"[{i+1}]: {choice_options[i]}\n"

            user_input = input(prompt)

            if not user_input and not default is None:
                return default

            if user_input.isnumeric():
                choice_index = int(user_input) - 1

                if choice_index >= 0 and choice_index < len(choice_options):
                    print(choice_options[choice_index])
                    return choice_index

            self.error(err_msg)

    def new_item(self):
        item = Note()  # creating new instance of Note class

        # get only public properties
        writable_attributes = item.get_writable_attributes()

        # for each public property we as user for input
        for attr in writable_attributes:
            while True:
                try:
                    user_input = input(f"[Notes] Please specify {attr}:\n")
                    setattr(item, attr, user_input)
                except ValueError:
                    self.error(f"Incorrect value for {attr}")
                else:
                    break

        return item

    def error(self, msg: str):
        print("[ERROR]: " + msg)

    def item_added(self, item: Note):
        print(f"Note {item.title} was added to notes book.\n")

    def select_item(self, items):
        names = []
        ids = []
        for item in items.values():
            names.append(f"{item.title}")
            ids.append(item.id())

        name_idx = self.choose(
            names, "Select note:", "Incorrect input, please select existing note.")
        return items[ids[name_idx]]

    def item_changed(self, item: Note):
        print(f"Note {item.title} was changed\n")

    def item_removed(self):
        print("Note was removed.\n")

    def get_search_request(self):
        search_request = SearchRequest()

        while True:
            if len(search_request.search) < 2:
                search_request.search = input(
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

    def show_items(self, items: list):
        print('')

        if not items:
            print('No records found')
            return

        for item in items:
            print(item)
            print('')
