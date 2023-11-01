import sys
from pathlib import Path
from contacts.address_book_manager import AddressBookManager
from contacts.address_book import AddressBook
from contacts.user_interfaces import CommandLineInterface
from contacts.address_book_storage import AddressBookStorage

from notes.notes_manager import NotesManager
from notes.notes_book import NotesBook
from notes.user_interfaces import CommandLineInterface as NotesCommandLineInterface


from notes.notes_manager import NotesManager
from notes.notes_book import NotesBook
from notes.user_interfaces import CommandLineInterface as NotesCommandLineInterface


def main():
    if 'notes' in sys.argv:
        manager = NotesManager(notes_book=NotesBook(), user_interface=NotesCommandLineInterface())
    else:
        manager = AddressBookManager(
            AddressBookStorage('address_book.dat'),
            CommandLineInterface()
        )

    manager.run()


if __name__ == '__main__':
    main()
