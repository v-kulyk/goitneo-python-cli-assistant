from contacts.address_book import AddressBook

import pickle

class AddressBookStorage():
    def __init__(self, path=None) -> None:
        self.path = path

    def load(self)->AddressBook:
        try:
            with open(self.path, 'rb') as fh:
                data = pickle.load(fh)

                if isinstance(data, AddressBook):
                    return data
        except FileNotFoundError:
            pass

        return AddressBook()

    def save(self, address_book:AddressBook):
        with open(self.path, 'wb') as fh:
            pickle.dump(address_book, fh)
        