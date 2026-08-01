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
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0]
sample_data2 = sample_data1

# %%
sample_data1 = """
L68
L30
R48
L5
R60
L55
L1
L201
R14
L82
""".strip()
sample_data2 = sample_data1
sample_data1s = [sample_data1]

# %%
for sample in sample_data1s:
    print(sample)
    print("=======================")


# %% [markdown]
# # Parse

# %%
def parse_line(line):
    shift = int(line[1:])
    return shift if line[0] == "R" else -shift

def parse_data(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def process(parsed):
    ics(parsed)
    pos = 50
    pw = 0

    for shift in parsed:
        pos = (pos + shift) % 100

        if pos == 0:
            pw += 1

    return pw


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def sign(num):
    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0
        
def process2(parsed):
    ics(parsed)
    pos = 50
    old_pos = 50
    pw = 0

    for n, shift in enumerate(parsed):
        pos = (old_pos + shift) % 100
        full = abs(shift) // 100
        partial_shift = (abs(shift) % 100) * sign(shift)

        if partial_shift != 0 and (pos == 0 or old_pos != 0 and pos != old_pos + partial_shift):
            pw += 1

        pw += full
        ics(n, shift, full, pw, old_pos, pos)
        old_pos = pos

    return pw


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
