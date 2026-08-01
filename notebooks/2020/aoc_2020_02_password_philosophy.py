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
Password = namedtuple("Password","min,max,letter,pw")

def parse_line(line):
    parts = line.split()
    nums = parts[0].split("-")
    
    return Password(int(nums[0]), int(nums[1]), parts[1].strip(":"), parts[2])

def parse_data(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()
    #return build_numpy_array_from_string_graph(inp)
    #return string_to_integers_list(inp)


# %% [markdown]
# # Process

# %%
def pw_is_valid(pw):
    ctr = Counter(pw.pw)
    cnt = ctr[pw.letter]
    return pw.min <= cnt <= pw.max 

def process(parsed):
    #ics(parsed)
    return seq(parsed).count(pw_is_valid)


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def pw_is_valid2(pw):
    ctr = Counter(pw.pw)
    cnt = ctr[pw.letter]
    try:
        return (pw.pw[pw.min-1] == pw.letter) ^ (pw.pw[pw.max-1] == pw.letter)
    except IndexError:
        return False
        
def process2(parsed):
    ics(parsed)
    return seq(parsed).count(pw_is_valid2)



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
