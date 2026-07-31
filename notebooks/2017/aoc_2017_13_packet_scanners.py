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
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from aoc_utils import * # this includes adding c:\ut to sys.path
from utilities import *
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

# %%
for sample in sample_data1s:
    print(sample)
    print("=======================")


# %% [markdown]
# # Parse

# %%
def parse_line(line):
    return string_to_integers(line)

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).dict()


# %% [markdown]
# # Process

# %%
def scanner_pos(pico, rng):
    if rng == 1:
        return 0
    if rng == 2:
        return pico % 2
    m = rng - 1
    return m - abs((pico % (rng*2-2)) - m)

def process(parsed):
    ics(parsed)
    penalty = 0

        # part1 is if packet leaves at pico=0, so depth == pico
    for depth, rng in parsed.items():
        ics(depth, rng, depth % rng)

        if scanner_pos(depth, rng) == 0:
            ics(depth * rng)
            penalty += depth * rng

    return penalty


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    ics(parsed.items())

    for start_pico in count():
        if start_pico % 1000000 == 0:
            ic(start_pico)

        for depth, rng in parsed.items():
            if scanner_pos(start_pico+depth, rng) == 0:
                break
        else:
            return start_pico

    return None


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
