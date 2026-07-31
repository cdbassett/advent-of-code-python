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
from collections import *

from icecream import ic
import pyperclip
import portion as P

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
sample_data1 = """
5-8
0-2
4-7
"""
sample_data2 = sample_data1


# %% [markdown]
# # Parse

# %%
def parse_line(line):
    return seq(line.split("-")).map(int).list()

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def process(parsed):
    ics(parsed)
    intervals = seq(parsed).starmap(P.closed).reduce(lambda a, b: a | b).list()
    ics(intervals)
    last = 0

    for interv in list(intervals):
        lo = interv.lower
        hi = interv.upper
        ics(last, lo, hi)

        if lo > last:
            return last

        last = hi + 1


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)

# %% [markdown]
# # Process2

# %%
def process2(parsed):
    ics(parsed)
    intervals = seq(parsed).starmap(P.closed).reduce(lambda a, b: a | b).list()
    ics(intervals)
    last = 0
    total = 0

    for interv in list(intervals):
        lo = interv.lower
        hi = interv.upper
        ics(last, lo, hi)

        if lo > last:
            total += lo - last

        last = hi + 1

    m = 9 if is_sample else 4294967295
    return total + m - last + 1


# %%
def part2(inp):
    parsed = parse(inp)
    result = process2(parsed)
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

