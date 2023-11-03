from notes.notes_book import NotesBook
import pickle

class Storage():
    def __init__(self, path=None) -> None:
        self.path = path

    def load(self)->NotesBook:
        try:
            with open(self.path, 'rb') as fh:
                data = pickle.load(fh)
                if not isinstance(data, NotesBook):
                    data = NotesBook()
        except FileNotFoundError:
            data = NotesBook()
        return data


    def save(self, address_book:NotesBook):
        with open(self.path, 'wb') as fh:
            pickle.dump(address_book, fh)
        