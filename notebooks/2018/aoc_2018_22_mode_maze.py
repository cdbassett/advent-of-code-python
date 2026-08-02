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
# [Advent of Code 2018 - Day 22](https://adventofcode.com/2018/day/22)

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
import re

import numpy as np
from icecream import ic
from colorama import Fore, Style

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils, pathfinding_redblob
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module
import utils.pathfinding_redblob as pathfinding_redblob

# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0]
sample_data2 = sample_data1

# %% [markdown]
# # Parse

# %%
sig_chars = ".=|"

def parse(inp):
    ints = string_to_integers_list(inp)
    return ints[0][0], tuple(ints[1])


# %% [markdown]
# # Process

# %%
a_to_c = np.vectorize(sig_chars.__getitem__)

def make_functions(depth, target):
    @cache
    def erosion_level(x, y):
        #assert x >= 0 and y >= 0
        #ic(x, y)
        if x == 0:
            gi = y * 48271
        elif y == 0:
            gi = x * 16807
        elif (x, y) in ((0,0), target):
            gi = 0
        else:
            gi = erosion_level(x-1, y) * erosion_level(x, y-1)

        return (gi + depth) % 20183

    def erosion_level_np(*args):
        ic(args, tuple(args))
        return erosion_level(*tuple(args))

    erosion_level_np_v = np.vectorize(erosion_level)

    def risk_level(x, y):
        return erosion_level(x, y) % 3

    def risk_level_v(x, y):
        return erosion_level_np_v(x, y) % 3

    return risk_level, risk_level_v

def process(parsed):
    ic(parsed)
    depth, target = parsed
    risk_level, risk_level_v = make_functions(depth, target)

    if is_sample:
        arr = np.fromfunction(risk_level_v, (16, 16), dtype="uint32")
        print(get_numpy_char_array_repr(a_to_c(arr.T)))

    return sum(sum(np.fromfunction(risk_level_v, (target[0]+1, target[1]+1), dtype="uint32")))


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
from utils.pathfinding_redblob import *

tools_list = [
    "CT", # rocky, climbing gear or torch
    "CN", # wet, climbing gear or nothing
    "TN", # narrow, torch or nothing
]

def process2(parsed):
    def tool_possibilities(x, y):
        r = risk_level(x, y)
        return tools_list[r]

    # location is x, y, tool
    class ErosionGrid:
        # can't go negative but anywhere else is fair game
        def in_bounds(self, id: GridLocation) -> bool:
            x, y, *_ = id
            return 0 <= x and 0 <= y

        def neighbors(self, id: GridLocation, came_from: dict[Location, Optional[Location]]) -> Iterator[GridLocation]:
            x, y, tool = id
            neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)] # E W N S
            results = list(filter(self.in_bounds, neighbors))
            #diag = [(n[0], n[1], t, risk_level(n[0], n[1])) for n in results for t in tool_possibilities(*n)]
            #ics(id, diag)
            # only tool changes that are valid and moves with same tool allowed
            results = [(n[0], n[1], tool) for n in results if tool in tool_possibilities(*n)] + [(x, y, othertool) for othertool in tool_possibilities(x, y) if othertool != tool]
            return results

            # based on the assumption that to_id is a 1-away neighbor of from_id
        def cost(self, from_id: Location, to_id: Location) -> float:
            return 1 if from_id[:2] != to_id[:2] else 7 # assume that same location means a tool change

        heuristic = SquareGrid.heuristic
        if 0:
            def heuristic(self, id: Location, goal: Location) -> float:
                (x1, y1, *_) = id
                (x2, y2, *_) = goal
                return abs(x1 - x2) + abs(y1 - y2)


    def callback(cbi):
        if 0:
            cost = cbi.cost_so_far[cbi.current]
            nc = list(zip(cbi.neighbors, map(partial(grid.cost, cbi.current), cbi.neighbors)))
            ics(cbi.iterations, cbi.current, cbi.cost, nc)

    ics(parsed)
    depth, target = parsed
    risk_level, risk_level_v = make_functions(depth, target)
    grid = ErosionGrid()
    goal = target + ("T",) # must end with torch
    start = 0, 0, "T" # start with torch equipped
    came_from, cost_so_far, current = pathfinding_redblob.a_star_search(grid, start, goal, callback_step=1, callback=callback)
    #came_from, cost_so_far, current = pathfinding_redblob.dijkstra_search(grid, start, goal, callback_step=1, callback=callback) # gave same result but took 27s instead of 5
    ics(goal, current, cost_so_far[current])

    path = pathfinding_redblob.reconstruct_path(came_from, start, goal)
    max_width, max_height = (max(path, key=itemgetter(n))[n]+1 for n in range(2))
    ic(max_width, max_height)
    arr = np.fromfunction(risk_level_v, (max_width, max_height), dtype="uint32")
    ic(len(path))
    pre, post = Fore.YELLOW+Style.BRIGHT, Style.RESET_ALL
    tool_colors = {
        "T": Fore.YELLOW+Style.BRIGHT,
        "N": Fore.BLUE+Style.BRIGHT,
        "C": Fore.RED+Style.BRIGHT, }

    special_chars = [(tool_colors[t]+sig_chars[arr[x, y]]+post, x, y) for x, y, t in path] + [("T", target[0], target[1])]
    print(get_numpy_char_array_repr(a_to_c(arr.T), special_chars=special_chars))
    return cost_so_far[current]


# %%
def part2(inp):
    parsed = parse(inp)
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
from utils.aoc_utils import *
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp) 
part2(real_inp) 

