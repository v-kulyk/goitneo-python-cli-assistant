from collections import UserDict, defaultdict
from contacts.record import Record
from datetime import datetime, timedelta
import pickle
import calendar


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.id()] = record

    def find(self, name: str):
        raise NotImplemented

    def delete(self, id):
        self.data.pop(id)

    def get_birthdays(self, days):
        today = datetime.today().date()

        output_data = defaultdict(list)

        for name in self.data:
            if not self.data[name].birthday:
                continue

            birthday = self.data[name].birthday.value

            celebration_date = birthday.replace(year=today.year)

            if celebration_date < today:
                celebration_date = celebration_date.replace(
                    year=today.year + 1)

            delta_to_celebration = celebration_date - today

            if delta_to_celebration.days >= days:
                continue

            output_data[celebration_date.weekday()].append(name)
            sorted(output_data)

        output = []

        for weekday_index in output_data.keys():
            day_name = calendar.day_name[weekday_index]
            celebrator_names = ", ".join(output_data.get(weekday_index))

            output.append(f"{day_name}: {celebrator_names}")

        return output
