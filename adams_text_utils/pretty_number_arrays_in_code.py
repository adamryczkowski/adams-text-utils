from fractions import Fraction
from typing import Iterator

import numpy as np
from .tick_iterator import int_tick_iterator


class ListWriter:
    _lines: list[list[str]]
    _line_items: list[str]
    _max_line_size: int
    _indent_size: int
    _first_line: str
    _comma: str
    _brackets: tuple[str, str]
    _big_indent: bool
    _big_indent_size: int

    def __init__(self, indent_size: int, first_line: str, max_line_size: int, big_indent_size: int = None,
                 comma: str = ", ", brackets: tuple[str, str] = ("[", "]")):
        assert len(brackets) == 2
        assert indent_size + len(first_line) + len(brackets[0]) + len(brackets[0]) + len(brackets[1]) + len(
            brackets[1]) < max_line_size
        assert isinstance(indent_size, int)
        assert isinstance(max_line_size, int)
        assert isinstance(first_line, str)
        assert isinstance(comma, str)
        assert isinstance(brackets, tuple)
        assert isinstance(brackets[0], str)
        assert isinstance(brackets[1], str)

        self._big_indent = big_indent_size is not None
        if self._big_indent:
            assert isinstance(big_indent_size, int)
            self._big_indent_size = big_indent_size
        else:
            self._big_indent_size = -1

        self._lines = []
        self._line_items = []
        self._max_line_size = max_line_size
        self._indent_size = indent_size
        self._first_line = first_line
        self._comma = comma
        self._brackets = brackets

    def last_line_size(self, is_eoi: bool) -> int:
        size = self._indent_size
        if len(self._line_items) == 0:
            if not self._big_indent:
                size += len(self._first_line)
            size += len(self._brackets[0])
        else:
            if self._big_indent:
                size += self._big_indent_size
            else:
                size += len(self._first_line)

        size += len(self._line_items) - 1 * len(self._comma) + sum([len(x) for x in self._line_items])

        if is_eoi:
            size += len(self._brackets[1])
        else:
            size += len(self._comma)

        return size

    def add_item(self, item: str, eoi: bool = False):
        if len(self._line_items) == 0 and len(self._lines) > 0:
            self._line_items.append(item)  # Each empty line should hold at least one item
            return

        if self.last_line_size(eoi) > self._max_line_size:
            self._line_items.pop()
            self._lines.append(self._line_items)
            self._line_items = []
            assert self.last_line_size(eoi) <= self._max_line_size
            self._line_items.append(item)

    def get_lines(self) -> list[tuple[str, int]]:
        """
        Returns the list of lines and the number of items in each line.
        :return:
        """
        if len(self._line_items) > 0:
            self._lines.append(self._line_items)
            self._line_items = []

        out = []
        if self._big_indent:
            out.append((" " * self._indent_size + self._first_line + self._brackets[0], 0))
        last_line = ""
        for i, line in enumerate(self._lines):
            if self._big_indent:
                last_line += " " * (self._big_indent_size + self._indent_size)
            else:
                if i == 0:
                    last_line += " " * self._indent_size + self._first_line + self._brackets[0]
                else:
                    last_line += " " * (self._indent_size + len(self._first_line) + len(self._brackets[0]))

            last_line += self._comma.join(line)
            if i == len(self._lines) - 1:
                last_line += self._brackets[1]
            else:
                last_line += self._comma
            out.append((last_line, len(line)))
        return out


