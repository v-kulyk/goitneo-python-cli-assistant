from collections import UserDict, defaultdict
from contacts.record import Record
from common.search_request import SearchRequest
from datetime import datetime


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.id] = record

    def find(self, search_request: SearchRequest) -> list:
        records = list(
            filter(lambda r: search_request.is_found(r), self.data.values()))
        return search_request.sort(records)

    def delete(self, id):
        self.data.pop(id)

    def get_birthdays(self, days):
        today = datetime.today().date()

        output_data = defaultdict(list)

        for record in self.data.values():
            if not record.birthday:
                continue

            birthday = record.birthday

            celebration_date = birthday.replace(year=today.year)

            if celebration_date < today:
                celebration_date = celebration_date.replace(
                    year=today.year + 1)

            delta_to_celebration = celebration_date - today

            if delta_to_celebration.days > days:
                continue

            output_data[celebration_date.strftime('%Y-%m-%d')].append(record)

            sorted(output_data)

        return output_data
