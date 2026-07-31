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

# %%
import aocd
from collections import *
import re

from icecream import ic

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from iter_utils import *
import utils.seq_extensions as seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

# %%
# %load_ext autoreload
# %autoreload 2


# %%
def parse_line(line):
    pieces = line.replace("rotate ", "").split()
    nums = string_to_integers(line)
    return (pieces[0],) + tuple(nums)


# %%
def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %%
reSearch = re.compile(r"\((\d+)x(\d+)\)")


# %%
def part1(inp):
    remaining = inp
    decompressed = ""

    while match := reSearch.search(remaining):
        lngth, cnt = int(match.group(1)), int(match.group(2))
        pat_start = match.end(0)
        pat_end = pat_start + lngth
        decompressed += remaining[:match.start(0)] + remaining[pat_start:pat_end] * cnt
        remaining = remaining[pat_end:]

    decompressed += remaining
    result = len(decompressed)
    #ics(decompressed)
    print_result(result)


# %%
def decomp_count(s, level = 0):
    #ics(" " * level, level, s, len(s))
    remaining = s
    decompressed = 0

    while match := reSearch.search(remaining):
        lngth, cnt = int(match.group(1)), int(match.group(2))
        pat_start = match.end(0)
        pat_end = pat_start + lngth
        decompressed += match.start(0) + decomp_count(remaining[pat_start:pat_end], level+1) * cnt
        remaining = remaining[pat_end:]

    decompressed += len(remaining)
    #ics(" " * level, level, decompressed)
    return decompressed


# %%
def part2(inp):
    result = decomp_count(inp)
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
samp_inp1 = """
ADVENT
A(1x5)BC
(3x3)XYZ
A(2x2)BCD(2x2)EFG
(6x1)(1x3)A
X(8x2)(3x3)ABCY
"""
for line in samp_inp1.strip().split("\n"):
    part1(line)

samp_inp2 = """
(3x3)XYZ
X(8x2)(3x3)ABCY
(27x12)(20x12)(13x14)(7x10)(1x12)A
(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN
"""
for line in samp_inp2.strip().split("\n"):
    part2(line)

# %% [markdown]
# # Actual data

# %%
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)

# %%
