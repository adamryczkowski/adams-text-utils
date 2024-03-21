from adams_text_utils import *

def test_bytes():
    a = human_readable_size(1234567890)
    assert a == "1.15 GiB"
    a = human_readable_size(1234567890, 0)
    assert a == "1 GiB"

    a = human_readable_size(1234567890, 3)
    assert a == "1.150 GiB"

    a = human_readable_size(1234567890, 4)
    assert a == "1.1498 GiB"

    a = human_readable_size(1, 4)
    assert a == "1.0000 B"

    a = human_readable_size(123456789012345, 2)
    assert a == "112.28 TiB"

def test_list():
    l = ["a", "b", "c"]
    a = format_txt_list(l)
    assert a == "a, b and c"

    l = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]
    a = format_txt_list(l)
    assert a == "a, b, c, d, e, f, g, h, i, j and k"

    a = format_txt_list(l, 3)
    assert a == "a, b, c, … , k"

    a = format_txt_list(l, 2)
    assert a == "a, b, … , k"

def test_noun():
    assert format_noun_with_number("apple", 1) == "1 apple"
    assert format_noun_with_number("apple", 0) == "no apples"
    assert format_noun_with_number("apple", 2) == "2 apples"

def test_ordinal():
    assert make_ordinal(1) == "1st"
    assert make_ordinal(2) == "2nd"
    assert make_ordinal(3) == "3rd"
    assert make_ordinal(4) == "4th"
    assert make_ordinal(11) == "11th"
    assert make_ordinal(12) == "12th"
    assert make_ordinal(21) == "21st"
    assert make_ordinal(22) == "22nd"
    assert make_ordinal(23) == "23rd"
    assert make_ordinal(24) == "24th"
    assert make_ordinal(101) == "101st"
    assert make_ordinal(0) == "0th"

def test_quotes():
    txt1 = "-q"
    txt2 = ""
    assert "cmd" + quote_with_space(txt1) == "cmd -q"
    assert "cmd" + quote_with_space(txt2) == "cmd"

    txt1 = "I like it!"
    txt2 = "I don't like 'this'"
    txt3 = "What is \"this\"?"
    txt4 = "She asked: \"what is 'this'?\"."

    assert quote(txt1) == "\"I like it!\""
    assert quote(txt2) == "\"I don't like 'this'\""
    assert quote(txt3) == "'What is \"this\"?'"
    assert quote(txt4) == "«She asked: \"what is 'this'?\".»"


if __name__ == '__main__':
    test_bytes()
    test_list()
    test_noun()
    test_ordinal()
    test_quotes()