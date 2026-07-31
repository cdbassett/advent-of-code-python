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
from aoc_utils import *
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
from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module

# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0]
sample_data2 = "dabAcCaCBAcCcaDA"

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


def char_reduce(l):
    if 0:
        # excessive list deletions meant I quit trying after 10 monutes, new method took 3 seconds
        new_chars = l[:]
        n = 0

        while n < len(new_chars)-1:
            if is_pair(new_chars[n], new_chars[n+1]):
                del new_chars[n:n+2]
                n -= 1
                continue
            n += 1
    else:
        inter_chars = list(flatten(p for p in pairs(l) if len(p) == 1 or not is_pair(*p)))
        #ics(l, inter_chars)

        if inter_chars:
            new_chars = list(flatten(p for p in pairs(inter_chars, 1) if len(p) == 1 or not is_pair(*p)))
            #ics(inter_chars, new_chars)
        else:
            new_chars = inter_chars

    return new_chars

def full_reduce(chars):
    old_len = len(chars)
    iterations = 0

    while (new_len := len(new_chars := char_reduce(chars))) < old_len:
        iterations += 1
        #ic(iterations, len(chars), len(new_chars))
        #ics(chars, new_chars)
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
    part1(sample_data1)

part2(sample_data2)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)
