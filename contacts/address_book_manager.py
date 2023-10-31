from contacts.record import Record
from contacts.address_book import AddressBook
from contacts.user_interfaces import UserInterface


class AddressBookManager:
    def __init__(self, address_book: AddressBook, user_interface: UserInterface) -> None:
        self.address_book = address_book
        self.user_interface = user_interface

    def run(self):
        action = self.user_interface.show_actions(actions=self._get_public_methods_list())
        method = getattr(self, action)
        method()

    def add_contact(self):
        record = self.user_interface.new_record()
        self.address_book.add_record(record=record)
        self.user_interface.contact_added(record)

    def find_contact(self) -> Record:
        search_request = self.user_interface.get_search_request()
        records = self.address_book.find(search_request)
        self.user_interface.show_records(records)

    def change_contact(self):
        id, field, value = self.user_interface.change_record()
        record = self.address_book.get(id)
        record[field] = value
        self.user_interface.contact_changed(record)

    def get_birthdays(self):
        self.user_interface.show_birthdays(self.address_book.get_birthdays())

    def _get_public_methods_list(self):
        return [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("_") and func != "run"]



