import sys

from common import EntityStorage
from contacts import AddressBookManager
from contacts import AddressBook
from contacts import CommandLineInterface as ContactsCommandLineInterface
from contacts import fill_demo_data as fill_demo_address_book

from notes.notes_manager import NotesManager
from notes.notes_book import NotesBook
from notes.user_interfaces import CommandLineInterface
from notes.storage import Storage

def createContactsContoller(is_demo):    
    return AddressBookManager(
            EntityStorage(
                entity_name='address_book',
                entity_class=AddressBook,
                demo_filler=fill_demo_address_book if is_demo else None
            ),
            ContactsCommandLineInterface()
        )

def createNotesContoller():
    return NotesManager(Storage('notes_book.dat'), CommandLineInterface('Notes', 'Note'))

def main():
    is_demo = '--demo' in sys.argv

    if 'notes' in sys.argv:
        controller = createNotesContoller();
    elif 'contacts' in sys.argv:
        controller = createContactsContoller(is_demo);
    else:
        while True:
            user_input = input("Choose application:\n[1]: contacts\n[2]: notes\n")
            if user_input == '1':
                controller = createContactsContoller(is_demo);
                break
            elif user_input == '2':
                controller = createNotesContoller();
                break
    try:
        controller.run()
    except KeyboardInterrupt:
        pass

    print("Bye.")


if __name__ == '__main__':
    main()
