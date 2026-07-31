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
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils, pathfinding_redblob
from aoc_utils import * # this includes adding c:\ut to sys.path
from utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module
import pathfinding_redblob as pf

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
    return string_to_integers_list(inp)
    return inp.strip()


# %% [markdown]
# # Process

# %%
def get_path(parsed, W, byte_count):
    first_bytes = parsed[:byte_count]
    walls = set(map(tuple, first_bytes))
    grid = pf.SquareGrid(W, W)
    grid.walls = walls
    start_pos = 0, 0
    end_pos = W-1, W-1
    came_from, cost_so_far, current = pf.a_star_search(grid, start_pos, end_pos)
    return start_pos, end_pos, came_from, cost_so_far, current, grid
    
def get_path_unviability(parsed, W, byte_count):
    start_pos, end_pos, came_from, cost_so_far, current, grid = get_path(parsed, W, byte_count)
    return current != end_pos

def process(parsed, W, byte_count):
    ic(len(parsed), W, byte_count)
    start_pos, end_pos, came_from, cost_so_far, current, grid = get_path(parsed, W, byte_count)
    ics(current)
    path = pf.reconstruct_path(came_from, start_pos, end_pos)
    ic(len(path))
    if is_sample:
        special_chars = [(graph_char_circle_cross, x, y) for x, y in path]
        print(get_vis_map_multiline_str(map_list(itemgetter(0), grid.walls), map_list(itemgetter(1), grid.walls), special_chars=special_chars, filled_char=graph_char_light_block, blank_char=graph_char_small_dot))
    return len(path)-1


# %%
def part1(inp, W, steps):
    parsed = parse_data(inp)
    result = process(parsed, W, steps)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed, W, steps):
    #ic(get_path_viability(parsed, W, steps))
    #ic(get_path_viability(parsed, W, len(parsed)))
    gpu = partial(get_path_unviability, parsed, W)
    ics(gpu(steps))
    too_many_steps = find_lowest_int(gpu, steps, len(parsed)-1)
    ic(too_many_steps)
    return ",".join(map(str, parsed[too_many_steps-1]))


# %%
def part2(inp, W, steps):
    parsed = parse_data(inp)
    result = process2(parsed, W, steps)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())
parsed = parse_data(sample_data1s[0])
ics(parsed.index([1, 1]))

for sample_data1 in sample_data1s:
    part1(sample_data1, 7, 12)

part2(sample_data2, 7, 12)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp, 71, 1024)

part2(real_inp, 71, 1024) # 2902 is wrong

# %% [markdown]
# # Others' solutions
