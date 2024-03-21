from adams_text_utils import *


def test1():
    col1 = ["a", "b", "c"]
    col2 = ["Alice", "Bob", "Charlie"]
    col3 = [12.345, 0.123, 0.000123]

    tab = print_table([col1, col2, col3], 1)
    print("\n".join(tab))
    assert tab == [
        "a Alice   12.345   ",
        "b Bob     0.123    ",
        "c Charlie 0.000123 ",
    ]


if __name__ == '__main__':
    test1()