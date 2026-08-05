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

# %% [markdown]
# [Advent of Code 2018 - Day 5](https://adventofcode.com/2018/day/5)

# %% editable=false jupyter={"source_hidden": true}
from utils.aoc_utils import *
if is_notebook():
    print(get_aoc_url())

# %% [markdown]
# # Imports

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
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module

# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
*sample_data1s, sample_data2 = split_example(example)

# %%
for sample in sample_data1s:
    print(sample)
    print("=======================")


# %% [markdown]
# # Parse

# %%
def parse(inp):
    return inp.strip()


# %% [markdown]
# # Process

# %%
def is_pair(c1, c2):
    a, b = (c1, c2) if c1.islower() else (c2, c1)
    return a.islower() and a.upper() == b

def is_pair(c1, c2):
    return abs(ord(c1) - ord(c2)) == 32

def pairs(l, ofs = 0):
    assert ofs in (0, 1)
    length = len(l)-ofs

    if ofs:
        yield [l[0]]

    remainder = length % 2

    yield from batched(l[ofs:ofs + length - remainder], 2)

    if remainder:
        yield [l[-1]]

# remove pairs (upper and lower case of same char next to each other) from the string
def char_reduce(l):
    new_chars = [None] * 50000
    i_new = n = 0
    end = len(l)
    l = list(l) + ["_"]

    try:
        # for n in range(len(l)-1):
        while n < end:                
        # for n in range(len(l)-1):
            c = l[n]

            if is_pair(c, l[n+1]):
                n += 2
                continue

            if i_new and is_pair(c, new_chars[i_new-1]):
                i_new -= 1
                n += 1
                continue

            new_chars[i_new] = c
            i_new += 1
            n += 1
    except IndexError:
        ic(len(l), i_new)
        raise

    return sjoin(new_chars[:i_new])


def full_reduce(chars):
    old_len = len(chars)
    iterations = 0

    while (new_len := len(new_chars := char_reduce(chars))) < old_len:
        iterations += 1
        old_len = new_len
        chars = new_chars
        
    return new_chars

def process(parsed):
    ic(len(parsed))
    ics(parsed)
    chars = list(parsed)
    new_chars = full_reduce(chars)
    return len(new_chars)


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    base_lower = ord("a")
    base_upper = ord("A")
    lengths = []

    for nc in range(26):
        chars = list(replace_multi(parsed, chr(nc + base_lower)+chr(nc + base_upper)))
        #ics(nc, chars)
        new_chars = full_reduce(chars)
        lengths.append(len(new_chars))

    return min(lengths)

def process2(parsed):
    base_lower = ord("a")
    base_upper = ord("A")
    min_length = 10e6 

    for nc in range(26):
        chars = list(replace_multi(parsed, chr(nc + base_lower)+chr(nc + base_upper)))
        #ics(nc, chars)
        new_chars = full_reduce(chars)
        min_length = min(min_length, len(new_chars))

    return min_length


# %%
def part2(inp):
    parsed = parse(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

for sample_data1 in sample_data1s:
    part1(sample_data1) # 0, 0, 4 , 6

part2(sample_data2) # 4

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)
