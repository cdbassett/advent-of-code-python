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
# [Advent of Code 2018 - Day 18](https://adventofcode.com/2018/day/18)

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
from icecream import ic
from scipy.ndimage import generic_filter

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
sig_chars = ".|#"
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
    ctr = Counter(image)

    match c:
        case 0:
            return int(ctr.get(1, 0) >= 3)
        case 1:
            return 2 if ctr.get(2, 0) >= 3 else 1
        case 2:
            return 2 if ctr.get(2, 0) >= 2 and ctr.get(1, 0) >= 1 else 0 # must account for central lumberyard being included int counter
        case _:
            raise Exception("unbknwon type!")

    return image[len(image) // 2]

def a_to_c(n):
    return sig_chars[n]

a_to_c = sig_chars.__getitem__ # same effect but should be faster bc using existing function
a_to_c = np.vectorize(a_to_c)

def one_pass(input):
    return generic_filter(input, filter_func, size=(3,3), mode="constant")

# worked but didn't seem any faster
#one_pass = partial_right(generic_filter, ff, size=(3,3), mode="constant")

def resource_value(input):
    unique, counts = np.unique(input, return_counts=True)
    #ics(unique, counts)
    ctr = dict(zip(unique, counts))
    return ctr.get(1, 0) * ctr.get(2, 0)

def process(parsed, minutes=10):
    ic(len(parsed))
    ics(parsed)
    #print(get_numpy_char_array_repr(a_to_c(parsed)))
    H = height(parsed)
    W = width(parsed)
    ic(W, H)
    res = parsed

    for n in range(minutes):
        res = one_pass(res)

    #print(get_numpy_char_array_repr(a_to_c(res)))
    return resource_value(res)


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def arr_2_hash(arr):
    return sjoin(a_to_c(arr).flatten())

def generator(parsed):
    res = parsed

    while True:
        res = one_pass(res)
        yield arr_2_hash(res)

def process2(parsed):
    final = predict(generator(parsed), 1000000000)
    # alternate more functional method that seems slower (only tested once though)
    #final = predict(map(arr_2_hash, it_ut.applyfunc(one_pass, parsed)), 1000000000)
    ics(final)
    final_arr = np.array(maplist(char_lookup, final)) # no need to reshape, we're just counting, which works regardless of shape
    return resource_value(final_arr)


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

part2(sample_data1) # pretty meaningless for sample

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp) # 514944
part2(real_inp) # 193050
