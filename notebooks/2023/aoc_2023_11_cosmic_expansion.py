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
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, pathfinding_redblob
from aoc_utils import * # this includes adding c:\ut to sys.path
from utilities import *
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
sample_data2 = sample_data1

# %%
print(sample_data1)


# %% [markdown]
# # Parse

# %%
def parse(inp):
    return inp.strip().split("\n")


# %% [markdown]
# # Process

# %%
def get_adders(filled, dim, expansion):
    add = 0
    adders = {}

    for n in range(dim):
        if n in filled:
            adders[n] = add
        else:
            add += expansion

    return adders

def expand_universe(parsed, expansion):
    H = height(parsed)
    W = width(parsed)
    points = build_points(parsed)
    ic(W, H, get_point_set_bounds(points))
    filled_cols = seq(points).map(itemgetter(0)).set()
    filled_rows = seq(points).map(itemgetter(1)).set()
    ic(len(filled_cols), len(filled_rows))
    col_adders = get_adders(filled_cols, W, expansion)
    row_adders = get_adders(filled_rows, H, expansion)
    ics(col_adders, row_adders)
    ic(len(points))
    points = set(Point2D(p.x + col_adders[p.x], p.y + row_adders[p.y]) for p in points)
    ic(len(points))
    ic(get_point_set_bounds(points))
    return points

def process(parsed, expansion = 1):
    #ics(parsed)
    points = expand_universe(parsed, expansion = expansion)
    #ic(sorted(points))

    if 0 and is_sample:
        print("\n".join(get_vis_map(points)))

    return seq(points).combinations(2).starmap(manhattan).sum()


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %%
def part2(inp, expansion):
    parsed = parse(inp)
    result = process(parsed, expansion)
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
part1(sample_data1)
part2(sample_data2, 99)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp, 1000000-1)
# 9553868 is too low
