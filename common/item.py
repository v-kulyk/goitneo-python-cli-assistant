
class Item:
    searchable_fields = {}
    orderable_fields = {}
    fillable_fields = {}
    validators = {}

    def list_field_replace(self, field: str, old_value, new_value):
        prop_list = getattr(self, '_'+field)

        if not isinstance(prop_list, list):
            raise TypeError

        idx = prop_list.index(old_value)

        if not old_value or idx < 0:
            return

        if not new_value or (field in self.validators and not self.validators[field](new_value)):
            raise ValueError

        prop_list[idx] = new_value
        setattr(self, '_'+field, prop_list)

    def list_field_delete(self, field: str, value):
        prop_list = getattr(self, '_'+field)

        if not isinstance(prop_list, list):
            raise TypeError

        prop_list.remove(value)
        setattr(self, '_'+field, prop_list)
