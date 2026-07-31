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

import numpy as np
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
def parse(inp):
    return inp.split("\n")


# %% [markdown]
# # Process

# %%
def process(parsed):
    def char_at(p):
        #ics(p)
        c =  parsed[int(p.imag)][int(p.real)]
        #ics(p, c)
        return c

    ics(parsed)
    start = parsed[0].index("|")
    H = height(parsed)
    W = width(parsed)
    ic(H, W, start)

    steps = 0
    word = ""
    direction = 0+1j
    pos = start + 0j
    letters = set(chr(n + ord("A")) for n in range(26))
    #ics(letters)

    while True:
        c = char_at(pos)
        steps += 1
        #ic(steps, pos, c)

        if c == "+":
            possible = [direction * 1j, direction * -1j]
        else:
            if c in letters:
                word = word + c

            possible = [direction]

        #chk = [np for d in possible if 0 <= (np := pos + d).imag < H and 0 <= np.real < W]
        #ics(chk)
        positions = [(np, d) for d in possible if 0 <= (np := pos + d).imag < H and 0 <= np.real < W and char_at(np) != " "]
        #ics(pos, c, possible, positions)

        if not positions:
            break

        assert len(positions) == 1
        pos, direction = positions[0]

    ic(word, steps)
    return word, steps


# %%
def part1(inp):
    parsed = parse(inp)
    word, steps = process(parsed)
    print_result(word)


# %%
def part2(inp):
    parsed = parse(inp)
    word, steps = process(parsed)
    print_result(steps)


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
#ic(real_inp)
part1(real_inp)
part2(real_inp)
