from contacts.record import Record
from contacts.user_interfaces import UserInterface
from contacts.address_book_storage import AddressBookStorage
from contacts.demo import fill_demo_data


class AddressBookManager:
    def __init__(self, storage: AddressBookStorage, user_interface: UserInterface, is_demo=False) -> None:
        self.address_book = storage.load()

        self.user_interface = user_interface

        self.storage = storage

        self.is_demo = is_demo

        if is_demo:
            fill_demo_data(self.address_book)

    def run(self):
        methods_list = self._get_public_methods_list()

        method_idx = self.user_interface.choose(
            methods_list,
            "[Contacts]: what do you want to do ?",
            "Please specify a valid action"
        )

        method = getattr(self, methods_list[method_idx])

        method()

    def list_contacts(self):
        records = self.address_book.data.values()

        self.user_interface.show_records(records)

        self.run()

    def add_contact(self):
        record = self.user_interface.new_contact()

        self.address_book.add_record(record=record)

        self.storage.save(address_book=self.address_book)

        self.user_interface.contact_added(record)

        self.run()

    def find_contact(self) -> Record:
        search_request = self.user_interface.get_search_request()

        records = self.address_book.find(search_request)

        self.user_interface.show_records(records)

        self.run()

    def change_contact(self):
        record = self.user_interface.select_contact(
            self.address_book,
            "Which contact do you want to change?",
            "Please select an existing contact."
        )

        field = self.user_interface.choose(
            record.get_writable_attributes(),
            "Which field do you want to change?",
            "Please select a valid field."
        )

        while True:
            value = self.user_interface.input(
                f"Please specify new value for {field}"
            )

            try:
                setattr(record, field, value)
            except ValueError:
                self.user_interface.error(f'Incorrect value for {field}')
            else:
                break

        self.storage.save(address_book=self.address_book)

        self.user_interface.contact_changed(record)

        self.run()

    def remove_contact(self):
        record = self.user_interface.select_contact(
            self.address_book,
            "Which contact do you want to remove?",
            "Please select an existing contact."
        )

        self.address_book.delete(record.id())

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

    def _get_public_methods_list(self):
        return [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("_") and func != "run"]
