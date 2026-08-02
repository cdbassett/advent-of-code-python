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
# [Advent of Code 2016 - Day 19](https://adventofcode.com/2016/day/19)

# %% [markdown]
# # Imports

# %%
# %load_ext autoreload

# %%
from collections import *

from icecream import ic
import pyperclip

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module


# %% [markdown]
# # Parse

# %%
#Disk = namedtuple("Disk","pos_count,t0pos")

def parse_line(line):
    return line

def parse(inp):
    #return seq(inp.strip().split("\n")).map(parse_line).list()
    return int(inp.strip())


# %% [markdown]
# # Process

# %%
"""/**
 * @param n the number of people standing in the circle
 * @return the safe position who will survive the execution
 *   f(N) = 2L + 1 where N =2^M + L and 0 <= L < 2^M
 */"""
def getSafePosition(n):
    # find value of L for the equation
    #valueOfL = n - Integer.highestOneBit(n);
    valueOfL = n - (1 << (n.bit_length() - 1))
    #rint(valueOfL)
    return 2 * valueOfL + 1;

getSafePosition(5)


# %%
def process(parsed):
    ics(parsed)
    return getSafePosition(parsed)


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    ics(parsed)
    i = 1

    while i * 3 < parsed:
        i *= 3

    return parsed - i

def part2(inp):
    parsed = parse(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
part1("5")
part2("5")

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)
