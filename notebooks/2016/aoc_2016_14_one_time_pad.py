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
# [Advent of Code 2016 - Day 14](https://adventofcode.com/2016/day/14)

# %% editable=false jupyter={"source_hidden": true}
from utils.aoc_utils import *
if is_notebook():
    print(get_aoc_url())

# %%
# %load_ext autoreload

# %%
from collections import *
import re

from icecream import ic
import iteration_utilities as it_ut
import pyperclip

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module

# %%
sample_data1 = """abc"""
sample_data2 = sample_data1


# %%
def parse(inp):
    return inp.strip()


# %% [markdown]
# # Process

# %%
reTriplets = re.compile(r"([\da-f])\1\1")

def process(get_hash, cnt):
    found = 0

    for n in count():
        hash = get_hash(n)
        m = reTriplets.search(hash)

        if m:
            scan = m.group(1) * 5

            if n < 100:
                ics(n, scan, hash)

            if seq(range(n+1,n+1001)).exists(lambda sn: scan in get_hash(sn)):
                found += 1
                #ics(n, scan, found)

        if found >= cnt:
            return n


# %%
def part1(inp):
    @lru_cache(maxsize=2001)
    def get_hash(index):
        return md5hex(parsed + str(index))

    parsed = parse(inp)
    result = process(get_hash, 64)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    pass


# %%
get_nth = it_ut.nth(2016)

def part2(inp):
    @lru_cache(maxsize=2001)
    def get_hash(index):
        return get_nth(it_ut.applyfunc(lambda s: hashlib.md5(s.encode("ascii")).hexdigest(), parsed + str(index)))

    parsed = parse(inp)
    result = process(get_hash, 64)
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
