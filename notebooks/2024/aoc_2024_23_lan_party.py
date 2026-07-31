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

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from iter_utils import *
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
def parse_line(line):
    return line.split("-")

def parse_data(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def setup(parsed):
    connections = defaultdict(set)

    for a, b in parsed:
        connections[a].add(b)
        connections[b].add(a)
        
    return connections

def next_conn(connections, items):
    ics(items)
    new_items = set()
    
    for conn_item in items:
        common = sets_intersection(connections[e] for e in conn_item)

        for c in common:
            new_items.add(tuple(sorted(conn_item + (c,))))

    return new_items    

def process(parsed):
    connections = setup(parsed)
    triples = next_conn(connections, map(tuple, parsed))
    if 0:
        triples = set()
        
        for a, b in parsed:
            common = connections[a] & connections[b]
    
            for c in common:
                triples.add(tuple(sorted((a, b, c))))

    #ics(len(triples), triples)        
    cnt = sum(1 for t in triples if any(e.startswith("t") for e in t))
    return cnt


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    connections = setup(parsed)
    last_valid_items = new_items = next_conn(connections, map(tuple, parsed))

    while new_items:
        ics(len(first(new_items)))
        last_valid_items = new_items
        new_items = next_conn(connections, new_items)
        ics(new_items)

    #ics(len(first(last_valid_items)), len(last_valid_items), last_valid_items)
    return ",".join(first(last_valid_items))


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

# %% [markdown]
# # Others' solutions
