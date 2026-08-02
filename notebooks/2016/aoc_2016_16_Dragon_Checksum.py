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
# [Advent of Code 2016 - Day 16](https://adventofcode.com/2016/day/16)

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
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module

# %%
sample_data1 = """
10000
"""
sample_data2 = sample_data1

# %%
Disk = namedtuple("Disk","pos_count,t0pos")

def parse_line(line):
    nums = string_to_integers(line)
    return Disk(nums[1], nums[-1])

def parse(inp):
    #return seq(inp.strip().split("\n")).map(parse_line).list()
    return inp.strip()


# %% [markdown]
# # Process

# %%
def flip(s):
    return s.replace("0", "a").replace("1", "0").replace("a", "1")

"""
Call the data you have at this point "a".
Make a copy of "a"; call this copy "b".
Reverse the order of the characters in "b".
In "b", replace all instances of 0 with 1 and all 1s with 0.
The resulting data is "a", then a single 0, then "b".
"""
def transform(s):
    return s + "0" + "".join(reversed(flip(s)))

def checksum(s):
    #ics(seq(list(s)).grouped(2))
    while (len(s) & 1) == 0:
        ics(s)
        s = seq(list(s)).grouped(2).starmap(lambda a, b: "1" if a == b else "0").make_string("")
    return s

def process(parsed, length):
    ics(parsed)
    value = parsed

    while len(value) < length:
        value = transform(value)

    value = value[:length]
    return checksum(value)


# %%
def part1(inp, length):
    parsed = parse(inp)
    result = process(parsed, length)
    print_result(result)


# %%
def part2(inp, length):
    parsed = parse(inp)
    result = process(parsed, length)
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
part1(sample_data1, 20)
#part2(sample_data2)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp, 272)
part2(real_inp, 35651584)
