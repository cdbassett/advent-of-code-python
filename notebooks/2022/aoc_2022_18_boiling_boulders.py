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
from collections import *

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils, pathfinding_redblob
from aoc_utils import * # this includes adding c:\ut to sys.path
from utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module
import pathfinding_redblob as pf

# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0]
sample_data2 = sample_data1s[1]

# %%
for sample in sample_data1s:
    print(sample)
    print("=======================")


# %% [markdown]
# # Parse

# %%
def parse_data(inp):
    return seq(inp.strip().split("\n")).map(string_to_integers_list).list()


# %% [markdown]
# # Process

# %%
def process(parsed):
    ics(parsed)
    ic(len(parsed))
    points = seq(parsed).map(tuple).set()
    faces = sum(add_tuple(p,m) not in points for m, p in product(movements_3d, parsed))
    return faces


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %%
def process2(parsed):
    ics(parsed)
    ic(len(parsed))
    mins = tuple(min(p[i]-1 for p in parsed) for i in range(3))
    maxes = tuple(max(p[i]+2 for p in parsed) for i in range(3))
    ic(maxes, mins)
    start = mins
    graph = pf.CubeGrid(*(maxes + mins))
    points = seq(parsed).map(tuple).set()
    graph.walls = points
    ics(graph.width, graph.height, graph.depth, graph.left, graph.top, graph.front)
    came_from, current = pf.breadth_first_search(graph, start, None)
    steam = set(came_from.keys()) | set(came_from.values())
    ic(len(came_from), start, current, current in came_from)
    ic(len(steam))
    ic((graph.width+1) * (graph.height+1) * (graph.depth+1))
    faces = sum((a := add_tuple(p,m)) in steam for m, p in product(movements_3d, parsed))
    return faces


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

# %% [markdown]
# # Others' solutions
