from common.item import Item
from common.entity_storage import EntityStorage
from common.base_interface import BaseInterface


class BaseManager:
    methods = {}

    def __init__(self, storage: EntityStorage, user_interface: BaseInterface) -> None:
        self.book = storage.load()

        self.user_interface = user_interface

        self.storage = storage

        self.user_interface.clear()

    def _update_item_list(self, item: Item, field: str, label: str):
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

            while True:
                new_entry = self.user_interface.input(
                    f"Enter replacement for {old_entry}:")
                try:
                    item.list_field_replace(field, old_entry, new_entry)
                    return
                except ValueError:
                    self.user_interface.error(f"Please enter valid value")

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

    def _set_item_value(self, item: Item, field: str, label: str, message: str):
        while True:
            value = self.user_interface.input(message)
            try:
                setattr(item, field, value)
            except ValueError:
                self.user_interface.error(f'Incorrect value for {label}')
            else:
                break
