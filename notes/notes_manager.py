from notes.note import Note
from notes.user_interfaces import UserInterface
from notes.storage import Storage

from datetime import date, datetime


class NotesManager:
    methods = {
        'find_item': 'Search',
        'list_items': 'List all items',
        'add_item': "New item",
        'change_item': "Edit item",
        'remove_item': "Delete item",       
        'exit': 'Exit',
    }

    def __init__(self, storage: Storage, user_interface: UserInterface) -> None:
        self.items = storage.load()
        self.user_interface = user_interface
        self.storage = storage
        self.user_interface.clear()

    def run(self):
        method_idx = self.user_interface.choose(
            list(self.methods.values()),
            "[Notes]: what do you want to do ?",
            "Please specify a valid action"
        )
        method_name = list(self.methods.keys())[method_idx]
        method = getattr(self, method_name)
        method()

    def list_items(self):
        self.user_interface.clear()
        items = self.items.data.values()
        self.user_interface.show_items(items)

        self.run()

    def add_item(self):
        self.user_interface.clear()
        item = self.user_interface.new_item()
        self.items.add(item)
        self.storage.save(self.items)
        self.user_interface.item_added(item)
        self.run()

    def find_item(self) -> Note:
        self.user_interface.clear()
        search_request = self.user_interface.get_search_request()
        items = self.items.find(search_request)
        self.user_interface.show_items(items)
        self.run()

    def change_item(self):
        self.user_interface.clear()
        items = list(self.items.data.values())
        item = self.user_interface.select_item(items)

        attrs_dict = Note.fillable_fields

        field_idx = self.user_interface.choose(
            list(attrs_dict.values()),
            "Which field do you want to change?",
            "Please select a valid field."
        )

        field = list(attrs_dict.keys())[field_idx]
        label = attrs_dict[field]
        current_value = getattr(item, field)
       
        if isinstance(current_value, list):
            self._update_item_list(item, field, label)
        else:
            message = f"[Change note] Please specify new value for {label}: {current_value}"
            self._set_item_value(item, field, label, message)

        self.storage.save(self.items)

        self.user_interface.item_changed(item)

        self.run()

    def remove_item(self):
        self.user_interface.clear()

        items = list(self.items.data.values())
        item = self.user_interface.select_item(items)

        self.items.delete(item.id)

        self.storage.save(self.items)

        self.user_interface.item_removed()

        self.run()



    def exit(self):
        pass

    def _update_item_list(self, item: Note, field: str, label: str):
        current_value = getattr(item, field)
        action = self._get_list_action(label)

        if action == 'add':
            self._set_item_value(item, field, label,
                                   f"[{label}] Please add new entry")
        elif action == 'delete':
            idx = self.user_interface.choose(
                current_value,
                "Which entry do you want to delete?",
                "Please select a valid entry."
            )

            item.list_field_delete(field, current_value[idx])

        elif action == 'edit':
            idx = self.user_interface.choose(
                current_value,
                "Which entry do you want to change?",
                "Please select a valid entry."
            )

            old_entry = current_value[idx]
            new_entry = self.user_interface.input(
                f"Enter replacement for {old_entry}:")

            item.list_field_replace(field, old_entry, new_entry)

    def _get_list_action(self, label: str) -> str:
        actions = {
            'add': 'Add',
            'edit': 'Edit',
            'delete': 'Delete',
        }

        action_idx = self.user_interface.choose(
            list(actions.values()),
            f"Choose action for {label}:",
            "Please select a valid action."
        )

        return list(actions.keys())[action_idx]

    def _set_item_value(self, item: Note, field: str, label: str, message: str):
        while True:
            value = self.user_interface.input(message)

            try:
                setattr(item, field, value)
            except ValueError:
                self.user_interface.error(f'Incorrect value for {label}')
            else:
                break
