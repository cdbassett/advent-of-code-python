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
# [Advent of Code 2017 - Day 15](https://adventofcode.com/2017/day/15)

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
def parse(inp):
    return string_to_integers(inp)


# %% [markdown]
# # Process

# %%
def generator1(factor, seed):
    val = seed

    while True:
        val = (val * factor) % 2147483647
        yield val

def process(parsed):
    ics(parsed)

    #values = zip(generator1(16807, parsed[0]), generator1(48271, parsed[1]))
    match_count = 0

    for step, a, b in zip(range(40_000_000), generator1(16807, parsed[0]), generator1(48271, parsed[1])):
        if not (step % 1_000_000):
            ic(step, match_count)

        if a & 0xffff == b & 0xffff:
            match_count +=1

    return match_count
    #ics(seq(values).take(5).list())


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def generator2(factor, seed, mod):
    val = seed

    while True:
        val = (val * factor) % 2147483647

        if val % mod == 0:
            yield val

def process2(parsed):
    ics(parsed)
    match_count = 0

    for step, a, b in zip(range(5_000_000), generator2(16807, parsed[0], 4), generator2(48271, parsed[1], 8)):
        if not (step % 1_000_000):
            ic(step, match_count)

        if a & 0xffff == b & 0xffff:
            match_count +=1

    return match_count



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
