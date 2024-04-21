# Random text python utilities, that I found missing in the standard library.


Adams Text Utils is a Python library that provides various text processing utilities. These utilities can be used in various projects for processing and formatting text.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

This project uses poetry for dependency management. You can install it with:

```bash
pip install poetry
```

Then, you can install the project dependencies with:

```bash
poetry install
```

## Usage

### Pretty-formatted numpy arrays

The `pretty_numpy` function pretty-prints a numpy array. It takes a numpy array as input and returns a string with the array formatted in a human-readable format.

```python
import numpy as np
from adams_text_utils import dump_ndarray_precision
arr = np.asarray([[0.01346473, 0.22654731, 0.24858536],
                      [0.64985173, 0.8378816, 0.6764337],
                      [0.77706594, 0.48403015, 0.51463447]])
print(dump_ndarray_precision(arr, precision=2, indent_size=0))
# Prints:
# [[0.01, 0.23, 0.25],
#  [0.65, 0.84, 0.68],
#  [0.78, 0.48, 0.51]]

print(dump_ndarray_precision(arr, precision=2, indent_size=0, big_indent_size=3))
# Prints:
# [[
#    0.01, 0.23, 0.25
# ], [
#    0.65, 0.84, 0.68
# ], [
#    0.78, 0.48, 0.51
# ]]

arr3d = np.random.rand(2,3,4)
print(dump_ndarray_precision(arr3d, precision=2, indent_size=0))
# Prints:
# [[[0.07, 0.70, 0.44, 0.46],
#   [0.30, 0.38, 0.98, 0.02],
#   [0.67, 0.97, 0.85, 0.37]]
# ,
#  [[0.01, 0.41, 0.01, 0.24],
#   [0.34, 0.38, 0.33, 0.58],
#   [0.58, 0.20, 0.72, 0.64]]
# ]



```

Sometimes the values are rational, and would be better (or more concise) represented as fractions. The `dump_ndarray_precision` function can also handle this case. Internally, it uses the `fractions` module to convert the values to fractions.

```python
import numpy as np
from adams_text_utils import dump_ndarray_rational
arr = np.asarray([[0.01346473, 0.22654731, 0.24858536],
                      [0.64985173, 0.8378816, 0.6764337],
                      [0.77706594, 0.48403015, 0.51463447]])

print(dump_ndarray_rational(arr, max_denominator=50, indent_size=3))
# Prints:
#   [[1/50, 5/22, 1/4],
#    [13/20, 31/37, 23/34],
#    [7/9, 15/31, 18/35]]

```


### Human Readable Size

The `human_readable_size` function converts a size in bytes into a human-readable format. It takes two arguments: the size in bytes and the number of decimal places to use in the output.

```python
from adams_text_utils import human_readable_size

print(human_readable_size(1234567890))  # Outputs: 1.15 GiB
```

### Format Text List

The format_txt_list function formats a list of strings into a single string with items separated by commas and the last two items separated by 'and'.

```python
from adams_text_utils import format_txt_list

print(format_txt_list(["a", "b", "c"]))  # Outputs: a, b and c
```

### Format Noun with Number

The format_noun_with_number function formats a noun with a number, taking into account the plural form of the noun.  

Example:

```python
from adams_text_utils import format_noun_with_number

print(format_noun_with_number("apple", 1))  # Outputs: 1 apple
print(format_noun_with_number("apple", 2))  # Outputs: 2 apples
print(format_noun_with_number("apple", 0))  # Outputs: "no apples"
```

### Make Ordinal

The make_ordinal function converts a number into its ordinal form.

```python
from adams_text_utils import make_ordinal

print(f'"{make_ordinal(1)}"')  # Outputs: "1st"
```

### Quote with Space
    
The quote_with_space function adds a space before a string and quotes it if it contains spaces.

Useful for command-line arguments that may or may not be present.

```python
from adams_text_utils import quote_with_space

def command_line(cond:bool)->str:
    if cond:
        flag1 = "-q"
        flag2 = ""
    else:
        flag1 = ""
        flag2 = "-a"
    return f"/bin/prog -x{quote_with_space(flag1)}{quote_with_space(flag2)} -f /path/to/file"

print(f'"{command_line(True)}"')  # Outputs: "/bin/prog -x -q -f /path/to/file"
print(f'"{command_line(False)}"')  # Outputs: "/bin/prog -x -a -f /path/to/file"
```

### Format Text List

The format_txt_list function formats a list of strings into a single string with items separated by commas and the last two items separated by 'and'.

```python
from adams_text_utils import format_txt_list

print(format_txt_list(["a", "b", "c"]))  # Outputs: a, b and c

l = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]
print(format_txt_list(l))  # Outputs: "a, b, c, d, e, f, g, h, i, j and k"
print(format_txt_list(l, max_length=5))  # Outputs: "a, b, c, … , k"
print(format_txt_list(l, max_length=3))  # Outputs: "a, … , k"
```

### Pretty rounded range

The `pretty_chart_ticks` function generates a list of progressively rounded numbers that span a range that covers a given integer. 

```python

from adams_text_utils import int_tick_iterator, format_txt_list

value = 1234 # The value to be covered by the range

left_bounds = list(int_tick_iterator(value, direction_up=False))
right_bounds = list(int_tick_iterator(value, direction_up=True))

format_txt_list([str(x) for x in left_bounds])
# Outputs: "1232, 1231, 1230, 1220, 1210, 1200, 1100 and 1000"
format_txt_list([str(x) for x in right_bounds])
# Outputs: "1235, 1240, 1250, 1300, 1500, 2000, 5000 and 10000"

# These are the progressively more rounded numbers that span the range that covers 1234:
# 1232 <= 1234 <= 1235
# 1231 <= 1234 <= 1240
# 1230 <= 1234 <= 1240
# 1220 <= 1234 <= 1250
# 1210 <= 1234 <= 1300
# 1200 <= 1234 <= 1300
# 1100 <= 1234 <= 1500
# 1000 <= 1234 <= 1500
# 1000 <= 1234 <= 2000
# 1000 <= 1234 <= 5000
# 1000 <= 1234 <= 10000

```
