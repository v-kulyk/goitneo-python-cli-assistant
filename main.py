import sys

from common import EntityStorage
from contacts import AddressBookManager
from contacts import AddressBook
from contacts import CommandLineInterface as ContactsCommandLineInterface
from contacts import fill_demo_data as fill_demo_address_book

from notes.notes_manager import NotesManager
from notes.notes_book import NotesBook
from notes.user_interfaces import CommandLineInterface as NotesCommandLineInterface
from notes.demo import fill_demo_data as fill_demo_notes_book


def createContactsContoller(is_demo):
    return AddressBookManager(
        EntityStorage(
            entity_name='address_book',
            entity_class=AddressBook,
            demo_filler=fill_demo_address_book if is_demo else None
        ),
        ContactsCommandLineInterface()
    )


def createNotesContoller(is_demo):
    return NotesManager(
        EntityStorage(
            entity_name='notes_book',
            entity_class=NotesBook,
            demo_filler=fill_demo_notes_book if is_demo else None
        ),
        NotesCommandLineInterface('Notes', 'Note'),
    )


def main():
    is_demo = '--demo' in sys.argv

    if 'notes' in sys.argv:
        controller = createNotesContoller(is_demo)
    elif 'contacts' in sys.argv:
        controller = createContactsContoller(is_demo)
    else:
        while True:
            user_input = input(
                "Choose application:\n[1]: contacts\n[2]: notes\n")
            if user_input == '1':
                controller = createContactsContoller(is_demo)
                break
            elif user_input == '2':
                controller = createNotesContoller(is_demo)
                break
    try:
        controller.run()
    except KeyboardInterrupt:
        pass

    print("Bye.")


if __name__ == '__main__':
    main()
