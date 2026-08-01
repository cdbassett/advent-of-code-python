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
    return list(map(int, line))

def parse_data(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def process(parsed):
    W, H = len(parsed[0]), len(parsed)
    graph = pf.GridWithWeights(W, H)
    start = 0,0
    goal = W-1, H-1

    for x, y in product(range(W), range(H)):
        graph.weights[x, y] = parsed[y][x]
        
    came_from, cost_so_far, current = pf.a_star_search(graph, start, goal)
    return cost_so_far[goal]


# %%
def part1(inp):
    parsed = parse_data(inp)
    ics(parsed)
    result = process(parsed)
    print_result(result)


# %%
def repeatcycle(it, cnt):
    return chain.from_iterable(repeat(it, cnt))

def process2(parsed):
    mag = 5
    W, H = len(parsed[0]), len(parsed)
    magnified = [[(v + x // W + y // H - 1) % 9 + 1 for x, v in enumerate(repeatcycle(line, mag))] for y, line in enumerate(repeatcycle(parsed, mag))]
    return process(magnified)


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
