from typing import Iterator


def int_tick_iterator(number: int, direction_up: bool) -> Iterator[int]:
    """
    Starting with an integer, produces progressively simpler integers by simplifying the last non-zero digit.
    The algorithm can be extended to handle decimal numbers.
    """
    assert isinstance(number, int)
    assert number > 0
    number = str(number)

    def is_done(number_str: str) -> bool:
        return number_str[0] == '1' and all([x == "0" for x in number_str[1:]])

    while not is_done(number):
        last_digit_pos = number.find("0")
        if last_digit_pos == -1:
            last_digit_pos = len(number)
        last_digit_pos -= 1
        last_digit = int(number[last_digit_pos])

        if direction_up:
            if last_digit == 1:
                number = number[:last_digit_pos] + "2" + "0" * (len(number) - last_digit_pos - 1)
            elif last_digit >= 2 and last_digit <= 4:
                number = number[:last_digit_pos] + "5" + "0" * (len(number) - last_digit_pos - 1)
            elif last_digit >= 5:
                if last_digit_pos == 0:
                    number = "1" + "0" * len(number)
                else:
                    number = str(int(number[:last_digit_pos]) + 1) + "0" * (len(number) - last_digit_pos)
        else:
            if last_digit == 1:
                number = number[:last_digit_pos] + "0" * (len(number) - last_digit_pos)
            elif last_digit == 2:
                number = number[:last_digit_pos] + "1" + "0" * (len(number) - last_digit_pos - 1)
            elif last_digit >= 3 and last_digit <= 5:
                number = number[:last_digit_pos] + "2" + "0" * (len(number) - last_digit_pos - 1)
            else:
                # number = str(int(number[:last_digit_pos]) - 1) + "0" * (len(number) - last_digit_pos - 1)
                number = number[:last_digit_pos] + "5" + "0" * (len(number) - last_digit_pos - 1)
        yield int(number)
