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
from scipy.ndimage import generic_filter

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
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

# %% [markdown]
# # Parse

# %%
sig_chars = ".#"
sig_chars_lookup = dict(zip(sig_chars, count()))

def char_lookup(l):
    return maplist(sig_chars_lookup.get, l)
    #return list(sig_chars_lookup[c] for c in l)

def parse(inp):
    return build_numpy_array_from_string_graph(inp, char_lookup)


# %% [markdown]
# # Process

# %%
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.generic_filter.html#scipy.ndimage.generic_filter
def filter_func(image):
    #ics(image)
    #print(image)
    c = image[len(image) // 2]
    neighbor_bugs = image[1:9:2] # top, left, right, bottom
    cnt = sum(neighbor_bugs)

    if c:
        return cnt == 1
        
    return cnt == 1 or cnt == 2

def a_to_c(n):
    return sig_chars[n]

a_to_c = sig_chars.__getitem__ # same effect but should be faster bc using existing function
a_to_c = np.vectorize(a_to_c)

def one_pass(input):
    return generic_filter(input, filter_func, size=(3,3), mode="constant", cval=0)

def arr_2_hash(arr):
    return sjoin(a_to_c(arr).flatten())

def biodiversity_rating(arr):
    s = sjoin(map(str, arr.flatten()))
    #s = sjoin(map(str, arr.flatten()))[::-1]
    return int(s, 2)

def process(parsed, minutes=10):
    ic(len(parsed))
    #ics(parsed)
    #print(get_numpy_char_array_repr(a_to_c(parsed)))
    H = height(parsed)
    W = width(parsed)
    ic(W, H)
    res = parsed
    seen = set([arr_2_hash(res)])

    for n in count():
        res = one_pass(res)
        hashed = arr_2_hash(res)

        #if is_sample and n < 5:
        #    print("step:", n, "\n", get_numpy_char_array_repr(a_to_c(res.T), show_axis=False))

        if hashed in seen:
            ics(n)
            break

        seen.add(hashed)

    #print(get_numpy_char_array_repr(a_to_c(res.T)))
    return biodiversity_rating(res)


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %% [markdown]
# track with set
# each node is the index into 5x5 and level
# set up dictionary with inner and outer conenctions (dicstinct because need to know whether level is increasing or decreasing)
# each stage, track nodes already processed
# go through all prsent node (representing the ones) and process them. While doing so, track all the neighbors of ones in a set that are zero
# that set is then zeros that need to be processed

# %%
connections = defaultdict(set)

# outer decreases level, inner increases
def form_double_connection(a1, a2, level = 0):
    connections[a1].add((a2, level))
    connections[a2].add((a1, -level))

# top row to outer
for n in range(1, 6):
    form_double_connection(n, 8, -1)

# bottom row to outer
for n in range(21, 26):
    form_double_connection(n, 18, -1)

# left side to outer
for n in range(1, 26, 5):
    form_double_connection(n, 12, -1)

# right side to outer
for n in range(5, 26, 5):
    form_double_connection(n, 14, -1)
    
x_y_to_straight = dict(zip(((x, y) for y, x in product(range(5), range(5))), count(1)))
#ic(x_y_to_straight)

# normal connections
#for (x1, x2), (y1, y2) in product(pairwise(range(5)), pairwise(range(5))):
for xs, ys in product(pairwise(range(5)), pairwise(range(5))):
    #ic(list(product(ys, xs)))
    a1, b1, a2, b2 = map(x_y_to_straight.get, product(ys, xs))
    #ic(a1, a2, b1, b2)
    #a1, a2, b1, b2 = map(x_y_to_straight.get, (x1, x2, y1, y2))
    
    if 13 not in (a1, a2, b1, b2):
        form_double_connection(a1, a2) # top
        form_double_connection(a1, b1) # left
        form_double_connection(b1, b2) # nottom
        form_double_connection(a2, b2) # right
        
#ic(connections)        
for i, s in connections.items():
    assert len(s) in (4,8)


def process2(parsed):
    def neighbor_is_one(nb):
        #ics(nb, nb[0] in ones) 
        return nb in ones
        
    minutes = 10 if is_sample else 200
    flat = parsed.T.flatten()
    positions = np.argwhere(flat == 1)+1
    #ics(flat, positions)
    ones = set((int(n), 0) for n in positions)
    #ics(ones)

    for step in range(minutes):
        zeros = set() # these are locations that need to be checked to see if they've become filled
        new_ones = set()
        #ics(step, ones)

            # only add existing ones if still meet criteria
        for loc in ones:
        #for loc in sorted(ones):
            pos, level = loc
            neighbors = [(i, level + add_level) for i, add_level in connections[pos]]
            nb_zeros, nb_ones = partition(neighbor_is_one, neighbors)
            #nb_zeros, nb_ones = list(nb_zeros), list(nb_ones)
            #ics(pos, level, neighbors, nb_zeros, nb_ones)
            zeros.update(nb_zeros)
            #zeros.update((i, level + add_level) for i, add_level in nb_zeros)
            
            if quantify(nb_ones) == 1:
                new_ones.add(loc)
            #else:
            #    ics("    dead bug", loc, neighbors)
                
        #ics(zeros)
                
            #  add neighbors of existing ones if meet criteria to become one
        for loc in zeros:
        #for loc in sorted(zeros):
            pos, level = loc
            neighbors = [(i, level + add_level) for i, add_level in connections[pos]]
            
            if quantify(neighbors, neighbor_is_one) in (1,2):
                #ics("    new bug", loc, neighbors)
                new_ones.add(loc)
        ones = new_ones    
        
    #ics(sorted(ones))
    return len(ones)


# %%
def part2(inp):
    parsed = parse(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

for sample_data1 in sample_data1s:
    part1(sample_data1)

part2(sample_data1)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp) # 
part2(real_inp) # 
