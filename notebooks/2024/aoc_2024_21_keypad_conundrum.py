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

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
from aoc_utils import * # this includes adding c:\ut to sys.path
from utilities import *
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
sample_data1s = ["""029A
980A
179A
456A
379A"""]

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
num_keypad = """789
456
123
 0A""".split("\n")
dir_keypad = """ ^A
<v>""".split("\n")
num_dict = dict(get_chars_and_coords(num_keypad, complex))
dir_dict = dict(get_chars_and_coords(dir_keypad, complex))
#ics(num_dict, dir_dict)
num_a_pos = num_dict["A"]
dir_a_pos = dir_dict["A"]
num_grid = CharTable(num_keypad)
dir_grid = CharTable(dir_keypad)

def count_movements(positions):
    return sum(starmap(manhattan, pairwise(positions)))

def get_keys(key, cnt):
    return key * max(0, int(cnt))

@cache
def is_valid_path(pos, code, first):
    #ics("is_valid_path", pos, code, first)
    dct = num_dict if first else dir_dict
    grid = num_grid if first else dir_grid

    for n, c in enumerate(code):
        if c != "A":
            pos += arrow_movements_c[c]
            #ics(c, pos)
            if grid[pos] == " ":
                return False
    return True

@cache
def get_best_path(a, b, level, first):
    if a == b:
        return 1

    hdr = "  " * (2-level)
    diff = b - a
    left_right = get_keys(">", diff.real) + get_keys("<", -diff.real)
    up_down = get_keys("^", -diff.imag) + get_keys("v", diff.imag)
    #ics(hdr, "get_best_path", a, b, level, first, up_down, left_right)

    if level == 0:
        best_path = manhattan_c(diff) + 1 # we don't care about optimal at last level bc no further keypads are affected
    elif not left_right or not up_down or level == 0:
        best_path = sum(get_best_path(a1, b1, level-1, False) for a1, b1 in pairwise([dir_dict[c] for c in "A" + left_right + up_down + "A"]))
    else:
        new_paths = []
        # only optimization is horiz first or vert first
        for test_code in (left_right + up_down + "A", up_down + left_right + "A"):
            if is_valid_path(a, test_code, first):
                new_path = sum(get_best_path(a1, b1, level-1, False) for a1, b1 in pairwise([dir_dict[c] for c in "A" + test_code])) # always starting from A position
                #ics(hdr, test_code, new_path)
                new_paths.append(new_path)
    
        best_path = min(new_paths)
        
    #ics(hdr, best_path)
    return best_path


def get_full_best_path(code, level = 2):
    positions = [num_dict[c] for c in "A" + code] # always starting from A position
    best_path = sum(get_best_path(a, b, level, True) for a, b in pairwise(positions)) 
    return best_path

def process(parsed, cnt=2):
    total = 0

    for code in parsed:
        best_path = get_full_best_path(code, cnt)
        total += int(code[:-1]) * best_path
        
    return total


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def part2(inp):
    parsed = parse_data(inp)
    result = process(parsed, 25)
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
part1(real_inp) # 97482 is too high
part2(real_inp)

# %% [markdown]
# # Others' solutions
