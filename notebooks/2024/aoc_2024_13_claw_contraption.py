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
# [Advent of Code 2024 - Day 13](https://adventofcode.com/2024/day/13)

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
from z3 import *

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
Entry = namedtuple("Entry","a,b,prize")

def parse_data(inp):
    return seq(string_to_integers_list(inp)).grouped(3).smap(Entry)


# %% [markdown]
# # Process

# %%
def solve_machine(entry, factor=0):
    a, b = Int("a"), Int("b")
    cost = Int('cost')
    cost_expr = a * 3 + b
    opt = Optimize()
    opt.add(cost == cost_expr)
    opt.add(a * entry.a[0] + b * entry.b[0] == entry.prize[0]+factor)
    opt.add(a * entry.a[1] + b * entry.b[1] == entry.prize[1]+factor)
    opt.minimize(cost)
    #print(opt)
    opt.check()
    
    if opt.check() == sat:
        model = opt.model()
        #print(model)
        sol_a, sol_b, sol_cost = model[a].as_long(), model[b].as_long(), model[cost].as_long()
        return sol_cost
        
    return 0 

def process(parsed):
    #ics(parsed)
    return sum(solve_machine(p) for p in parsed)


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    return sum(solve_machine(p, 10000000000000) for p in parsed)


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
