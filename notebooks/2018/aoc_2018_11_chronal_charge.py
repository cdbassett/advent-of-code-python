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

import numpy as np
from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module

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
    return int(inp.strip())


# %% [markdown]
# # Process

# %%
def hundreds(v):
    return (v // 100) % 10

@cache
def cell_power_general(parsed, x, y):
    rack_id = x + 10
    return hundreds((rack_id * y + parsed) * rack_id) - 5

def max_power(parsed, square_width):
    W = 300
    #W = 5

    cell_power = partial(cell_power_general, parsed)

    def row_cost(it):
        return sum(starmap(cell_power, it))

    def row_costs(it):
        return list(starmap(cell_power, it))

    grid_range = range(1, W+1)
    section_points = seq(product(sliding_window(grid_range, square_width), sliding_window(grid_range, square_width))).starmap(product).map(list).list()
    section_topleft_points = seq(section_points).map(first_elem).list()

    if 0:
        ics(section_points)
        ics(section_topleft_points)
        ics(seq(section_points).map(row_costs).zip(section_topleft_points).list())
        ics(seq(section_points).map(row_cost).zip(section_topleft_points).list())

    return tuple(seq(section_points).map(row_cost).zip(section_topleft_points).max())

    if 0:
        points = list(product(grid_range, grid_range))
        costs = list(batched(starmap(cell_power, points), W))
        ics(costs)
        sections = list(triplewise(map(composite_function(triplewise, list), costs)))
        ics(sections)

def process(parsed):
    ic(parsed)
    res = max_power(parsed, 3)[1]
    ic(res)
    return ",".join(map(str, res))


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    ic(parsed)
    max_val = (4, (1, 1), 1)

    if 1:
        for n in range(2, 301):
            res = max_power(parsed, n)+(n,)
            max_val = max(max_val, res)

            if is_sample or n % 10 == 0:
                ic(n, res, max_val)
        res = max_val
    else:
        res = max(max_power(parsed, n)+(n,) for n in range(2, 301)) # don't even bother with 1, its max is 4 bc that's max of single cell bc subtract 5

    ic(res)
    return ",".join(map(str, res[1] + list(res[2])))


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
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)

# %%
# solution from reddit: https://www.reddit.com/r/adventofcode/comments/a53r6i/comment/ebjosg2/?utm_source=share&utm_medium=web2x&context=3
# not truly a solution, author stopped early like I did after it became apparent that max was getting more and more negative
# and didn't track max sseen so far like I did. same result as me, but much faster
# looks like special slicing of numpy and is a big factor
serial = int(real_inp)

def power(x, y):
    rack = (x + 1) + 10
    power = rack * (y + 1)
    power += serial
    power *= rack
    return (power // 100 % 10) - 5

grid = np.fromfunction(power, (300, 300))

for width in range(3, 300):
    windows = sum(grid[x:x-width+1 or None, y:y-width+1 or None] for x in range(width) for y in range(width))
    maximum = int(windows.max())
    location = numpy.where(windows == maximum)
    print(width, maximum, location[0][0] + 1, location[1][0] + 1)
