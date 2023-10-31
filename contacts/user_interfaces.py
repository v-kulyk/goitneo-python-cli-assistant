from contacts.record import Record


class UserInterface:
    def show_ations(self, actions: dict):
        raise NotImplemented

    def new_record(self) -> Record:
        raise NotImplemented

    def contact_added(self):
        raise NotImplemented

    def get_search_request(self):
        raise NotImplemented

    def show_records(self, records: list):
        raise NotImplemented

    def change_record(self, id, field, value):
        raise NotImplemented

    def show_birthdays(self):
        raise NotImplemented


class CommandLineInterface(UserInterface):
    def show_actions(self, actions: list):
        while True:
            prompt = "[Contacts]: what do you want to do ?\n"
            for i in range(len(actions)):
                prompt += f"[{i}]: {actions[i]}\n"

            action_index = int(input(prompt))

            if action_index in actions:
                return actions[action_index]

            print("Please specify valid action")
