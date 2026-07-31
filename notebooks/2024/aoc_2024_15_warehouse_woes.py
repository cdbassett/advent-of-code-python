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
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils, pathfinding_redblob
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module
import pathfinding_redblob as pf

# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0]
sample_data2 = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""
sample_data1s = [sample_data2, sample_data1]
sample_data2b = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""
sample_data2s = [sample_data2b, sample_data1]

# %%
for sample in sample_data1s:
    print(sample)
    print("=======================")


# %% [markdown]
# # Parse

# %%
def parse_data(inp, double = False):
    map_str, movements = inp.split("\n\n")
    
    if double:
        map_str = map_str.replace("#","##").replace(".","..").replace("O","[]").replace("@","@.")
        
    return map_str.split("\n"), movements.replace("\n","")
    #return build_numpy_array_from_string_graph(inp)


# %% [markdown]
# # Process

# %%
def show_grid(title, robot_pos, grid):
    print_lines(title, get_chartable_list_repr(grid, special_chars=[("@",)+complex_to_tuple(robot_pos)] ))

def process(parsed):
    def attempt_move(pos, move):
        if (c := grid[pos]) == ".":
            grid[pos] = "O"
            return True
        elif c == "O":
            return attempt_move(pos+move, move)            
            
        return False
        
    map_str, movements = parsed
    grid = CharTable(maplist(list, map_str))
    robot_pos = first(build_complex_points(map_str, sig_char="@"))
    grid[robot_pos] = "."

    for n, movement in enumerate(movements):
        move = arrow_movements_c[movement]
        new_pos = robot_pos+move

        if attempt_move(new_pos, move):
            grid[new_pos] = "."
            robot_pos = new_pos

    #show_grid("final", robot_pos, grid)
    return sum(x+y*100 for x, y in get_char_coords(grid.table, "O"))


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
right, left = 1, -1

def process2(parsed):
    def box_positions(pos, move):
        if (c := grid[pos]) == "[":
            res = (pos, pos + right) if move.imag else (pos,)
        elif c == "]":
            res = (pos + left, pos) if move.imag else (pos,)
        else:
            res =  tuple()
        #ics("bp", pos, res)
        return res

    def attempt_move(positions, move, level=0):
        if walls.intersection(positions):
           return False

        new_positions = set(flatten(box_positions(pos, move) for pos in positions))
        
        if (not new_positions or all(grid[pos] == "." for pos in positions) or 
                attempt_move(list(pos+move for pos in new_positions), move, level+1)):
            for pos in new_positions:
                grid[pos+move] = grid[pos]
                grid[pos] = "."
            return True
            
    map_str, movements = parsed
    grid = CharTable(maplist(list, map_str))
    robot_pos = first(build_complex_points(map_str, sig_char="@"))
    walls = set(build_complex_points(map_str, sig_char="#"))
    show_grid("initial", robot_pos, grid)
    grid[robot_pos] = "."

    for step, movement in enumerate(movements, 1):
        move = arrow_movements_c[movement]
        new_pos = robot_pos+move

        if attempt_move((new_pos,), move):
            robot_pos = new_pos

    show_grid("final", robot_pos, grid)
    return sum(x+y*100 for x, y in get_char_coords(grid.table, "["))    


# %%
def part2(inp):
    parsed = parse_data(inp, True)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

for sample_data1 in sample_data1s:
    part1(sample_data1)

for sample_data2 in sample_data2s[1:]:
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
