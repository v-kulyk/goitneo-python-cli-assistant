import sys

from contacts.address_book_manager import AddressBookManager
from contacts.address_book import AddressBook
from contacts.user_interfaces import CommandLineInterface as ContactsCommandLineInterface
from contacts.address_book_storage import AddressBookStorage

from notes.notes_manager import NotesManager
from notes.notes_book import NotesBook
from notes.user_interfaces import CommandLineInterface
from notes.storage import Storage

def createContactsContoller(is_demo):
    return AddressBookManager(AddressBookStorage(book_name='address_book', is_demo=is_demo), ContactsCommandLineInterface())

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
