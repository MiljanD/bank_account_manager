from prettytable import PrettyTable

class Display:
    """
    Utility class for formatting and displaying data in tabular form
    using PrettyTable. Supports single records (dict) and multiple
    records (list of dicts).
    """
    def __init__(self):
        """Initialize Display with a PrettyTable instance."""
        self.table = PrettyTable()


    def _display_record(self, data) -> None:
        """
        Display a single record (dict) in tabular format.
        :param data:Dictionary representing one record.
        """
        self.table.clear()
        clean_column_names = [col.replace("_", " ").title() for col, row in data.items()]
        clean_row = [row for col, row in data.items()]

        self.table.field_names = clean_column_names
        self.table.add_row(clean_row)

        print(self.table)

    def _display_multi_records(self, data) -> None:
        """
        Display multiple records (list of dicts) in tabular format.
        :param data: List of dictionaries representing multiple records.
        """
        self.table.clear()
        column_names = [ record.replace("_", " ").title() for record in data[0]]
        rows = [[value for key, value in record.items()] for record in data]
        self.table.field_names = column_names
        for row in rows:
            self.table.add_row(row)

        print(self.table)


    def _check_data_type(self, data) -> str|None:
        """
        Determine the type of data provided.
        :param data: Input data (dict or list of dicts).
        :return: 'dict', 'list', or None if empty/unsupported.
        """
        if isinstance(data, list) and data:
            return "list"
        elif isinstance(data, dict) and data:
            return "dict"
        return None


    def display_content(self, data) -> None:
        """
        Central method for displaying data.
        Delegates to the appropriate private method based on input type.
        :param data: Dictionary or list of dictionaries to display.
        """
        match self._check_data_type(data):
            case "dict":
                self._display_record(data)
            case "list":
                self._display_multi_records(data)
            case _:
                print("No content to display!")

