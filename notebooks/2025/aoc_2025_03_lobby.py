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
sample_data1 = """
hijkl
"""
sample_data2 = sample_data1

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
example

# %%
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0]
sample_data2 = sample_data1

# %%
for sample in sample_data1s:
    print(sample)
    print("=======================")


# %% [markdown]
# # Parse

# %%
def parse_line(line):
    return maptuple(int, line)

def parse_data(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def max_joltage_old(batteries):
    l = len(batteries)
    ics(l)
    #max_j, idx = max(zip(batteries[:-1], count()))
    max_j, idx = max(zip(batteries[:-1], count(0, -1)))
    idx = idx * -1
    ics(max_j, idx, batteries[:-1])
    next_max = max(batteries[idx+1:])
    ics(next_max, batteries[idx+1:])
    return max_j * 10 + next_max

def max_joltage_rec(batteries, reserve):
    if not reserve:
        return max(batteries)
        
    l = len(batteries)
    max_j, idx = max(zip(batteries[:-reserve], count(0, -1)))
    idx = idx * -1
    #ics(l,reserve,max_j,batteries)
    return max_j * 10 ** reserve + max_joltage_rec(batteries[idx+1:], reserve - 1)


def process(parsed, num_batteries=2):
    if 0:
        multipliers = tuple(reversed([10 ** n for n in range(num_batteries)]))
        
        def calc_joltage(batteries):
            return sum(multiply(batteries, multipliers))
        
        def max_joltage(batteries):
            res = max(map(calc_joltage, combinations(batteries, num_batteries)))
            return res
            
    def max_joltage(batteries):
        res = max_joltage_rec(batteries, num_batteries-1)
        #ics(batteries, res)
        return res
    #ics(parsed)
    return seq(parsed).map(max_joltage).sum()


# %%
def part1(inp):
    parsed = parse_data(inp)
    #result = process(parsed[:10])
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def part2(inp):
    parsed = parse_data(inp)
    result = process(parsed, 12)
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
