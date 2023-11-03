from common import BaseManager
from contacts.record import Record
from datetime import date, datetime


class AddressBookManager(BaseManager):
    methods = {
        'find_contact': 'Search',
        'list_contacts': 'List all contacts',
        'add_contact': "New contact",
        'change_contact': "Edit contact",
        'remove_contact': "Delete contact",
        'get_birthdays': "Get birthdays",
        'exit': 'Exit',
    }

    def run(self):
        method_idx = self.user_interface.choose(
            list(self.methods.values()),
            "[Contacts]: what do you want to do ?",
            "Please specify a valid action"
        )

        method_name = list(self.methods.keys())[method_idx]

        method = getattr(self, method_name)

        method()

    def list_contacts(self):
        self.user_interface.clear()

        records = self.book.data.values()

        self.user_interface.show_items(records)

        self.run()

    def add_contact(self):
        self.user_interface.clear()

        record = self.user_interface.new_contact()

        self.book.add_record(record=record)

        self.storage.save(entity=self.book)

        self.user_interface.contact_added(record)

        self.run()

    def find_contact(self):
        self.user_interface.clear()

        search_request = self.user_interface.get_search_request(Record.searchable_fields, Record.orderable_fields)

        records = self.book.find(search_request)

        self.user_interface.show_items(records)

        self.run()

    def change_contact(self):
        self.user_interface.clear()

        records = list(self.book.data.values())
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
            self._update_item_list(record, field, label)
        else:
            message = f"[Change contact] Please specify new value for {label}: {current_value}"
            self._set_item_value(record, field, label, message)

        self.storage.save(entity=self.book)

        self.user_interface.contact_changed(record)

        self.run()

    def remove_contact(self):
        self.user_interface.clear()

        records = list(self.book.data.values())
        record = self.user_interface.select_contact(records)

        self.book.delete(record.id)

        self.storage.save(entity=self.book)

        self.user_interface.contact_removed()

        self.run()

    def get_birthdays(self):
        days = self.user_interface.get_birthdays_interval()

        birthdays = self.book.get_birthdays(days)

        self.user_interface.show_birthdays(birthdays)

        self.run()

    def exit(self):
        pass
