
class SearchRequest:
    def __init__(self) -> None:
        self.search = ''
        self.field = None
        self.sort_by = None
        self.is_descending = None

    def is_found(self, record) -> bool:
        if self.field:
            attr = getattr(record, self.field)
            return isinstance(attr, str) and self.search.casefold().lower() in attr.casefold().lower()

        if record.searchable_fields:
            properties = record.searchable_fields.keys()
        else:
            properties = list(
                map(lambda p: not p.startswith('_'), dir(record)))

        for prop in properties:
            if not prop:
                continue

            attr = getattr(record, prop)
            if isinstance(attr, str) and self.search.casefold().lower() in attr.casefold().lower():
                return True

            if isinstance(attr, list):
                for item in attr:
                    if isinstance(item, str) and self.search.casefold().lower() in item.casefold().lower():
                        return True

        return False

    def sort(self, records: list) -> list:
        if not self.sort_by:
            return records
        
        records.sort(key=lambda r: getattr(r, self.sort_by))

        if self.is_descending:
            records.reverse()

        return records
