from notes.note import Note
from notes.user_interfaces import CommandLineInterface
from contacts.address_book_storage import AddressBookStorage as Storage
#from contacts.demo import fill_demo_data


class NotesManager:
    def __init__(self, storage: Storage, user_interface: CommandLineInterface) -> None:
        self.items = storage.load()
        self.user_interface = user_interface
        self.storage = storage


    def run(self):
        methods_list = self._get_public_methods_list()
        method_idx = self.user_interface.choose(
            methods_list,
            "[Notes]: what do you want to do ?",
            "Please specify a valid action"
        )
        method = getattr(self, methods_list[method_idx])
        method()


    def list_items(self):
        items = self.items.data.values()
        self.user_interface.show_items(items)
        self.run()


    def add_item(self):
        item = self.user_interface.new_item()
        self.items.add(item)
        self.storage.save(self.items)
        self.user_interface.item_added(item)
        self.run()


    def find_item(self):
        search_request = self.user_interface.get_search_request()
        notes = self.items.find(search_request)
        self.user_interface.show_notes(notes)
        self.run()


    def change_item(self):
        note = self.user_interface.select_item(
            self.items,
            "Which note do you want to change?",
            "Please select an existing note."
        )
        field = self.user_interface.choose(
            note.get_writable_attributes(),
            "Which field do you want to change?",
            "Please select a valid field."
        )
        while True:
            value = self.user_interface.input(
                f"Please specify new value for {field}"
            )
            try:
                setattr(note, field, value)
            except ValueError:
                self.user_interface.error(f'Incorrect value for {field}')
            else:
                break

        self.storage.save(self.items)
        self.user_interface.item_changed(note)
        self.run()


    def remove_item(self):
        note = self.user_interface.select_item(
            self.items,
            "Which note do you want to remove?",
            "Please select an existing note."
        )

        self.items.delete(note.id())
        self.storage.save(self.items)
        self.user_interface.item_removed()
        self.run()


    def exit(self):
        pass

    def _get_public_methods_list(self):
        return [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("_") and func != "run"]
