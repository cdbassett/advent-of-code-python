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
import sys
from collections import *

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, pathfinding_redblob
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
from utils.pathfinding_redblob import *
import utils.pathfinding_redblob as pathfinding_redblob
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module

# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0]
sample_data2 = sample_data1
#sample_data1="hijkl"

# %% [markdown]
# # Parse

# %%
#Disk = namedtuple("Disk","pos_count,t0pos")

def parse_line(line):
    return line

def parse(inp):
    #return seq(inp.strip().split("\n")).map(parse_line).list()
    return inp.strip()


# %% [markdown]
# # Process

# %%
door_indices = { "U": 0, "D": 1, "L": 2, "R": 3 }

@lru_cache(maxsize=16)
def get_doors_hash(path):
    return md5hex(path)[:4]

# location is x, y, path to current (we add path bc part of lcoation because for this puzzle the same coordinates can be reused)
class VariableDoorsGrid(SquareGrid):
    def passable(self, id: GridLocation) -> bool:
        path, last_dir = id[2][:-1], id[2][-1]
        doors = get_doors_hash(path)
        #ics("  ", id, last_dir, doors[door_indices[last_dir]])
        return doors[door_indices[last_dir]] in "bcdef"

    def neighbors(self, id: GridLocation, came_from: dict[Location, Optional[Location]]) -> Iterator[GridLocation]:
        x, y, path = id
#        doors = md5hex(path)[:4]
        #ics(doors)
        neighbors = [(x+1, y, path + "R"), (x-1, y, path + "L"), (x, y-1, path + "U"), (x, y+1, path + "D")] # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0: neighbors.reverse() # S N W E
        results = filter(self.in_bounds, neighbors)
        results = list(filter(self.passable, results))
        #ics(id, doors, results)
        return results

    def is_goal(self, id: Location, goal: Location) -> bool:
        return id[:2] == goal[:2]

def process(parsed, grid):
    ics(parsed)
    start = 0, 0, parsed
    goal = 3, 3
    came_from, cost_so_far, final = pathfinding_redblob.a_star_search(grid, start, goal)
    return final[2][len(parsed):]


# %%
def part1(inp):
    parsed = parse(inp)
    grid = VariableDoorsGrid(4, 4)
    result = process(parsed, grid)
    print_result(result)


# %% [markdown]
# # Process2

# %%
class VariableDoorsGridLongest(VariableDoorsGrid):
    def cost(self, from_id: Location, to_id: Location) -> float:
        return sys.maxsize if to_id[:2] == (3,3) else -1


def part2(inp):
    parsed = parse(inp)
    grid = VariableDoorsGridLongest(4, 4)
    result = len(process(parsed, grid))
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())

sample_datas = "ihgpwlah,kglvqrro,ulqzkmiv".split(",")

for sample_data in sample_datas:
    part1(sample_data)

print()

for sample_data in sample_datas:
    part2(sample_data)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp) # DDRRUDLRRD
part2(real_inp) # 488
