from operator import itemgetter
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
# [Advent of Code 2016 - Day 24](https://adventofcode.com/2016/day/24)

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
from dataclasses import dataclass

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, pathfinding_redblob
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
def parse(inp):
    return inp.strip().split("\n")


# %% [markdown]
# # Process

# %% [markdown]
# * location should include nodes visited and in what order, visiting 2 after 3 is not the same as before
# * first calculate costs for each node pair, then use that as graph - maybe with dijkstra, supposed to be good for multiple destinations

# %%
from utils.pathfinding_redblob import *
@dataclass
class ReducedGrid:
    junctions: dict # id -> dict(id) (id -> cost)

    def neighbors(self, id: GridLocation, came_from: dict[Location, Optional[Location]]) -> Iterator[GridLocation]:
        return self.junctions[id].keys()

        # based on the assumption that to_id is a neighbor of from_id
    def cost(self, from_id: Location, to_id: Location) -> float:
        return self.junctions[from_id][to_id]

def setup(parsed):
    if is_sample:
        print(njoin(parsed))
    H = height(parsed)
    W = width(parsed)
    ic(W, H)
    grid = pathfinding_redblob.SquareGrid(W, H)
    relevant_points = dict(((x, y), c) for x, y in product(range(W), range(H)) if (c := parsed[y][x]) != ".")
    start = first_element(set(p for p, c in relevant_points.items() if c == "0"))
    grid.walls = set(p for p, c in relevant_points.items() if c == "#")
    goals = set(p for p, c in relevant_points.items() if c.isdigit())
    ic(len(goals))
    goals_from_start = goals.difference([start])
    ics(start, goals_from_start)
    # build costs from every numbered node to every other numbered node
    junction_nodes = pathfinding_redblob.dijkstra_reduced_node_connections(grid, goals)
    ics(junction_nodes)
    return start, goals_from_start, grid, junction_nodes


# %%
def process(parsed):
    def path_length(path):
        result = seq(path).pad_front(start).sliding(2).starmap(lambda a, b: junction_nodes[a][b]).sum()
        #ics("path_length", path, result)
        return result

    start, goals_from_start, grid, junction_nodes = setup(parsed)
    result = seq(goals_from_start).permutations().map(path_length).min()
    return result


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    def path_length(path):
        result = seq(path).pad_front(start).pad_back(start).sliding(2).starmap(lambda a, b: junction_nodes[a][b]).sum()
        #ics("path_length", path, result)
        return result

    start, goals_from_start, grid, junction_nodes = setup(parsed)
    result = seq(goals_from_start).permutations().map(path_length).min()
    return result


# %%
def part2(inp):
    parsed = parse(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
part1(sample_data1) # 14
part2(sample_data2) # 20

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp) # 456
part2(real_inp) # 704
