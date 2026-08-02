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
# [Advent of Code 2024 - Day 12](https://adventofcode.com/2024/day/12)

# %% editable=false
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
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils, pathfinding_redblob
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module
import utils.pathfinding_redblob as pf

# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
example

# %%
sample_data1s = split_example(example)
sample_data1a = sample_data1s[0]
sample_data1b = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""
sample_data1c = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""
sample_data2b="""EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""
sample_data2c="""AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""
sample_data1s = [sample_data1a, sample_data1b, sample_data1c]
sample_data2s = [sample_data1a, sample_data1c, sample_data2b, sample_data2c]

# %%
for sample in sample_data1s:
    print(sample)
    print("=======================")


# %% [markdown]
# # Parse

# %%
def parse_data(inp):
    return maplist(list, inp.strip().split("\n"))


# %% [markdown]
# # Process

# %%
dirs = (1, 1j, -1, -1j)

def perimeter(points_dict, positions):
    c = points_dict[positions[0]]
    return sum(1 for pos in positions for dir in dirs if points_dict.get(pos + dir) != c)

class GardenGrid(pf.ComplexDictGrid):
    def passable(self, from_id: complex, id: complex) -> bool:
        return self.points[from_id] == self.points[id]

def setup(inp):
    parsed = parse_data(inp)
    ics(parsed)
    points_dict = build_complex_points_dict(parsed)
    grid = GardenGrid(points_dict)
    visited = set()
    areas = []

    for pos, c in points_dict.items():
        if pos not in visited:
            came_from, current = pf.breadth_first_search(grid, pos, "None")
            visited.update(came_from.keys())
            #ics(c, came_from.keys())
            areas.append((c, list(came_from.keys())))
    return points_dict, grid, visited, areas

def process(inp):
    points_dict, grid, visited, areas = setup(inp)
    total = sum(perimeter(points_dict, positions) * len(positions) for c, positions in areas)
    return total


# %%
def part1(inp):
    result = process(inp)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def count_sides_at(xy, points, dir):
    if not points:
        res = 0
    else:
        res = 1 + sum(1 for p1, p2 in pairwise(points) if p1*dir + dir != p2*dir)
        
    #ics("count_sides_at", xy, points, dir, mult, res)
    return res

def sides(points_dict, positions):
    c = points_dict[positions[0]]
    perimeter_positions = set((pos, dir) for pos in positions for dir in dirs if points_dict.get(pos + dir) != c) # pos, vert
    #ics(c, perimeter_positions)
    left_xs = set(p[0].real for p in perimeter_positions if p[1] == -1)
    right_xs = set(p[0].real for p in perimeter_positions if p[1] == 1)
    top_ys = set(p[0].imag for p in perimeter_positions if p[1] == -1j)
    bot_ys = set(p[0].imag for p in perimeter_positions if p[1] == 1j)
    #ics(left_xs, right_xs, top_ys, bot_ys)
    xsides = 0
    ysides = 0

        # check all ys at each x
    for x in left_xs:
        xsides += count_sides_at(x, sorted(p[0].imag for p in perimeter_positions if p[1] == -1 and p[0].real == x), 1)

    for x in right_xs:
        xsides += count_sides_at(x, sorted(p[0].imag for p in perimeter_positions if p[1] == 1 and p[0].real == x), 1)

    for y in top_ys:
        ysides += count_sides_at(y, sorted(p[0].real for p in perimeter_positions if p[1] == -1j and p[0].imag == y), 1j)

    for y in bot_ys:
        ysides += count_sides_at(y, sorted(p[0].real for p in perimeter_positions if p[1] == 1j and p[0].imag == y), 1j)

    #ics(c, positions[0], xsides, ysides, xsides + ysides)
    return xsides + ysides     

paired_corners = tuple(pairwise((1, 1j, -1, -1j, 1)))

# technically this is counting corners...
def sides(points_dict, positions):
    def is_corner(pos, dir_a, dir_b):
        ca, cb = points_dict.get(pos + dir_a), points_dict.get(pos + dir_b)
        # outer corner then inner corner
        return ca != c and cb != c or ca == c and cb == c and points_dict.get(pos + dir_a + dir_b) != c
        
    c = points_dict[positions[0]]
    res = sum(sum(1 for dir_a, dir_b in paired_corners if is_corner(pos, dir_a, dir_b)) for pos in positions)
    ics(c, positions[0], res)
    return res
    
def process2(inp):
    points_dict, grid, visited, areas = setup(inp)
    total = sum(sides(points_dict, positions) * len(positions) for c, positions in areas)
    return total


# %%
def part2(inp):
    result = process2(inp)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

for sample_data1 in sample_data1s:
    part1(sample_data1)

for sample_data2 in sample_data2s:
    part2(sample_data2)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)
