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
# [Advent of Code 2021 - Day 25](https://adventofcode.com/2021/day/25)

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

import numpy as np
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

# %%
for sample in sample_data1s:
    print(sample)
    print("=======================")


# %% [markdown]
# # Parse

# %%
def parse_data(inp):
    return build_numpy_array_from_string_graph(inp)


# %% [markdown]
# # Process

# %%
def process(parsed):
    def rep(a):
        return 1 * a

    def shift(state, c, axis):
        herd = state == c
        empty = state == "."
        want = np.roll(herd, 1, axis=axis)
        can = want & empty
        moved = np.roll(can, -1, axis=axis)
        #ics(rep(herd), rep(want), rep(can), rep(moved))
        state[np.nonzero(can)] = c
        state[np.nonzero(moved)] = "."
        
    print_sample(get_numpy_char_array_repr(parsed.T))
    w = width(parsed)
    h = height(parsed)
    state = np.copy(parsed.T) # don't care about x/y order for this problem
    previous = np.copy(state)

    for step in count(1):
        #ics(step)
        shift(state, ">", 1)
        #print_sample(get_numpy_char_array_repr(state))
        shift(state, "v", 0)
        #print_sample(get_numpy_char_array_repr(previous))
        #print_sample(get_numpy_char_array_repr(state))
        
        if np.array_equal(state, previous):
            return step

        previous = np.copy(state)
    
    return None


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
