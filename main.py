import sys

from common import EntityStorage

from contacts import AddressBookManager
from contacts import AddressBook
from contacts import CommandLineInterface
from contacts import fill_demo_data as fill_demo_address_book

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
            EntityStorage(
                entity_name='address_book',
                entity_class=AddressBook,
                demo_filler=fill_demo_address_book if is_demo else None
            ),
            CommandLineInterface()
        )

    try:
        manager.run()
    except KeyboardInterrupt:
        pass

    print("Bye.")



if __name__ == '__main__':
    main()
