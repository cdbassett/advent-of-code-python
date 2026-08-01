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
import os
import sys
from collections import *
import re
import math

from icecream import ic
import iteration_utilities as it_ut

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions # when running standalone, apparently need this import explicitly in main module

# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
example

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
def parse_data(inp):
    return CharTable(inp.strip().split("\n"))


# %% [markdown]
# # Process

# %%
def setup(parsed):
    start = next(parsed.get_char_coords("S"))
    ics(parsed)
    splitters = set(parsed.get_char_coords("^")) 
    ic(len(splitters))
    ic(start, parsed.w, parsed.h)
    return start, splitters

def process(parsed):
    start, splitters = setup(parsed)
    queue = [(0, start)]
    put, get = get_queue_functions_lifo(queue)
    splits = set()
    processed = set()

    def add_move(move):
        p = add_tuple(pos, move)
        
        if parsed.valid(*p) and p not in processed:
            put((steps+1, p))
            processed.add(p)
        
    while queue:
        steps, pos = get()

#        if not steps % 10:
#            ics(steps, len(queue))
        
        if pos in splitters:
            add_move(move_left)
            add_move(move_right)
            splits.add(pos)
        else:
            add_move(move_down)

    #ics(len(splits), splits)
    return len(splits)


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    start, splitters = setup(parsed)
    queue = deque([(0, start)])
    put, get = get_queue_functions_fifo(queue)
    timeline_gen = count(1)
    step = 0

    def add_move(timeline, move, new_t=False):
        p = add_tuple(pos, move)
        
        if parsed.valid(*p):
            put((next(timeline_gen) if new_t else timeline, p))

    while queue:
        step = step + 1
        timeline, pos = get()
        #ics(step, len(queue), timeline, pos)
        
        if not step % 1000:
            ic(step, len(queue), timeline, pos)

        #if not steps % 10:
        #          ics(steps, len(queue))
        
        if pos in splitters:
            add_move(timeline, move_left)
            add_move(timeline, move_right, True)
            #splits.add(pos)
        else:
            add_move(timeline, move_down)

    ics(next(timeline_gen))

def process2(parsed):
    start, splitters = setup(parsed)

    @cache
    def new_timelines(pos):
        if not parsed.valid(*pos):
            return 0
            
        if pos in splitters:
            return 1 + new_timelines(add_tuple(pos, move_left)) + new_timelines(add_tuple(pos, move_right))

        return new_timelines(add_tuple(pos, move_down))
                    
    return 1 + new_timelines(start)        


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
