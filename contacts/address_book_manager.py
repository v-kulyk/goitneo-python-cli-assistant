from contacts.record import Record
from contacts.user_interfaces import UserInterface
from contacts.address_book_storage import AddressBookStorage

from datetime import date, datetime


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

        records = list(self.address_book.data.values())
        record = self.user_interface.select_contact(records)

        attrs_dict = Record.fillable_fields

        field_idx = self.user_interface.choose(
            list(attrs_dict.values()),
            "Which field do you want to change?",
            "Please select a valid field."
        )

        field = list(attrs_dict.keys())[field_idx]
        label = attrs_dict[field]

        current_value = getattr(record, field)

        if isinstance(current_value, datetime) or isinstance(current_value, date):
            current_value = current_value.strftime(Record.birthday_format)

        if isinstance(current_value, list):
            self._update_record_list(record, field, label)
        else:
            message = f"[Change contact] Please specify new value for {label}: {current_value}"
            self._set_record_value(record, field, label, message)

        self.storage.save(address_book=self.address_book)

        self.user_interface.contact_changed(record)

        self.run()

    def remove_contact(self):
        self.user_interface.clear()

        records = list(self.address_book.data.values())
        record = self.user_interface.select_contact(records)

        self.address_book.delete(record.id)

        self.storage.save(address_book=self.address_book)

        self.user_interface.contact_removed()

        self.run()

    def get_birthdays(self):
        days = self.user_interface.get_birthdays_interval()

        birthdays = self.address_book.get_birthdays(days)

        self.user_interface.show_birthdays(birthdays)

        self.run()

    def exit(self):
        pass

    def _update_record_list(self, record: Record, field: str, label: str):
        current_value = getattr(record, field)
        action = self._get_list_action(label)

        if action == 'add':
            self._set_record_value(record, field, label,
                                   f"[{label}] Please add new entry")
        elif action == 'delete':
            idx = self.user_interface.choose(
                current_value,
                "Which entry do you want to delete?",
                "Please select a valid entry."
            )

            record.list_field_delete(field, current_value[idx])

        elif action == 'edit':
            idx = self.user_interface.choose(
                current_value,
                "Which entry do you want to change?",
                "Please select a valid entry."
            )

            old_entry = current_value[idx]
            new_entry = self.user_interface.input(
                f"Enter replacement for {old_entry}:")

            record.list_field_replace(field, old_entry, new_entry)

    def _get_list_action(self, label: str) -> str:
        actions = {
            'add': 'Add',
            'edit': 'Edit',
            'delete': 'Delete',
        }

        action_idx = self.user_interface.choose(
            list(actions.values()),
            f"Choose action for {label}:",
            "Please select a valid action."
        )

        return list(actions.keys())[action_idx]

    def _set_record_value(self, record: Record, field: str, label: str, message: str):
        while True:
            value = self.user_interface.input(message)

            try:
                setattr(record, field, value)
            except ValueError:
                self.user_interface.error(f'Incorrect value for {label}')
            else:
                break
