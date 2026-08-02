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
# [Advent of Code 2018 - Day 9](https://adventofcode.com/2018/day/9)

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
    return string_to_integers_list(inp)


# %% [markdown]
# # Process

# %%
def process(parsed):
    ic(len(parsed))
    ics(parsed)
    player_count, max_marble = parsed

    players = cycle(range(player_count))
    dq = deque([0])
    player_scores = [0] * player_count

    for marble, player in zip(range(1, max_marble+1), players):
        if marble % 23 == 0:
            player_scores[player] += marble
            dq.rotate(7)
            player_scores[player] += dq.popleft()
        else:
            dq.rotate(-2)
            dq.appendleft(marble)
        #ics(dq)

    #ics(player_scores)
    return max(player_scores)


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %%
def part2(inp):
    parsed = parse(inp)
    parsed = parsed[0], parsed[1] * 100
    result = process(parsed)
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
