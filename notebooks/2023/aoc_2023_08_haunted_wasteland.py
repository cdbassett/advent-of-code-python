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
import math

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
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
sample_data2 = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)""".strip()

# %%
print(sample_data1)


# %% [markdown]
# # Parse

# %%
def parse(inp):
    [rl], l = seq(seq(inp.strip().replace("=","").replace(",","").replace("(","").replace(")","").split("\n")).split())
    return rl, seq(l).map(str.split).map(tuple).list()


# %% [markdown]
# # Process

# %%
def process(parsed):
    #ics(parsed)
    rl, lst = parsed
    dct = dict((a, (b, c)) for a, b, c in lst)
    #ics(dct)
    nxt = "AAA"
    idx = { "R": 1, "L": 0 }

    for n, c in enumerate(cycle(rl), 1):
        ics(nxt, c)
        nxt = dct[nxt][idx[c]]

        if nxt == "ZZZ":
            return n

    return 0


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    def find_cycle(nxt):
        for n, c in enumerate(cycle(rl), 1):
            nxt = dct[nxt][idx[c]]

            if nxt.endswith("Z"):
                return n

    #ics(parsed)
    ic(len(parsed))
    rl, lst = parsed
    dct = dict((a, (b, c)) for a, b, c in lst)
    #ics(dct)
    idx = { "R": 1, "L": 0 }
    nxt = [k for k in dct.keys() if k.endswith("A")]
    cycles = [find_cycle(n) for n in nxt]
    ic(cycles)
    ic(len(nxt))

    return math.lcm(*cycles)

    if 0:
        for n, c in enumerate(cycle(rl), 1):
            i = idx[c]
            nxt = [dct[n][i] for n in nxt]
            ics(nxt, c, i)

            if n % 1000000 == 0:
                ic(n, c, i, nxt)

            if all(n.endswith("Z") for n in nxt):
                return n

    return 0



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
sample_data1 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

part1(sample_data1)
part2(sample_data2)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)
