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

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module

# %% [markdown]
# # Sample Data

# %%
sample_data1 = """125 17"""
sample_data2 = sample_data1

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
example

# %%
sample_data1s = ["0 1 10 99 999", "125 17"]
sample_data1s = ["125 17"]
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
    return string_to_integers_list(inp)


# %% [markdown]
# # Process

# %%
def transform(stone):
    if not stone:
        return [1]
    elif (digits := count_integer_digits(stone)) % 2 == 0:
        s = str(stone)
        n = count_integer_digits(stone) // 2
        return [int(s[:n]), int(s[n:])]
        
    return [stone * 2024]        

def process(parsed, cnt=25):
    ics(parsed)
    stones = parsed
    
    for n in range(cnt):
        stones = seq(stones).map(transform).flatten().list()
        
        if n < 3:
            ics(n, stones)
        
    return len(stones)


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
@cache
def digit_cnt(remain, stone):
    if remain <= 0:
        return 1

    remain -= 1
    
    if not stone:
        return digit_cnt(remain, 1)
    elif (digits := count_integer_digits(stone)) % 2 == 0:
        s = str(stone)
        n = count_integer_digits(stone) // 2
        return digit_cnt(remain, int(s[:n])) + digit_cnt(remain, int(s[n:]))

    return digit_cnt(remain, stone * 2024)

def process2(parsed):
    return seq(parsed).map(partial(digit_cnt, 75)).sum()


# %%
def part2(inp):
    parsed = parse_data(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
import sys
print(sys.getrecursionlimit())
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
