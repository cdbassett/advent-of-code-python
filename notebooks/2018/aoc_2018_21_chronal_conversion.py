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
# [Advent of Code 2018 - Day 21](https://adventofcode.com/2018/day/21)

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
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils, aoc_2018_computer
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module
import aoc_2018_computer


# %% [markdown]
# # Parse

# %%
def parse_line(line):
    ics(line)
    return list(multimap(line.split(), identity, int, int, int))

def parse(inp):
    lines = inp.strip().split("\n")
    return string_to_integers(lines[0]), seq(lines[1:]).map(str.split).multimap(identity, int, int, int).list()


# %% [markdown]
# # Process

# %%
A, B, C, D, E, F = range(6)

def process(parsed):
    ip_idx, instructions = parsed

    for registers in aoc_2018_computer.run_instructions_with_ip_gen(instructions, ip_idx, [0] * 6):
        if registers[ip_idx] == 28:
            return registers[D]


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def part2(inp):
    if not is_sample:
        print_result(10721810) # calculated separately


# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
print_preface_notebook()
part1(real_inp) # 2792537
part2(real_inp) # 10721810

# %% [markdown]
# # Analysis

# %%
import aoc_2018_computer
parsed = parse(real_inp)
ip_idx, instructions = parsed
ic(ip_idx)
aoc_2018_computer.analyze_instructions(instructions, ip_idx)

