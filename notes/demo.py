import random

from faker import Faker

from notes.notes_book import NotesBook
from notes.note import Note


def fill_demo_data(notes_book: NotesBook):
    fake = Faker()
    Faker.seed(0)

    for i in range(random.randint(10, 20)):
        note = get_random_note(fake)
        notes_book.add(note)


def get_random_note(fake) -> Note:
    note = Note()
    note.title = fake.sentence(nb_words=random.randint(3, 6))
    note.description = fake.paragraph(nb_sentences=random.randint(2, 5))

    tags = [
        'finance',
        'family',
        'health',
        'auto',
    ]

    for tag in random.sample(tags, random.randint(1, 3)):
        note.tags = tag

    return note
