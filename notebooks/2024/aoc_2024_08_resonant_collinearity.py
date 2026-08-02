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
# [Advent of Code 2024 - Day 8](https://adventofcode.com/2024/day/8)

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
    return inp.strip().split("\n")


# %% [markdown]
# # Process

# %%
def setup(parsed):
    W, H = width_height(parsed)
    ic(W, H)
    possible_chars = set(sjoin(parsed))
    possible_chars.discard(".")
    #ic(possible_chars)
    points_by_char = dict((c, build_tuple_points(parsed,c)) for c in possible_chars)
    return W, H, points_by_char

def process(parsed):
    def add_pos(p):
        #ics("    ", p)
        if 0 <= p[0] < W and 0 <= p[1] < H:
            #ics("        ", "add")
            antinode_locations.add(p)            
            
    ics(parsed)
    W, H, points_by_char = setup(parsed)
    #ic([(k, len(v)) for k, v in points_by_char.items()])
    antinode_locations = set()

    for c, points in points_by_char.items():
        for a, b in combinations(points, 2):
            diff = subtract_tuple(a, b)
            #ics(a, b, diff)
            add_pos(subtract_tuple(b, diff))
            add_pos(add_tuple(a, diff))
    
    return len(antinode_locations)


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def extending(p, diff):
    while True:
        yield p
        p = add_tuple(p, diff)

def process2(parsed):
    def add_positions(start, diff):
        for p in extending(a, diff):
            if 0 <= p[0] < W and 0 <= p[1] < H:
                #ics("        ", "add")
                antinode_locations.add(p)            
            else:
                break
            
        #ics("    ", p)
            
    ics(parsed)
    W, H, points_by_char = setup(parsed)
    #ic([(k, len(v)) for k, v in points_by_char.items()])
    antinode_locations = set()

    for c, points in points_by_char.items():
        for a, b in combinations(points, 2):
            diff = subtract_tuple(a, b)

            add_positions(a, diff)
            add_positions(b, multiply_tuple(diff, (-1, -1)))
    
    return len(antinode_locations)


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
