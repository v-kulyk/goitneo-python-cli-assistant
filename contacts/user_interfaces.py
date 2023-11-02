from contacts.record import Record
from contacts.address_book import AddressBook
from contacts.search_request import SearchRequest


class UserInterface:
    def input(self, prompt):
        raise NotImplemented

    def choose(self, choice_options: dict, prompt: str, err_msg: str):
        raise NotImplemented

    def error(self, msg: str):
        raise NotImplemented

    def select_contact(self, address_book: AddressBook):
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

    def show_birthdays(self):
        raise NotImplemented


class CommandLineInterface(UserInterface):
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

    def new_contact(self):
        record = Record()  # creating new instance of Record class

        # get only public properties
        writable_attributes = record.get_writable_attributes()

        # for each public property we as user for input
        for attr in writable_attributes:
            while True:
                try:
                    user_input = input(f"[Contacts] Please specify {attr}:\n")
                    setattr(record, attr, user_input)
                except ValueError:
                    self.error(f"Incorrect value for {attr}")
                else:
                    break

        return record

    def error(self, msg: str):
        print("[ERROR]: " + msg)

    def contact_added(self, record: Record):
        print(f"Contact {record.full_name} was added to address book.\n")

    def select_contact(self, address_book: AddressBook):
        names = []

        ids = []

        for record in address_book.values():
            names.append(f"{record.full_name}")

            ids.append(record.id())

        name_idx = self.choose(
            names, "Select contact:", "Incorrect input, please select existing contact.")

        return address_book[ids[name_idx]]

    def contact_changed(self, record: Record):
        print(f"Contact {record.full_name} was changed\n")

    def contact_removed(self):
        print("Contact was removed.\n")

    def get_search_request(self):
        search_request = SearchRequest()

        while True:
            if len(search_request.search) < 2:
                search_request.search = input(
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
