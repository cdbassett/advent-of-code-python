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
# [Advent of Code 2025 - Day 2](https://adventofcode.com/2025/day/2)

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
import iteration_utilities as it_ut

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions # when running standalone, apparently need this import explicitly in main module

# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
example

# %%
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0].replace("\n","")
sample_data1s=[sample_data1]
sample_data2 = sample_data1

# %%
for sample in sample_data1s:
    print(sample)
    print("=======================")


# %% [markdown]
# # Parse

# %%
def parse_line(line):
    return maptuple(int, line.split("-"))

def parse_data(inp):
    return seq(inp.strip().split(",")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def is_invalid(id):
    sid = str(id)
    l = len(sid)
    hl = l // 2
    return hl * 2 == l and sid[:hl] == sid[hl:]

def invalid_count(id_range):
    return seq(range(id_range[0], id_range[1]+1)).filter(is_invalid).sum()

def process(parsed):
    #ics(parsed)
    return seq(parsed).map(invalid_count).sum()


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def invalid_for_length(sid, cnt=2):
    l = len(sid)

    if l % cnt:
        return False

    n = l // cnt    
    # Source - https://stackoverflow.com/a
    # Posted by Tim Zimmermann
    # Retrieved 2025-12-02, License - CC BY-SA 3.0
    parts = [sid[i:i+n] for i in range(0, l, n)]
    first = parts[0]
    return all(p == first for p in parts)

def is_invalid2(id):
    sid = str(id)
    l = len(sid)
    res = any(invalid_for_length(sid, cnt) for cnt in range(2, l+1))
    #ics("   ", id, res)
    return res

def invalid_count2(id_range):
    #ics(id_range)
    return seq(range(id_range[0], id_range[1]+1)).filter(is_invalid2).sum()

def process2(parsed):
    return seq(parsed).map(invalid_count2).sum()


# %%
def part2(inp):
    parsed = parse_data(inp)
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
