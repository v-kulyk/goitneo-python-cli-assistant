from contacts.address_book import AddressBook
from contacts.demo import fill_demo_data

import pickle

class AddressBookStorage():
    def __init__(self, book_name:str, is_demo:bool=False) -> None:
        self.book_name = book_name
        self.is_demo = is_demo

    def load(self)->AddressBook:
        try:
            with open(self.__get_path(), 'rb') as fh:
                data = pickle.load(fh)

                if isinstance(data, AddressBook):
                    return data
        except FileNotFoundError:
            pass

        book = AddressBook()

        if self.is_demo and len(book) == 0:
            fill_demo_data(book)

        return book

    def save(self, address_book:AddressBook):
        with open(self.__get_path(), 'wb') as fh:
            pickle.dump(address_book, fh)

    def __get_path(self):
        return self.book_name + "_demo.dat" if self.is_demo else self.book_name + ".dat"
        