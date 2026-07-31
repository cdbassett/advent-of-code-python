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
import os
import sys
from collections import *
import re
import math

from icecream import ic
import iteration_utilities as it_ut
from z3 import Int, Optimize, If, Real, Solver, Or, And

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
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
sample_data2 = sample_data1

# %%
for sample in sample_data1s:
    print(sample)
    print("=======================")

# %% [markdown]
# # Parse

# %%
Machine = namedtuple("Machine","lights,buttons,joltage")

def lights_to_bits(s):
    return int(sjoin(reversed(s)).replace("#","1").replace(".","0"), 2)

def button_to_bits(wiring):
    #ics(wiring)
    return sum(1 << n for n in wiring)
    
def buttons_to_bits(wiring):
    return seq(wiring).map(button_to_bits).to_tuple()

def parse_line(line):
    lights, *buttons, joltage = line.split()
    return Machine(lights_to_bits(lights[1:-1]), buttons_to_bits(string_to_integers_list("\n".join(buttons))), string_to_integers(joltage[1:-1]))

def parse_data(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def get_light_min_button_presses(lights, buttons, joltages):
    queue = []
    put, get = get_queue_functions_smallest(queue)
    put((0, lights.bit_count(), 0, buttons))

    while queue:
        #iterations += 1
        steps, diff_val, cur_val, rem_btns = get()
        
        for btn, other_btns in tuples_without(rem_btns):
            new_val = cur_val ^ btn
            
            if new_val == lights:
                return steps+1
                
            put((steps+1, (new_val ^ lights).bit_count(), new_val, other_btns))
            
# max button index is 9
# max lights is 10
# max num of buttons is 13
# highest joltage is 286
def process(parsed):
    ics(parsed)
    #ic(seq(parsed).map(second_elem).level2_map(max).map(max).max())
    #ic(seq(parsed).map(third_elem).map(max).max()) # highest joltage
    #ic(seq(parsed).map(second_elem).map(len).max()) # max num of buttons
    #ic(seq(parsed).map(first_elem).map(bin).map(len).max()-2) # max lights
    return seq(parsed).starmap(get_light_min_button_presses).sum()


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
@cache
def get_set_bits(val):
    return tuple(iterate_set_bits(val))

# this turned out to be extremely slow for even thae sample
# the problem was that each pass brought the possibility of each button, but in reality the order of pressign doesn't matter and was greatly expanding the problem area
# also there's no need to do one button press at a time
def get_joltage_min_button_presses(lights, buttons, joltages):
    queue = []
    put, get = get_queue_functions_smallest(queue)
    put((0, sum(joltages), [0] * len(joltages)))
    ics(buttons, joltages)
    #buttons = [n if 1 << n & buttons else 0 for n in range(len(joltages))]
    #ics(buttons)
    iterations = 0

    while queue:
        iterations += 1
        steps, diff_val, cur_val = get()
        #ics("  ", steps, diff_val, cur_val)

        if not iterations % 10000:
            ics("  ", steps, diff_val, cur_val)
            
        for btn in buttons:
            new_val = cur_val[:]

            for idx in get_set_bits(btn):
                new_val[idx] += 1
            
            if new_val == joltages:
                return steps+1

            comp = list(zip(new_val, joltages))

            if any(a > b for a, b in comp):
                #ics("    exceeded", new_val)
                continue

            diff_val = sum(b - a for a, b in comp)
            #ics("    ", btn, new_val, diff_val)
            put((steps+1, diff_val, new_val))

# max number of times any button can be pressed can be determined by smallest of joltages it affects

def get_joltage_min_button_presses(lights, buttons, joltages):
    ics(buttons, joltages)

    if 0:
        for btn in buttons:
            m = min(joltages[idx] for idx in get_set_bits(btn))
            ics("  ", btn, m, get_set_bits(btn))
            
    opt = Optimize()
    bpresses = [Int("b"+str(n)) for n, btn in enumerate(buttons)]
    btn_indices = [[] for _ in joltages]
    
    for btn, bpress in zip(buttons, bpresses):
        for idx in get_set_bits(btn):
            btn_indices[idx].append(bpress)
        opt.add(bpress >= 0)
            
    for b, j in zip(btn_indices, joltages):          
        opt.add(j == sum(b))

    bpress_count = Int("bpc")
    opt.add(bpress_count == sum(bpresses))
    d = opt.minimize(bpress_count)

    ics(opt.check())
    #ics(opt.lower(d))
    model = opt.model()
    #ics(model)
    ics(model[bpress_count])
    return model[bpress_count].as_long()

def process2(parsed):
    #ics(parsed)
    return seq(parsed).starmap(get_joltage_min_button_presses).sum()


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

# %%
int("0110",2)
int("0110",2).bit_count()

# %% [markdown]
# # Others' solutions