def format_ndarray_custom_fixed_tabs(array: np.ndarray, indent_size: int, first_line: str = "",
                                     big_indent_size: int = None,
                                     comma: str = ", ", brackets: tuple[str, str] = ("[", "]"),
                                     max_line_size: int = 96,
                                     how_important_good_column_size: int = 3,
                                     no_finishing_bracket: bool = False) -> str:
    if len(array.shape) > 1:
        # We are going to split each dimension along the first axis and format each of them separately
        out = []
        items = []
        suffix = ""
        local_big_indent_size = big_indent_size
        local_first_line = first_line
        if big_indent_size is not None:
            local_brackets = ("", "")
        else:
            local_brackets = brackets
        for i in range(array.shape[0]):
            if big_indent_size is None:
                if i == 0:
                    local_first_line = first_line + "["
                else:
                    local_first_line = " " * (len(first_line) + 1)
            else:
                if i == 0:
                    local_first_line = first_line + "[["
                else:
                    local_big_indent_size = None
                    local_first_line = " " * big_indent_size

            # if i == 0:
            #     if big_indent_size is None:
            #         local_first_line = first_line + "["
            #     else:
            #         local_first_line = first_line + "[["
            # else:
            #     if big_indent_size is None:
            #         if i > 0:
            #             local_first_line = ""
            #     else:
            #         if i > 0:
            #             local_first_line = ""
            # if big_indent_size is not None:
            #     if i > 0:
            #         local_big_indent_size = None
            #         local_first_line = " " * big_indent_size

            items.append(format_ndarray_custom_fixed_tabs(array[i], indent_size=indent_size,
                                                          first_line=local_first_line,
                                                          big_indent_size=local_big_indent_size,
                                                          comma=comma, brackets=local_brackets,
                                                          max_line_size=max_line_size,
                                                          how_important_good_column_size=how_important_good_column_size) + suffix)

        if big_indent_size is None:
            intra_indent = indent_size + len(local_first_line) - 1
            infix = ",\n"
            suffix = "]\n"
        else:
            intra_indent = indent_size
            infix = "\n" + " " * intra_indent + "], [\n"
            suffix = "\n" + " " * intra_indent + "]]\n"
        out = infix.join(items)
        out += suffix
        return out
    if isinstance(array, np.ndarray):
        assert len(array.shape) == 1
    array = [str(i) for i in array]
    raw_length = sum([len(i) for i in array]) + (len(array) - 1) * len(comma)
    avg_item_size = raw_length / len(array)

    min_item_size = int(np.floor(max_line_size * 0.8 / avg_item_size))
    max_item_size = int(np.ceil(max_line_size * 1.1 / avg_item_size))
    avg_item_size = int(np.round(max_line_size / avg_item_size))
    column_sizes_to_try = {i for i in range(min_item_size, max_item_size + 1)}
    extra_sizes_up = {i for i in int_tick_iterator(avg_item_size, True)}
    extra_sizes_down = {i for i in int_tick_iterator(avg_item_size, False)}
    column_sizes_to_try = column_sizes_to_try.union(extra_sizes_up).union(extra_sizes_down)

    best_quality = -np.inf
    best_break = []
    for items_per_line in column_sizes_to_try:
        check, padded_items = format_ndarray_custom_fixed_tabs_(array, indent_size=indent_size,
                                                                first_line=first_line,
                                                                items_per_line=items_per_line,
                                                                big_indent_size=big_indent_size,
                                                                comma=comma,
                                                                brackets=brackets,
                                                                no_finishing_bracket=no_finishing_bracket)
        waste = sum([len(x) - len(y) for x, y in zip(padded_items, array)]) / sum(
            [len(x) for x in check])  # What percent of the total space is wasted for the padding
        line_sizes = [len(x) for x in check]
        if max(line_sizes) > max_line_size:
            continue

        # Bonus for number of digits in the number of lines; i.e. the more rounded the value, the more bonus we get:
        digit_count = list_size_not_rounded_penalty(items_per_line)

        quality = -len(
            check) - waste * 5 - digit_count * how_important_good_column_size  # The more lines, the worse. Waste of 20% of the space counts the same as adding 1 line.

        if quality > best_quality:
            best_quality = quality
            best_break = check

    return "\n".join(best_break)


def list_size_not_rounded_penalty(list_size: int) -> float:
    # Size of the train of zeroes on the right size:
    assert isinstance(list_size, int)
    assert list_size > 0

    # Each zero at the end of the list is not penalized
    # Numbers with a leading 1, 2 or 5 and then only zeroes are not penalized
    # Least significant digit 1, 2 and 5 is penalized as 0.5
    # All other numbers are penalized as 1

    last_digit_pos = str(list_size).find("0")
    if last_digit_pos == -1:
        last_digit_pos = len(str(list_size))

    last_digit_pos -= 1
    last_digit = int(str(list_size)[last_digit_pos])
    penalty = 0
    last_item_is_rounded = last_digit == 1 or last_digit == 5 or last_digit == 2
    if last_item_is_rounded:
        penalty = 0.5
    else:
        penalty = 1
    penalty += last_digit_pos - 0.5
    return penalty




def format_ndarray_custom_fixed_tabs_(array: np.ndarray | list[str], indent_size: int, first_line: str,
                                      items_per_line: int,
                                      big_indent_size: int = None,
                                      comma: str = ", ", brackets: tuple[str, str] = ("[", "]"),
                                      no_finishing_bracket: bool = False) -> tuple[
    list[str], list[str]]:
    item_sizes = np.zeros(items_per_line, dtype=int)
    lines = []
    for i in range(int(np.ceil(len(array) / items_per_line))):
        line = []
        for j in range(items_per_line):
            if i * items_per_line + j >= len(array):
                break
            item = str(array[i * items_per_line + j])
            item_sizes[j] = max(int(item_sizes[j]), len(item))
            line.append(item)
        lines.append(line)

    for i in range(len(lines)):
        for j in range(len(lines[i])):
            lines[i][j] = lines[i][j].rjust(item_sizes[j])

    # flattened version of 2-dimensional list "lines"
    flattened_lines = [item for sublist in lines for item in sublist]

    out = []
    if big_indent_size is not None:
        out.append(" " * indent_size + first_line + brackets[0])
    for i, line in enumerate(lines):
        last_line = ""
        if big_indent_size is not None:
            last_line += " " * (big_indent_size + indent_size)
        else:
            if i == 0:
                last_line += " " * indent_size + first_line + brackets[0]
            else:
                last_line += " " * (indent_size + len(first_line) + len(brackets[0]))

        last_line += comma.join(line)
        if i == len(lines) - 1 and not no_finishing_bracket:
            last_line += brackets[1]
        else:
            last_line += comma
        out.append((last_line))
    return out, flattened_lines


