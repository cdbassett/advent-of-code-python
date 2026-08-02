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
# [Advent of Code 2017 - Day 22](https://adventofcode.com/2017/day/22)

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
for sample in sample_data1s:
    print(sample)
    print("=======================")


# %% [markdown]
# # Parse

# %%
def parse_line(line):
    return line

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def process(parsed, iterations):
    ics(parsed)
    H = height(parsed)
    W = width(parsed)
    ic(W, H)
    points = build_complex_points(parsed)
    pos = W//2 + (H//2)*1j
    dir = -1j
    infect_count = 0

    for iteration in range(iterations):
        #ics(iteration, pos, get_vis_map(set(map(complex_to_point, points))))
        infected = pos in points
        dir = dir * (1j if infected else -1j)

        if infected:
            points.remove(pos)
        else:
            points.add(pos)
            infect_count += 1

        pos += dir

    #ics(get_vis_map(set(map(complex_to_point, points)), min_val=-W, max_val=-H))
    return infect_count


# %%
def part1(inp, iterations):
    parsed = parse(inp)
    result = process(parsed, iterations)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed, iterations):
    ics(parsed)
    H = height(parsed)
    W = width(parsed)
    ic(W, H)
    points = build_complex_points(parsed)
    pos = W//2 + (H//2)*1j
    dir = -1j
    infect_count = 0
    # CWIF
    points = dict((p, 2) for p in points)
    direction_changes = [-1j, 1, 1j, -1]

    for iteration in range(iterations):
        #ics(iteration, pos, get_vis_map(set(map(complex_to_point, points))))
        infected_level = points.get(pos, 0)
        dir = dir * direction_changes[infected_level]
        infected_level = (infected_level + 1) % 4

        if infected_level:
            points[pos] = infected_level

            if infected_level == 2:
                infect_count += 1
        else:
            del points[pos]

        pos += dir

    #ics(get_vis_map(set(map(complex_to_point, points)), min_val=-W, max_val=-H))
    return infect_count


# %%
def part2(inp, iterations):
    parsed = parse(inp)
    result = process2(parsed, iterations)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

for sample_data1 in sample_data1s:
    part1(sample_data1, 70)

part2(sample_data2, 100)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp, 10000)
part2(real_inp, 10000000)
