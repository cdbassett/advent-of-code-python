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
from collections import *

import numpy as np
from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils, aoc_2019_intcode, pathfinding_redblob
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module
from utils.aoc_2019_intcode import process_intcodes, parse_intcodes
from utils.pathfinding_redblob import *


# %% [markdown]
# # Parse

# %%
def parse_data(inp):
    return parse_intcodes(inp)


# %% [markdown]
# # Process

# %%
class FoundException(Exception):
    def __init__(self, val):
        self.val=val
        print( 'custom exception occurred')

directions = range(1,5) # directions are 1-4
N, S, W, E = directions
reverse = [-1, S, N, E, W]
translations = dict((n, compass_movements[c]) for n, c in enumerate("NSWE", 1))
#ic(translations)

def build_map_and_grid(parsed):
    #ics(parsed[:20], parsed[-20:])
    def show_map(target):
        special_chars = [(graph_char_circle_cross, x, y) for x, y in visited] + [(graph_char_bullseye, target[0], target[1])]
        print(get_vis_map_multiline_str(map_list(itemgetter(0), walls), map_list(itemgetter(1), walls), special_chars=special_chars, filled_char=graph_char_light_block))

    def move(direction):
        #ics("move", direction)
        return generator.send(direction)
    # we want dfs bc we have to move the droid every time
    def explore(pos, level=0):
        nonlocal oxygen

        for direction in directions:
            new_pos = add_tuple(pos, translations[direction])

            if new_pos in visited or new_pos in walls:
                continue

            status = move(direction)

            if status == 2:
                oxygen = pos
                ic(oxygen)

            if status == 0:
                walls.add(new_pos)
            #elif status == 2:
                #raise FoundException(pos)
            else:
                visited.add(new_pos)
                rev = reverse[direction]
                explore(new_pos, level+1)
                status = move(rev)
                assert status == 1

    generator = process_intcodes(parsed)
    generator.send(None) # start generator
    oxygen = None
    #moved = []
    start = 0, 0
    visited = set([start])
    walls = set()

    try:
        explore(start)
    except FoundException as fe:
        print(fe.val)
        show_map(fe.val)
        return

    show_map(oxygen)

    max_x = max(walls, key=itemgetter(0))[0]
    max_y = max(walls, key=itemgetter(1))[1]
    min_x = min(walls, key=itemgetter(0))[0]
    min_y = min(walls, key=itemgetter(1))[1]
    # technically should be max_x+1 et.c but we know from drawn map that walls are a straight line
    grid = SquareGrid(max_x, max_y, min_x, min_y)
    grid.walls = walls
    return oxygen, grid, visited, walls

def process(parsed):
    oxygen, grid, visited, walls = build_map_and_grid(parsed)
    start = 0, 0
    came_from, cost_so_far, current = a_star_search(grid, start, oxygen)
    path = reconstruct_path(came_from, start, oxygen)
    #ics(path)
    special_chars = [(graph_char_circle_cross, x, y) for x, y in path] + [(graph_char_bullseye, oxygen[0], oxygen[1])]
    print(get_vis_map_multiline_str(map_list(itemgetter(0), walls), map_list(itemgetter(1), walls), special_chars=special_chars, filled_char=graph_char_light_block, blank_char=graph_char_small_dot))
    #ic(path[:10], path[-10:])
    return len(path)


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    oxygen, grid, visited, walls = build_map_and_grid(parsed)
    came_from, end_node, longest = breadth_first_count_longest(grid, oxygen)
    return longest + 1


# %%
def part2(inp):
    parsed = parse_data(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
print_preface_notebook()
part1(real_inp) # 29 is not right, neither is 335
part2(real_inp) # 359 is too low
# both accepted answers seem like they're one higher than I think they should be
# example in both cases show initial position not coutning but answer seems to include them
# either that or my mapping is off by exactly one

# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())
print_preface_notebook()
part1(real_inp)
part2(real_inp)
