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

    arr = np.fromfunction(risk_level_v, (16, 16) if is_sample else (35,728), dtype="uint32")
    path = pathfinding_redblob.reconstruct_path(came_from, start, goal)
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
part1(real_inp) # 10115
part2(real_inp) # 984 is too low

# %% [markdown]
# # Other's Solutions

# %%
# https://www.reddit.com/r/adventofcode/comments/a8i1cy/comment/ecax3s5/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
# curiously gives same wrong answer as mine does
from functools import lru_cache
from heapq import heappush, heappop

MOD = 20183
depth, (tx, ty) = parse(real_inp)

@lru_cache(None)
def gindex(x, y):
    if x == y == 0: return 0
    if x == tx and y == ty: return 0
    if y == 0: return x * 16807 % MOD
    if x == 0: return y * 48271 % MOD
    return ((gindex(x-1, y) + depth) *
            (gindex(x, y-1) + depth) % MOD)

def region(x, y):
    return (gindex(x, y) + depth) % MOD % 3

ans1 = sum(region(x, y) for x in range(tx+1) for y in range(ty+1))

def neighbors(x, y, e):
    for nx, ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
        if 0 <= nx and 0 <= ny:
            r = region(nx, ny)

            for ne in range(3):
                if r != ne:
                    yield nx, ny, ne, 8 if e != ne else 1

# rocky - neither [0]
# wet - torch [1]
# narrow - climb [2]
pq = [(0, 0, 0, 1)]
dist = {(0, 0, 1): 0}

while pq:
    d, x, y, e = heappop(pq)

    if (x, y, e) == (tx, ty, 1):
        print(f'Answer: {d}')

    if x > 3 * tx or y > 3 * ty: continue

    if dist.get((x, y, e)) < d: continue

    for nx, ny, ne, nw in neighbors(x, y, e):
        if d + nw < dist.get((nx, ny, ne), float('inf')):
            dist[nx, ny, ne] = d + nw
            heappush(pq, (d + nw, nx, ny, ne))


# %%
# https://www.reddit.com/r/adventofcode/comments/a8i1cy/comment/ecax2bg/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
def ints(s):
    return list(map(int, re.findall(r"-?\d+", s)))  # thanks mserrano!

inp = real_inp
#depth, (tx, ty) = parse(real_inp)
lines = inp.splitlines()
depth = ints(lines[0])[0]
tx, ty = tuple(ints(lines[1]))
dp = [[None for _ in range(ty+1000)] for _ in range(tx+1000)]

def erosion(x, y):
    if dp[x][y] is not None:
        return dp[x][y]

    geo = None

    if y == 0:
        geo = x * 16807
    elif x == 0:
        geo = y * 48271
    elif (x, y) == (tx, ty):
        geo = 0
    else:
        geo = erosion(x-1, y) * erosion(x, y-1)

    dp[x][y] = (geo + depth) % 20183
    return dp[x][y]

def risk(x, y):
    return erosion(x, y) % 3

print(sum(erosion(x, y) % 3 for x in range(tx+1) for y in range(ty+1)))

# torch = 1
import heapq
queue = [(0, 0, 0, 1)] # (minutes, x, y, cannot)
best = dict() # (x, y, cannot) : minutes
target = (tx, ty, 1)

while queue:
    minutes, x, y, cannot = heapq.heappop(queue)
    best_key = (x, y, cannot)

    if best_key in best and best[best_key] <= minutes:
        continue

    best[best_key] = minutes

    if best_key == target:
        print(minutes)
        break

    for i in range(3):
        if i != cannot and i != risk(x, y):
            heapq.heappush(queue, (minutes + 7, x, y, i))

    # try going up down left right
    for dx, dy in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
        newx = x + dx
        newy = y + dy

        if newx < 0:
            continue

        if newy < 0:
            continue

        if risk(newx, newy) == cannot:
            continue

        heapq.heappush(queue, (minutes + 1, newx, newy, cannot))
