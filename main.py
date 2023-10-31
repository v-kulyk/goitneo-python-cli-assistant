from contacts.address_book_manager import AddressBookManager
from contacts.address_book import AddressBook
from contacts.user_interfaces import CommandLineInterface

def main():
    manager = AddressBookManager(address_book=AddressBook(), user_interface=CommandLineInterface())
    manager.run()

if __name__ == '__main__':
    main()

