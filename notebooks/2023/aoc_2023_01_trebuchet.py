# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% editable=false jupyter={"source_hidden": true}
from utils.aoc_utils import *
if is_notebook():
    print(get_aoc_url())

# %%
# %load_ext autoreload

# %%
from collections import *

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module

# %%
sample_data1 = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""
sample_data2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""


# %%
def parse(inp):
    return inp.strip().split("\n")


# %% [markdown]
# # Process

# %%
def digits(s):
    return "".join(c for c in s if c.isdigit())

def process(parsed):
    only_digits = [digits(s) for s in parsed]
    vals = [int(s[0]+s[-1]) for s in only_digits]
    return sum(vals)


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
digit_names = "one,two,three,four,five,six,seven,eight,nine".split(",")

def pull_one(line, index, func, next_string):
    first = None
    s = line

    while first is None:
        if s[index].isdigit():
            first = s[index]
        else:
            for n, name in enumerate(digit_names, 1):
                if func(s, name):
                    first = str(n)
                    break
        s = next_string(s)
    return first

def process_line(line):
    first = pull_one(line, 0, lambda s, name: s.startswith(name), lambda s: s[1:])
    second = pull_one(line, -1, lambda s, name: s.endswith(name), lambda s: s[:-1])
    ics(line, first, second)
    return first+second

def process2(parsed):
    only_digits = [process_line(s) for s in parsed]
    vals = [int(s[0]+s[-1]) for s in only_digits]
    return sum(vals)


# %%
def part2(inp):
    parsed = parse(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
part1(sample_data1)
part2(sample_data2)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)

# %%
