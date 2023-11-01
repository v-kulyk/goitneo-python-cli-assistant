from contacts.record import Record
from contacts.address_book import AddressBook


class UserInterface:
    def input(self, prompt):
        raise NotImplemented

    def choose(self, choice_options:dict, prompt:str, err_msg:str):
        raise NotImplemented

    def error(self, msg:str):
        raise NotImplemented

    def select_contact(self, address_book: AddressBook):
        raise NotImplemented

    def new_contact(self) -> Record:
        raise NotImplemented

    def contact_added(self, record:Record):
        raise NotImplemented

    def contact_changed(self, record:Record):
        raise NotImplemented

    def contact_removed(self):
        raise NotImplemented

    def get_search_request(self):
        raise NotImplemented

    def show_records(self, records: list):
        raise NotImplemented

    def show_birthdays(self):
        raise NotImplemented


class CommandLineInterface(UserInterface):
    def input(self, prompt):
        return input(">>>" + prompt)
    
    def choose(self, choice_options:list, prompt:str, err_msg:str) -> str:
        prompt = prompt + "\n"

        while True:
            for i in range(len(choice_options)):
                prompt += f"[{i}]: {choice_options[i]}\n"

            try:
                choice_index = int(input(prompt))

            except ValueError:
                self.error(err_msg)
                continue

            try:
                choice_options[choice_index]

                return choice_index

            except IndexError:
                self.error(err_msg)

    def new_contact(self):
        record = Record() #creating new instance of Record class

        #get only public properties
        writable_attributes = record.get_writable_attributes() 

        #for each public property we as user for input
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

    def contact_added(self, record:Record):
        print(f"Contact {record.first_name} {record.last_name} was added to address book.\n")

    def select_contact(self, address_book: AddressBook):
        names = []

        ids   = []

        for record in address_book.values():
            names.append(f"{record.first_name} {record.last_name}")

            ids.append(record.id())

        name_idx = self.choose(names, "Select contact:", "Incorrect input, please select existing contact.")
        
        return address_book[ids[name_idx]]

        
    def contact_changed(self, record:Record):
        print(f"Contact {record.first_name} {record.last_name} was changed\n")

    def contact_removed(self):
        print("Contact was removed.\n")
        