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
# [Advent of Code 2024 - Day 25](https://adventofcode.com/2024/day/25)

# %% editable=false jupyter={"source_hidden": true}
from utils.aoc_utils import *
if is_notebook():
    print(get_aoc_url())

# %% [markdown]
# # Imports

# %%
# %load_ext autoreload

# %%
import os
import sys
from collections import *
import re
import math

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
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
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0]
sample_data2 = sample_data1


# %% [markdown]
# # Parse

# %%
def parse_line(line):
    return line.strip().split("\n")

def parse_data(inp):
    return seq(inp.strip().split("\n\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def convert(chunk):
    return seq(zip(*chunk)).map(sjoin).map(lambda s: len(s.strip(".")) - 1).to_tuple()

def convert_chunks(l):
    return map_tuple(convert, l)

def fits(key, lock):
    return all(n <= 5 for n in add_tuple(key, lock))

def process(parsed):
    locks, keys = list(), list()
    
    for chunk in parsed:
        dest = locks if chunk[0] == "#####" else keys
        dest.append(chunk)

    locks, keys = map(convert_chunks, (locks, keys))
    ics(keys, locks)
    matches = sum(1 for key, lock in product(keys, locks) if fits(key, lock))
    return matches


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

for sample_data1 in sample_data1s:
    part1(sample_data1)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
