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

import numpy as np
import scipy
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

# %%
for sample in sample_data1s:
    print(sample)
    print("=======================")


# %% [markdown]
# # Parse

# %% [markdown]
# I solved this myself but lost the code (changed the code before the save as instead of after). So this time around I'm borrowing.
# * https://cutonbuminband.github.io/AOC/qmd/2018.html#day-12-subterranean-sustainability

# %%
def parse_data(inp):
    return inp.strip().split("\n")
    #return build_numpy_array_from_string_graph(inp)


# %% [markdown]
# # Process

# %%
def setup(parsed):
    def update(cell_neighbors):
        #return 1 * (not abs(np.array(alive) - cell_neighbors).sum(axis=1).min())
        # process every rule at once with subtraction
        # every position that matches will be a 0, every one that doesn't will be a 1
        # the sum of each row will be 0 if match, greater than 0 if not
        # the min of those sums will be zero if one matched, greater than 0 if not
        # not means true if one matched
        # *1 turns it into a 1 or 0
        return 1 * (not abs(alive - cell_neighbors).sum(axis=1).min())
        
    #ics(parsed)
    lookup = {".": 0, "#": 1}
    initial_state = [lookup[char] for char in parsed[0] if char in lookup]
    rules = [line.split(" => ") for line in parsed[2:]]
    alive = np.array([[lookup[x] for x in rule[0]] for rule in rules if lookup[rule[1]] == 1])
    return update, initial_state, alive
    
def process(parsed):
    update, initial_state, alive = setup(parsed)
    generations = 20
    state = np.pad(initial_state, generations)
    states = [state.copy()]
    #ics(alive, states)

    for i in range(generations):
        state = scipy.ndimage.generic_filter(state, update, footprint=np.ones(5), mode="constant")
        states.append(state.copy())

    # the indexes each plant would have if we actually went negative for the left side
    indices = np.arange(state.shape[0]) - generations
    #ics(indices)
    return (indices * state).sum()    


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %%
def process2(parsed):
    update, initial_state, alive = setup(parsed)
    generations = 150
    state = np.pad(initial_state, generations)
    states = [state.copy()]
    
    for i in range(1, generations):
        new_state = scipy.ndimage.generic_filter(state, update, footprint=np.ones(5), mode="constant")
        states.append(new_state.copy())

        # if this state looks just like the last state but shifted by one
        if (new_state == np.roll(state, 1)).all():
            break
            
        state = new_state
    return (
        ((np.arange(new_state.shape[0]) - generations) + (50_000_000_000 - i)) * new_state
    ).sum()    


# %% [markdown]
# # Process2

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
