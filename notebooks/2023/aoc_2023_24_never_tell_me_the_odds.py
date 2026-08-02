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
# [Advent of Code 2023 - Day 24](https://adventofcode.com/2023/day/24)

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

import sympy as sp
from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
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

# %%
print(sample_data1)


# %% [markdown]
# # Parse

# %%
def parse_line(line):
    return seq(string_to_integers(line)).grouped(3).starmap(Point3D).to_tuple()

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
"""
position = start + v * t
v * t = position - start
t = (position - start)/v
start = position - v * t
"""


# %%
def new_min(min_val, init_val, velo):
    return max(min_val, init_val) if velo >= 0 else min_val

def new_max(max_val, init_val, velo):
    return min(max_val, init_val) if velo < 0 else max_val

def process(parsed, min_val, max_val):
    ics(parsed)
    intersection_in_boundaries_count = 0

    for h1, h2 in seq(parsed).combinations(2):
        hi1, hv1 = h1
        hi2, hv2 = h2

        m1 = hv1.y / hv1.x
        m2 = hv2.y / hv2.x

        if m1 == m2:
            continue

        b1 = hi1.y - m1*hi1.x
        b2 = hi2.y - m2*hi2.x
        x = (b2-b1) / (m1-m2)
        y = m1*x + b1

        min_x = min_val
        min_y = min_val
        min_x = new_min(min_x, hi1.x, hv1.x)
        min_x = new_min(min_x, hi2.x, hv2.x)
        min_y = new_min(min_y, hi1.y, hv1.y)
        min_y = new_min(min_y, hi2.y, hv2.y)

        max_x = max_val
        max_y = max_val
        max_x = new_max(max_x, hi1.x, hv1.x)
        max_x = new_max(max_x, hi2.x, hv2.x)
        max_y = new_max(max_y, hi1.y, hv1.y)
        max_y = new_max(max_y, hi2.y, hv2.y)
        #ics(hi1.x, hi2.x, x, min_x, max_x, hi1.y, hi2.y, y, min_y, max_y)

        if min_x <= x <= max_x and min_y <= y <= max_y:
            #ics("intersected", x, y)
            intersection_in_boundaries_count += 1
        else:
            #ics("no intersection", x, y)
            pass

    return intersection_in_boundaries_count


# %%
def part1(inp, min_val, max_val):
    parsed = parse(inp)
    result = process(parsed, min_val, max_val)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    ics(parsed)
    unknowns = sp.symbols('x y z dx dy dz t1 t2 t3')
    x, y, z, dx, dy, dz, *time = unknowns
    equations = []

    for t, (h_init, h_velo) in zip(time, parsed[:3]):
        equations.append(sp.Eq(x + t*dx, h_init.x + t*h_velo.x))
        equations.append(sp.Eq(y + t*dy, h_init.y + t*h_velo.y))
        equations.append(sp.Eq(z + t*dz, h_init.z + t*h_velo.z))

    ic(len(equations))
    ics(equations)
    solution = sp.solve(equations, unknowns)
    #ics(solution)
    solution = solution.pop()
    ics(solution)
    return int(sum(solution[:3]))


# %%
def part2(inp):
    parsed = parse(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
part1(sample_data1, 7, 27)
part2(sample_data2)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp, 200000000000000, 400000000000000) # 16502
part2(real_inp)