def dump_ndarray_custom_inline(generator: Iterator[str], line_prefix: int, first_line: str, max_line_size: int = 96) -> \
        list[tuple[str, int]]:
    """
    Generic procedure that formats the array using the generator in 1-pass fashion.
    Assumes the generator does not produce '\n' characters. It may not be suitable for higher-dimensional arrays.
    Each line will contain at least one element.
    :param generator: The generator that produces formated output of each element of the array.
    :param line_prefix: Number of spaces to be added to each line (to match the indentation)
    :param first_line: The prefix of the first line of the output. Excludes indentation. Something like "my_array = ".
    :param max_line_size: The size of the line, after which the line is broken into the next line.
    :return: List of pairs (line, number of elements) that can be joined with '\n' character.
    """
    out = []
    first_line = first_line + "["
    while True:
        item_count = 0
        try:
            item = next(generator)
        except StopIteration:
            break
        if len(out) == 0:
            line = " " * line_prefix + first_line
        else:
            line = " " * line_prefix
        while True:
            if len(line) + len(item) + 2 > max_line_size and item_count > 0:
                break
            item_count += 1
            line += item + ", "
            try:
                item = next(generator)
            except StopIteration:
                line += item + "]"
                break

        out.append((line, item_count))

    return out


def dump_ndarray_precision(array: np.ndarray, precision: int, indent_size: int,
                           first_line: str = "", big_indent_size: int = None,
                           comma: str = ", ", brackets: tuple[str, str] = ("[", "]"),
                           max_line_size: int = 96,
                           how_important_good_column_size: int = 3) -> str:
    """Dumps the ndarray in the precision form.
    """
    array = np.vectorize(lambda x: f"{x:.{precision}f}")(array)
    return format_ndarray_custom_fixed_tabs(array, indent_size, first_line, big_indent_size, comma, brackets,
                                            max_line_size, how_important_good_column_size)


def dump_ndarray_int(array: np.ndarray, indent_size: int, first_line: str = "",
                     big_indent_size: int = None,
                     comma: str = ", ", brackets: tuple[str, str] = ("[", "]"),
                     max_line_size: int = 96,
                     how_important_good_column_size: int = 3) -> str:
    """Dumps the ndarray in the precision form.
    """
    array = np.vectorize(lambda x: f"{int(x)}")(array)
    return format_ndarray_custom_fixed_tabs(array, indent_size, first_line, big_indent_size, comma, brackets,
                                            max_line_size, how_important_good_column_size)


def dump_ndarray_relative_precision(array: np.ndarray, indent_size: int, significant_digits: int = 2,
                                    first_line: str = "",
                                    big_indent_size: int = None,
                                    comma: str = ", ", brackets: tuple[str, str] = ("[", "]"),
                                    max_line_size: int = 96,
                                    how_important_good_column_size: int = 3) -> str:
    """Dumps the ndarray in the precision form. The precision is relative to the smallest value in the array,
    and is expressed in the number of significant digits.
    The output is either a one-line or multi-line string, depending on the length of the array and the max_line_size.
    """
    min_value = np.min(np.abs(array))
    if np.isclose(min_value, 0):
        precision = significant_digits
    else:
        precision = -int(np.ceil(np.log10(min_value))) + significant_digits
    return dump_ndarray_precision(array, precision, indent_size, first_line, big_indent_size, comma, brackets,
                                  max_line_size, how_important_good_column_size)


def dump_ndarray_rational(array: np.ndarray, indent_size: int, max_denominator: int = 1000,
                          first_line: str = "", big_indent_size: int = None,
                          comma: str = ", ", brackets: tuple[str, str] = ("[", "]"),
                          max_line_size: int = 96,
                          how_important_good_column_size: int = 3) -> str:
    """Dumps the ndarray in the rational form"""
    array = np.vectorize(lambda x: f"{Fraction(x).limit_denominator(max_denominator)}")(array)
    return format_ndarray_custom_fixed_tabs(array, indent_size, first_line, big_indent_size, comma, brackets,
                                            max_line_size, how_important_good_column_size)
