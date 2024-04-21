
def human_readable_size(size, decimal_places=2):
    # Credit to: https://stackoverflow.com/a/43690506
    for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB']:
        if size < 1024.0 or unit == 'PiB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def format_txt_list(ltxt: list[str], max_length: int = -1) -> str:
    if len(ltxt) == 0:
        return ""
    if len(ltxt) == 1:
        return ltxt[0]
    else:
        if max_length == -1 or len(ltxt) <= max_length - 2:
            out = ", ".join(ltxt[:-1])
            return out + " and " + ltxt[-1]
        else:
            assert max_length > 3
            max_length -= 2
            ltxt1, ltxt2 = ltxt[0:max_length], ltxt[-1]
            return ", ".join(ltxt1) + ", … , " + ltxt2


def format_noun_with_number(noun: str, number: int) -> str:
    if number == 1:
        return f"1 {noun}"
    elif number == 0:
        return f"no {noun}s"
    else:
        return f"{number} {noun}s"


def make_ordinal(n: int) -> str:
    """
    Convert an integer into its ordinal representation::
    credit: https://stackoverflow.com/a/50992575/1261153
        make_ordinal(0)   => '0th'
        make_ordinal(3)   => '3rd'
        make_ordinal(122) => '122nd'
        make_ordinal(213) => '213th'
    """
    n = int(n)
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix


def quote_with_space(what: str):
    if what is None:
        return ""
    elif what == "":
        return ""
    else:
        return " " + what


def quote(text: str) -> str:
    if text.find('"') == -1:
        return '"' + text + '"'
    if text.find("'") == -1:
        return f"'{text}'"
    else:
        return f"«{text}»"


# def get_repr(obj, quoted: bool, repr_max_size: int = 50) -> str:
#     if isinstance(obj, str):
#         repr_str = obj
#     else:
#         repr_str = repr(obj)
#     repr_str = repr_str.split("\n")[0]
#     if len(repr_str) > repr_max_size:
#         return ""
#     if quoted:
#         return quote(repr_str)
#     return repr_str
