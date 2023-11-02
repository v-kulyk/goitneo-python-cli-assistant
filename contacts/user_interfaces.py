from contacts.record import Record
from contacts.address_book import AddressBook
from contacts.search_request import SearchRequest
from contacts.completer import Completer
import readline
from os import system

from datetime import datetime


class UserInterface:
    def input(self, prompt):
        raise NotImplemented

    def choose(self, choice_options: list, prompt: str, err_msg: str, default=None):
        raise NotImplemented

    def error(self, msg: str):
        raise NotImplemented

    def select_contact(self, records: list) -> Record:
        raise NotImplemented

    def new_contact(self) -> Record:
        raise NotImplemented

    def contact_added(self, record: Record):
        raise NotImplemented

    def contact_changed(self, record: Record):
        raise NotImplemented

    def contact_removed(self):
        raise NotImplemented

    def get_search_request(self) -> SearchRequest:
        raise NotImplemented

    def show_records(self, records: list):
        raise NotImplemented

    def get_birthdays_interval(self) -> int:
        pass

    def show_birthdays(self, birthdays: dict):
        raise NotImplemented

    def clear(self):
        raise NotImplemented


class CommandLineInterface(UserInterface):
    def input(self, prompt):
        return input(prompt + "\n>")

    def choose(self, choice_options: list, prompt: str, err_msg: str, default=None) -> str:
        prompt = prompt + "\n"

        self.__set_completer(choice_options)

        while True:
            for i in range(len(choice_options)):
                prompt += f"[{i+1}]: {choice_options[i]}\n"

            user_input = self.input(prompt)

            if not user_input and not default is None:
                self.__unset_completer()
                return default

            if not user_input.isnumeric() and user_input not in choice_options:
                self.error(err_msg)
                continue

            choice_index = int(
                user_input) - 1 if user_input.isnumeric() else choice_options.index(user_input)

            if choice_index >= 0 and choice_index < len(choice_options):
                self.__unset_completer()
                return choice_index

            self.__unset_completer()

            self.error(err_msg)

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

    def error(self, msg: str):
        print("[ERROR]: " + msg + "\n")

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

    def get_search_request(self):
        search_request = SearchRequest()

        while True:
            if len(search_request.search) < 2:
                search_request.search = self.input(
                    "[Search]: please, input at least 2 characters\n")
                continue

            if search_request.field is None:
                choice = self.choose(
                    list(Record.searchable_fields.values()),
                    '[Field]: choose where to search:',
                    'Incorrect input',
                    0,
                )
                search_request.field = list(
                    Record.searchable_fields.keys())[choice]
                continue

            if search_request.sort_by is None:
                choice = self.choose(
                    list(Record.orderable_fields.values()),
                    '[Field]: choose the sorting criteria:',
                    'Incorrect input',
                    0,
                )
                search_request.sort_by = list(
                    Record.orderable_fields.keys())[choice]
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

    def show_records(self, records: list):
        print('')

        if not records:
            print('No records found')
            return

        for record in records:
            print(record)
            print('')

    def clear(self):
        system('clear')

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

    def __set_completer(self, options: list):
        completer = Completer(options)

        readline.set_completer(completer.complete)

        readline.parse_and_bind('tab: complete')

    def __unset_completer(self):
        readline.set_completer(None)
