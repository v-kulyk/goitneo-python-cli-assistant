from contacts.record import Record
from contacts.user_interfaces import UserInterface
from contacts.address_book_storage import AddressBookStorage


class AddressBookManager:
    methods = {
        'find_contact': 'Search',
        'list_contacts': 'List all contacts',
        'add_contact': "New contact",
        'change_contact': "Edit contact",
        'remove_contact': "Delete contact",
        'get_birthdays': "Get birthdays",
        'exit': 'Exit',
    }

    def __init__(self, storage: AddressBookStorage, user_interface: UserInterface) -> None:
        self.address_book = storage.load()

        self.user_interface = user_interface

        self.storage = storage

        self.user_interface.clear()

    def run(self):
        method_idx = self.user_interface.choose(
            list(AddressBookManager.methods.values()),
            "[Contacts]: what do you want to do ?",
            "Please specify a valid action"
        )
        
        method_name = list(AddressBookManager.methods.keys())[method_idx]

        method = getattr(self, method_name)

        method()

    def list_contacts(self):
        self.user_interface.clear()

        records = self.address_book.data.values()

        self.user_interface.show_records(records)

        self.run()

    def add_contact(self):
        self.user_interface.clear()

        record = self.user_interface.new_contact()

        self.address_book.add_record(record=record)

        self.storage.save(address_book=self.address_book)

        self.user_interface.contact_added(record)

        self.run()

    def find_contact(self) -> Record:
        self.user_interface.clear()

        search_request = self.user_interface.get_search_request()

        records = self.address_book.find(search_request)

        self.user_interface.show_records(records)

        self.run()

    def change_contact(self):
        self.user_interface.clear()

        record = self.user_interface.select_contact(self.address_book)

        attrs_dict = Record.fillable_fields

        field_idx = self.user_interface.choose(
            list(attrs_dict.values()),
            "Which field do you want to change?",
            "Please select a valid field."
        )

        field = list(attrs_dict.keys())[field_idx]
        label = list(attrs_dict.values())[field_idx]

        while True:
            value = self.user_interface.input(
                f"[Change contact] Please specify new value for {label}"
            )

            try:
                setattr(record, field, value)
            except ValueError:
                self.user_interface.error(f'Incorrect value for {label}')
            else:
                break

        self.storage.save(address_book=self.address_book)

        self.user_interface.contact_changed(record)

        self.run()

    def remove_contact(self):
        self.user_interface.clear()

        record = self.user_interface.select_contact(self.address_book)

        self.address_book.delete(record.id)

        self.storage.save(address_book=self.address_book)

        self.user_interface.contact_removed()

        self.run()

    def get_birthdays(self):
        self.user_interface.show_birthdays(
            self.address_book.get_birthdays()
        )

        self.run()

    def exit(self):
        pass