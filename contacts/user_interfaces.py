from datetime import datetime

from common import SearchRequest
from common import BaseInterface

from contacts.record import Record


class CommandLineInterface(BaseInterface):
    def new_contact(self):
        record = Record()  # creating new instance of Record class

        # get only public properties
        writable_attributes = Record.fillable_fields

        # for each public property we as user for input
        for field, label in writable_attributes.items():
            while True:
                try:
                    user_input = self.input(
                        f"[New contact] Please specify `{label}`:")
                    setattr(record, field, user_input)
                except ValueError:
                    self.error(f"Incorrect value for `{label}`")
                else:
                    break

        return record

    def contact_added(self, record: Record):
        print(
            f"[Contacts] Contact {record.full_name} was added to address book.")

    def select_contact(self, records: list) -> Record:
        names = list(map(lambda r: r.full_name, records))

        name_idx = self.choose(
            names, "Select contact:", "Incorrect input, please select existing contact.")

        return records[name_idx]


    def contact_changed(self, record: Record):
        print(f"Contact was changed:")
        print(record)


    def contact_removed(self):
        print("Contact was removed.")

    def get_search_request(self) -> SearchRequest:
        return super().get_search_request(
            searchable_fields=Record.searchable_fields,
            orderable_fields=Record.orderable_fields
        )

    def get_birthdays_interval(self) -> int:
        while True:
            days = self.input(
                '[Birthdays]: please, input the number of days')

            if days and days.isnumeric() and int(days) > 0:
                return int(days)

            print(self.error('Incorrect number of days provided'))

    def show_birthdays(self, birthdays: dict):
        if not len(birthdays):
            print('No birthdays found.')

        for date_str, records in birthdays.items():
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            print(date.strftime(Record.birthday_format + ' (%A)'))

            for record in records:
                years = date.year - record.birthday.year
                print(f"{record.full_name} ({years} years)")

            print('')
