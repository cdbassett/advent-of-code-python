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
import os
import sys
from collections import *
import re
import math

from icecream import ic
import iteration_utilities as it_ut
import numpy as np

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions # when running standalone, apparently need this import explicitly in main module

# %% [markdown]
# # Sample Data

# %%
sample_data1 = """
hijkl
"""
sample_data2 = sample_data1

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
def parse_shape(lines):
    return lines[1:]

def parse_region(line):
    #ics(line)
    ints = string_to_integers(line)
    return tuple(ints[:2]), tuple(ints[2:])

def parse_data(inp):
    *shapes, regions = seq(inp.strip().split("\n")).split().list()
    #ics(shapes, regions)
    return seq(shapes).map(parse_shape).list(), seq(regions).map(parse_region).list()


# %% [markdown]
# # Process

# %%
# max region size is 50x50
# don't need every way they can fit, just one way they can fit
# probably worth something to remove from consideration those lines that don't have enough pixels to fit the shapes no matter what

def pixel_count(lines):
    return "".join(lines).count("#")

def process(parsed):
    def fits(region):
        area = math.prod(region[0])
        min_space = sum(r * c for r, c in zip(region[1], counts))
        return area >= min_space
    
    shapes, regions = parsed
    counts = seq(shapes).map(pixel_count).list()
    shapes_with_counts = seq(shapes).zip(counts).list()
    ic(shapes_with_counts)
    ic(seq(regions).map(itemgetter(0)).map(itemgetter(0)).max())
    ic(seq(regions).map(itemgetter(0)).map(itemgetter(1)).max())
    ic(len(regions))
    # apparently we don't have to fit, if there's enough pixels, that line works
    return seq(regions).count(fits)
    
    if 0:
        for n, region in enumerate(regions):
            area = math.prod(region[0])
            min_space = sum(r * c for r, c in zip(region[1], counts))
            fits = area >= min_space
            ic(n, region[0], fits, area, min_space)



# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

for sample_data1 in sample_data1s:
    part1(sample_data1)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)

# %%
a = [[1, 2], [3, 4]]
np.pad(a, ((3, 2), (1, 3)))

# %% [markdown] jp-MarkdownHeadingCollapsed=true
# # Others' solutions
