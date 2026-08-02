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
# [Advent of Code 2024 - Day 9](https://adventofcode.com/2024/day/9)

# %% editable=false jupyter={"source_hidden": true}
from utils.aoc_utils import *
if is_notebook():
    print(get_aoc_url())

# %% [markdown]
# # Imports

# %%
# %load_ext autoreload

# %%
import os
import sys
from collections import *
import re
import math

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
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


# %% [markdown]
# # Parse

# %%
def parse_data(inp):
    return maplist(int, inp)


# %% [markdown]
# # Process

# %%
def check_sum(expanded):
    return seq(expanded).enumerate().where(lambda e: e[1] >= 0).smap(operator.mul).sum()
    
def digit_repr(l):
    return sjoin(map(lambda s:"." if s == -1 else str(s), l))
    
def from_back(d):
    while d:
        n, cnt = d.pop()
        yield from repeat(n // 2, cnt)
        if d:
            d.pop()


# %%
def process(parsed):
    ics(parsed)
    expanded = []
    ics(digit_repr(enumerate(parsed)))
    ics(digit_repr(from_back(deque(enumerate(parsed)))))
    d = deque(enumerate(parsed))
    back = from_back(d)
    
    try:
        while d:
            b, cnt = d.popleft()
            expanded.extend([b // 2] * cnt)
            _, cnt = d.popleft()
    
            for i in range(cnt):
                expanded.append(next(back))
    except IndexError:
        pass
        
    expanded.extend(back)
    ics(digit_repr(expanded))
    return check_sum(expanded)


# %%
# redone as generator
def files(parsed):
    d = deque(enumerate(parsed))
    back = from_back(d)
    
    try:
        while d:
            b, cnt = d.popleft()
            yield from [b // 2] * cnt
            _, cnt = d.popleft()
            yield from islice(back, cnt)
    except IndexError:
        pass
        
    yield from back

def process(parsed):
    return check_sum(files(parsed))


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def check_sum_block(block):
    return sum(block[2] * n for n in range(block[1], block[1] + block[0]))

def process2(parsed):
    gaps = [] # length, pos
    blocks = [] # length, pos, block_num
    l = 0

    for block_num, (block_length, gap_length) in enumerate(batched(parsed + [0], 2)):
        blocks.append((block_length, l, block_num))
        l += block_length
        gaps.append((gap_length, l))
        l += gap_length

    #ics(blocks)

    for block_length, block_pos, block_num in reversed(blocks[1:]):
        for gap_index, (gap_length, gap_pos) in enumerate(gaps):
            if gap_pos > block_pos:
                break
            elif gap_length >= block_length:
                blocks[block_num] = block_length, gap_pos, block_num
                
                if gap_length == block_length:
                    del gaps[gap_index]
                else:
                    gaps[gap_index] = gap_length - block_length, gap_pos + block_length
                break                    
    #ics(blocks)
    #pyperclip.copy(njoin(seq(expanded).map(str)))
    return seq(blocks).map(check_sum_block).sum()


# %%
def part2(inp):
    parsed = parse_data(inp)
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
