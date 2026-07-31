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

# %%
# %load_ext autoreload

# %%
from collections import *

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, pathfinding_redblob
from aoc_utils import * # this includes adding c:\ut to sys.path
from utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module
import pathfinding_redblob as pf


# %%
def parse(inp):
    return int(inp.strip())


# %%
def is_valid_location(x, y, fav_num):
    val = x*x + 3*x + 2*x*y + y + y*y + fav_num
    return not (val.bit_count() & 1 )


# %% [markdown]
# # Process

# %%
class CubiclesGrid(pf.SquareGrid):
    def __init__(self, fav_num):
        super().__init__(-1, -1) # special grid, infinite width and height
        self.fav_num = fav_num
        
    def in_bounds(self, id: pf.GridLocation) -> bool:
        x, y, *_ = id
        return self.left <= x and self.top <= y

    def passable(self, from_id: pf.GridLocation, id: pf.GridLocation) -> bool:
        x, y, *_ = id
        return is_valid_location(x, y, fav_num)

def process(parsed, x, y):
    start = initial_state = (1,1)
    goal = final_state = (x, y)
    graph = CubiclesGrid(parsed)
    came_from, cost_so_far, current = pf.a_star_search(graph, start, goal)
    return cost_so_far[current]


# %%
def part1(inp, x, y):
    parsed = parse(inp)
    steps  = process(parsed, x, y)
    result = steps
    print_result(result)

# %% [markdown]
# # Process2

# %%
def process2(parsed, limit = 50):
    start = initial_state = (1,1)
    graph = CubiclesGrid(parsed)
    cost_so_far = {}
    
    def is_goal(current, goal):
        return cost_so_far[current] >= limit
        
    came_from, cost_so_far, current = pf.dijkstra_search(graph, start, goal=None, is_goal=is_goal, cost_so_far=cost_so_far)
    return cost_so_far


# %%
def part2(inp, limit=50):
    parsed = parse(inp)
    cost_so_far = process2(parsed, limit)
    result = len(cost_so_far)
    print_result(result)
    return cost_so_far


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
part1("10", 7, 4)
cost_so_far = part2("10")
#xs_and_ys = [(x, y) for x, y in product(range(10), range(7)) if (x, y) in cost_so_far]
#print(get_vis_map_multiline_str(*zip(*xs_and_ys)))

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp, 31, 39)
cost_so_far = part2(real_inp)
