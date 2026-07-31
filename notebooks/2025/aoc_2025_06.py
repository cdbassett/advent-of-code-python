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
def parse_data(inp):
    *numbers, ops = inp.strip().split("\n")
    return seq(numbers).map(string_to_integers_list).transpose().list(), ops.split()

def parse_data2(inp):
    *numbers, ops = inp.strip().split("\n")
    ics(seq(numbers).transpose().map(sjoin).list())
    return seq(numbers).transpose().map(sjoin).map(string_to_integers_list).split([]).level2_map_tuple(first_elem).list(), ops.split()
    #return seq(numbers).transpose().map(sjoin).map(str.split).map(string_to_integers_list).list(), ops.split()


# %% [markdown]
# # Process

# %%
operations = {
    "*": math.prod,
    "+": sum
}

def solve(lst, op):
    return operations[op](lst)

def process(parsed):
    numbers, ops = parsed
    ics(numbers, ops)
    assert seq(numbers).flatten().map(str).map(len).max() <= 4
    return seq(numbers).zip(ops).starmap(solve).sum()


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    numbers, ops = parsed
    ics(numbers, ops)
    return seq(numbers).zip(ops).starmap(solve).sum()


# %%
def part2(inp):
    parsed = parse_data2(inp)
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

# %% [markdown]
# # Others' solutions
