from common import BaseManager
from notes.note import Note


class NotesManager(BaseManager):
    methods = {
        'list_items': 'List all notes',
        'find_items': 'Search',
        'filter_items': 'Filter by tag',
        'add_item': "New note",
        'change_item': "Edit note",
        'remove_item': "Delete note",
        'exit': 'Exit',
    }

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
        items = self.book.data.values()
        self.user_interface.show_items(items)
        self.run()

    def add_item(self):
        self.user_interface.clear()
        item = self.user_interface.new_item()
        self.book.add(item)
        self.storage.save(self.book)
        self.user_interface.item_added(item)
        self.run()

    def find_items(self) -> Note:
        self.user_interface.clear()
        search_request = self.user_interface.get_search_request(
            Note.searchable_fields, Note.orderable_fields)
        items = self.book.find(search_request)
        self.user_interface.show_items(items)
        self.run()

    def filter_items(self) -> Note:
        self.user_interface.clear()
        tag = self.user_interface.get_filter_request(self.items)
        items = self.items.filter(tag)
        self.user_interface.show_items(items)
        self.run()

    def change_item(self):
        self.user_interface.clear()
        items = list(self.book.data.values())
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

        self.storage.save(self.book)

        self.user_interface.item_changed(item)

        self.run()

    def remove_item(self):
        self.user_interface.clear()

        items = list(self.book.data.values())
        item = self.user_interface.select_item(items)

        self.book.delete(item.id)

        self.storage.save(self.book)

        self.user_interface.item_removed()

        self.run()

    def exit(self):
        pass
