import sys

from contacts.address_book_manager import AddressBookManager
from contacts.address_book import AddressBook
from contacts.user_interfaces import CommandLineInterface
from contacts.address_book_storage import AddressBookStorage

from notes.notes_manager import NotesManager
from notes.notes_book import NotesBook
from notes.user_interfaces import CommandLineInterface as NotesCommandLineInterface


def main():
    is_demo = '--demo' in sys.argv

    if 'notes' in sys.argv:
        manager = NotesManager(notes_book=NotesBook(),
                               user_interface=NotesCommandLineInterface())
    else:
        manager = AddressBookManager(
            AddressBookStorage(book_name='adress_book', is_demo=is_demo),
            CommandLineInterface(),
        )

    try:
        manager.run()
    except KeyboardInterrupt:
        pass

    print("Bye.")



if __name__ == '__main__':
    main()
