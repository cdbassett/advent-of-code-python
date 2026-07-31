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
def bag_name(s):
    return " ".join(s.split()[:-1])

def bag_count_and_name(s):
    p = s.split() 
    return int(p[0]), " ".join(p[1:-1])

def parse_line(line):
    parts = line.split(" contain ")
    hold_bag = bag_name(parts[0])
    #ics(hold_bag, parts[1])
    contains = [] if parts[1] == "no other bags." else seq(parts[1].split(", ")).map(bag_count_and_name).list()
    return hold_bag, contains

def parse_data(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def process(parsed):
    def can_hold(bag):
        bag_holders = carriers[bag]
        return bag_holders | sets_union(can_hold(holder_bag) for holder_bag in bag_holders)        
        
    #ics(parsed)
    carriers = defaultdict(set)

    for hold_bag, contains_bags in parsed:
        for cnt, bag_name in contains_bags:
            carriers[bag_name].add(hold_bag)

    #ics(carriers)
    possibilities = set()
    all_bags = can_hold("shiny gold")
    return len(all_bags)


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    bag_dict = dict(parsed)

    def bag_contains(bag, level = 0):
        res = sum(bag_contains(b, level+1) * c + c for c, b in bag_dict[bag])
        #ics(level*"  ", res, bag, bag_dict[bag])
        return res
    
    #ics(bag_dict)
    return bag_contains("shiny gold")


# %%
def part2(inp):
    parsed = parse_data(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

part1(sample_data1)

for sample_data1 in sample_data1s:
    part2(sample_data1)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)

# %% [markdown]
# # Others' solutions
