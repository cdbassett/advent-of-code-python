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
from Utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module
import pathfinding_redblob

# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0]
sample_data2 = sample_data1s[-1]

# %% [markdown]
# # Parse

# %%
def parse(inp):
    return inp.strip()[1:-1]


# %% [markdown]
# # Process

# %%
def build_graph(edges, pos, s, n=0, lvl=0):
    start = pos
    #ics(start)

    while n < len(s):
        c = s[n]
        #ics("  ", c, n)

        if c == "(":
            n = build_graph(edges, pos, s, n + 1, lvl+1)
        elif c == ")":
            return n # n gets incrementd after call returns
        elif c == "|":
            pos = start
        else:
            new_pos = add_tuple(pos, compass_movements[c])
            edges[pos].add(new_pos)
            edges[new_pos].add(pos)
            #ics("    ", pos, new_pos, len(edges))
            pos = new_pos

        n += 1
    return n

def process(parsed):
    ic(len(parsed))
    ics(parsed)
    H = height(parsed)
    W = width(parsed)
    ic(W, H)
    edges = defaultdict(set)
    build_graph(edges, (0,0), parsed)
    #ics(edges)

    #print(get_edge_grid_map_multiline_str(edges))
    grid = pathfinding_redblob.SimpleGraph()
    grid.edges = edges
    came_from, end_node, longest = pathfinding_redblob.breadth_first_count_longest(grid, (0,0))
    return longest


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
from pathfinding_redblob import *

def process2(parsed, min_path_length=1000):
    @cache
    def calc_path_length(current):
        return 0 if (next := came_from.get(current, 0)) is None else 1 + calc_path_length(next)
        
    ics(parsed)
    edges = defaultdict(set)
    build_graph(edges, (0,0), parsed)
    grid = pathfinding_redblob.SimpleGraph()
    grid.edges = edges
    came_from, end_node, longest = pathfinding_redblob.breadth_first_count_longest(grid, (0,0))
    return sum(1 for current in came_from.keys() if calc_path_length(current) >= min_path_length)

# %%
def part2(inp, min_path_length=1000):
    parsed = parse(inp)
    result = process2(parsed, min_path_length)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

for sample_data1 in sample_data1s:
    part1(sample_data1)

part2(sample_data2, 10)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)
