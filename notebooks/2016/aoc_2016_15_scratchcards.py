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
# [Advent of Code 2016 - Day 15](https://adventofcode.com/2016/day/15)

# %% editable=false jupyter={"source_hidden": true}
from utils.aoc_utils import *
if is_notebook():
    print(get_aoc_url())

# %%
# %load_ext autoreload

# %%
from collections import *

from icecream import ic
import pyperclip

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0]
sample_data2 = sample_data1

# %%
Disk = namedtuple("Disk","pos_count,t0pos")

def parse_line(line):
    nums = string_to_integers(line)
    return Disk(nums[1], nums[-1])

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def disk_pos_func(disk):
    def f(t):
        return (t + disk.t0pos) % disk.pos_count
    return f

def disk_pos0_func(disk):
    def f(t):
        return ((t + disk.t0pos) % disk.pos_count) == 0
    return f


def process(parsed):
    ics(parsed)
    if 0:
        cycles = [seq(range(disk.pos_count)).cycle().drop(disk.t0pos) for disk in parsed]

        for cycle in cycles:
            ics(cycle.take(5))

    cycle_funcs = [disk_pos_func(disk) for disk in parsed]
    cycle_cnt = len(parsed)

    for f in cycle_funcs:
        ics(seq(range(5)).map(f))

    cycle0_funcs = [disk_pos0_func(disk) for disk in parsed]

    found_index = seq(count()).find(lambda n: seq(range(n+1, n+cycle_cnt+1)).zip(cycle_funcs).for_all(lambda e: e[1](e[0]) == 0))
    return found_index


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %%
def part2(inp):
    parsed = parse(inp)
    parsed.append(Disk(11, 0))
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
part1(sample_data1)
part2(sample_data2)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)
