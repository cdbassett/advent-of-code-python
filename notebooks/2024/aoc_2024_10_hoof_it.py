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
from Utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module
import pathfinding_redblob as pf

# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
example

# %%
sample_data2 = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""
sample_data1s = split_example(example) + [sample_data2]
sample_data1 = sample_data1s[0]


# %%
for sample in sample_data1s:
    print(sample)
    print("=======================")


# %% [markdown]
# # Parse

# %%
def parse_data(inp):
    return inp.split("\n")


# %% [markdown]
# # Process

# %%
class GridWithSlopes(pf.SquareGrid):
    def __init__(self, width: int, height: int, numbers):
        super().__init__(width, height)
        self.numbers = numbers
        
    def passable(self, from_id, id) -> bool:
        return self.numbers[from_id] == self.numbers[id] - 1

def setup(parsed):
    ics(parsed)
    numbers = ParsedCharArray(seq(parsed).level2_map_tuple(int).list())
    ics(numbers)
    starts = build_tuple_points(parsed, sig_char="0")
    ics(starts)
    ends = set(build_tuple_points(parsed, sig_char="9"))
    ics(ends)
    W, H = width_height(parsed)
    grid = GridWithSlopes(W, H, numbers)
    total = 0
    is_goal = lambda current, goal: current in ends
    return numbers, starts, ends, W, H, grid, is_goal

def process(parsed):
    numbers, starts, ends, W, H, grid, is_goal = setup(parsed)
    total = 0

    for start in starts:
        # have to pass unreachable goal to make algorithm only return successful paths
        final_paths = pf.breadth_first_search_all_paths(grid, start, goal="nope", is_goal=is_goal)
        end_points = set(p[-1] for p in final_paths)
        #ics(start, len(final_paths), len(end_points), end_points)
        score = len(end_points)
        total += score
        #if score == 6:
        #    ics(final_paths)
        
    return total


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    numbers, starts, ends, W, H, grid, is_goal = setup(parsed)
    total = 0

    for start in starts:
        final_paths = pf.breadth_first_search_all_paths(grid, start, goal="nope", is_goal=is_goal)
        score = len(final_paths)
        total += score
        
    return total


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

# %% [markdown]
# # Others' solutions

# %%
# https://old.reddit.com/r/adventofcode/comments/1hau6hl/2024_day_10_solutions/m1blpww/
# used this to make sure my results from sample were wrong and not aoc
from collections import deque
data = get_aocd_data()
data = sample_data2
heights = {x+y*1j: int(c) for y, line in enumerate(data.split("\n")) for x, c in enumerate(line) if c != '\n'}
adjecents = {pos: [pos+d for d in (1, -1, 1j, -1j) if heights.get(pos+d, -1) == heights[pos] + 1] for pos in heights}

class nullset:
    def __contains__(self, item): return False
    def add(self, item): pass

def trails_from(que: deque, visited: set):
    while que:
        que.extend(adjecents[node := que.popleft()])
        if node not in visited:
            visited.add(node)
            yield heights[node] == 9

print(sum(sum(trails_from(deque([pos]), visited=set())) for pos, c in heights.items() if c == 0))
#print(sum(sum(trails_from(deque([pos]), visited=nullset())) for pos, c in heights.items() if c == 0))
