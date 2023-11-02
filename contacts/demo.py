import random

from faker import Faker

from contacts.address_book import AddressBook
from contacts.record import Record


def fill_demo_data(address_book: AddressBook):
    fake = Faker()
    Faker.seed(0)

    for i in range(random.randint(10, 20)):
        record = get_random_record(fake)
        address_book.add_record(record)


def get_random_record(fake) -> Record:
    record = Record()
    record.first_name = fake.first_name()
    record.last_name = fake.last_name()

    if random.random() > 0.3:
        record.birthday = fake.date_of_birth().strftime(Record.birthday_format)

    record.emails = fake.email()

    if random.random() > 0.5:
        record.emails = fake.email()

    record.phones = fake.bothify(text='+380#########')

    if random.random() > 0.5:
        record.phones = fake.bothify(text='+380#########')

    return record
