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

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
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
def parse_line(line):
    #return list(map(partial(operator.add, ord("a")), line))
    return line

def parse_data(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
class HeightGrid(pf.SquareGrid):
    def __init__(self, width: int, height: int, heights):
        super().__init__(width, height)
        self.heights = heights
        
    def cost(self, from_id, to_id): 
        return 1
        
    def passable(self, from_id, id):
        return self.heights[id] <= self.heights[from_id] + 1

def setup(parsed):
    def pos(c):
        idx = single_line.index(c)
        return idx % W, idx // W
        
    W, H = len(parsed[0]), len(parsed)
    ic(W, H)
    single_line = sjoin(parsed)
    start = pos("S")
    goal = pos("E")
    orda = ord("a")
    heights = dict(((x, y), ord(parsed[y][x]) - orda) for x, y in product(range(W), range(H)))
    heights[start] = 0
    heights[goal] = 25
    graph = HeightGrid(W, H, heights)
    return graph, start, goal, heights

def find_shortest(graph, start, goal):
    came_from, cost_so_far, current = pf.a_star_search(graph, start, goal)
    #ic(start, goal, current)
    return cost_so_far[goal] if current == goal else None    

def process(parsed):
    def pos(c):
        idx = single_line.index(c)
        return idx % W, idx // W
        
    ics(parsed)
    graph, start, goal, heights = setup(parsed)
    return find_shortest(graph, start, goal)  


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %%
def process2(parsed):
    ics(parsed)
    graph, start, goal, heights = setup(parsed)
    starts = [p for p, h in heights.items() if h == 0]
    return min(dist for start in starts if (dist := find_shortest(graph, start, goal)) is not None)


# %% [markdown]
# # Process2

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
