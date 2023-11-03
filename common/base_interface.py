import readline
from os import system
from common.completer import Completer
from common.search_request import SearchRequest


class BaseInterface:
    def input(self, prompt):
        return input(prompt + "\n>")

    def choose(self, choice_options: list, prompt: str, err_msg: str, default=None) -> str:
        prompt = prompt + "\n"

        self.__set_completer(choice_options)

        while True:
            for i in range(len(choice_options)):
                prompt += f"[{i+1}]: {choice_options[i]}\n"

            user_input = self.input(prompt)

            if not user_input and not default is None:
                self.__unset_completer()
                return default

            if not user_input.isnumeric() and user_input not in choice_options:
                self.error(err_msg)
                continue

            choice_index = int(
                user_input) - 1 if user_input.isnumeric() else choice_options.index(user_input)

            if choice_index >= 0 and choice_index < len(choice_options):
                self.__unset_completer()
                return choice_index

            self.__unset_completer()

            self.error(err_msg)

    def get_search_request(self, searchable_fields: dict, orderable_fields: dict) -> SearchRequest:
        search_request = SearchRequest()

        while True:
            if len(search_request.search) < 2:
                search_request.search = self.input(
                    "[Search]: please, input at least 2 characters\n")
                continue

            if search_request.field is None:
                choice = self.choose(
                    list(searchable_fields.values()),
                    '[Field]: choose where to search:',
                    'Incorrect input',
                    0,
                )
                search_request.field = list(
                    searchable_fields.keys())[choice]
                continue

            if search_request.sort_by is None:
                choice = self.choose(
                    list(orderable_fields.values()),
                    '[Field]: choose the sorting criteria:',
                    'Incorrect input',
                    0,
                )
                search_request.sort_by = list(
                    orderable_fields.keys())[choice]
                continue

            if search_request.is_descending is None:
                choice = self.choose(
                    ['Normal', 'Inverted'],
                    '[Field]: choose the sorting order:',
                    'Incorrect input',
                    0,
                )
                search_request.is_descending = choice > 0
                continue

            return search_request

    def error(self, msg: str):
        print("[ERROR]: " + msg + "\n")

    def show_items(self, items: list):
        print('')

        if not items:
            print('No items found\n')
            return

        for item in items:
            print(item)
            print('')

    def clear(self):
        system('clear')

    def __set_completer(self, options: list):
        completer = Completer(options)

        readline.set_completer(completer.complete)

        readline.parse_and_bind('tab: complete')

    def __unset_completer(self):
        readline.set_completer(None)
