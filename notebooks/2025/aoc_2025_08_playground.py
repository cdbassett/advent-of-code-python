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
# [Advent of Code 2025 - Day 8](https://adventofcode.com/2025/day/8)

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
def parse_line(line):
    return line

def parse_data(inp):
    #return seq(inp.strip().split("\n")).map(parse_line).list()
    return string_to_integers_list(inp)


# %% [markdown]
# # Process

# %%
def connect(parsed, cnt=10): 
    points = maplist(tuple, parsed)
    ics(len(points))
    distances = list()
    put, get = get_queue_functions_smallest(distances)

    for a, b in combinations(points, 2):
        put((distance(a, b), a, b))

    ic(len(distances))
    networks = defaultdict(list)
    
    for n in range(cnt):
        #if not (conn := get()): 
        if not distances: 
            break
            
        d, a, b = get()
        
        if not distances: 
            ics(d, a, b)
            
        an = networks.get(a)
        bn = networks.get(b)

        if an and bn:
            if an != bn:
                network = an + bn
                lasta, lastb = a, b                    
                
                for a in network:
                    networks[a] = network
                ics(a, b, an, bn, network)                    
        elif an:
            if b in an:
                continue
            an.append(b)
            networks[b] = an
            lasta, lastb = a, b                    
            #ics(an)
        elif bn:
            if a in bn:
                continue
            bn.append(a)
            networks[a] = bn
            lasta, lastb = a, b                    
            #ics(bn)
        else:
            network = [a, b]
            networks[a] = network
            networks[b] = network

    return networks, lasta, lastb
    
def process(parsed, cnt=10):
    networks, a, b = connect(parsed, cnt)
    #ics(parsed)
    final_networks = list(set(seq(networks.values()).map(tuple)))
    #ics(seq(final_networks).map(len).zip(final_networks).sorted().list())
    return math.prod(seq(final_networks).map(len).sorted(reverse=True).take(3))


# %%
def part1(inp, cnt=10):
    parsed = parse_data(inp)
    result = process(parsed, cnt)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    networks, a, b = connect(parsed, 1_000_000_000_000)
    ics(a, b)
    return a[0] * b[0]


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
ic(real_inp.split("\n")[:3])
insert_sample_functions(True, globals())
part1(real_inp, 1000) # not 2744, 900, 1452
part2(real_inp)
