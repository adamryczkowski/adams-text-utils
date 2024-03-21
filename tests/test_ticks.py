from adams_text_utils import *


def test_ticks():
    value = 1234
    for item in int_tick_iterator(value, direction_up=False):
        print(item)

    items = list(int_tick_iterator(value, direction_up=True))
    assert items == [1235, 1240, 1250, 1300, 1500, 2000, 5000, 10000]

    items = list(int_tick_iterator(value, direction_up=False))
    assert items == [1232, 1231, 1230, 1220, 1210, 1200, 1100, 1000]

if __name__ == '__main__':
    test_ticks()