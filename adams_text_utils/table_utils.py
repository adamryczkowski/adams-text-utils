

def print_table(columns: list[list[str]], space_size: int = 1) -> list[str]:
    """A poor's man text table formatter. No support for alignment customization - only flush left.
    No special handling for tables that are too wide for the page's width.
    Input will be converted to text using the str() function.
    """
    # Get the number of records in the table
    record_count = None
    for col in columns:
        assert isinstance(col, list)
        if record_count is None:
            record_count = len(col)
        else:
            assert len(col) == record_count

    # Get the maximum length of each column
    colsizes = [max([len(str(item)) for item in col]) for col in columns]

    # Create a list of strings, each string is a row in the table
    str_rows = []
    for row in range(record_count):
        str_row = ""
        for i, col in enumerate(columns):
            # Get the string representation of the item
            s = str(col[row])

            # Pad the string with spaces to the maximum length of the column
            item = s + " " * (colsizes[i] - len(s) + space_size)

            # Add the item to the row
            str_row += item

        # Add the row to the list of rows
        str_rows.append(str_row)

    return str_rows
