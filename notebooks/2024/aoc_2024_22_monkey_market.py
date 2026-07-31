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
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module

# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
sample_data1s = [split_example(example)[0], """1
10
100
2024"""]
sample_data2 = """1
2
3
2024"""


# %% [markdown]
# # Parse

# %%
def parse_data(inp):
    return seq(inp.strip().split("\n")).map(int).list()


# %% [markdown]
# # Process

# %%
bin(16777216)


# %%
def mix_and_prune(n, a):
    return (n ^ a) % 16777216
    
def next_number(n):
    n = mix_and_prune(n, n * 64)
    n = mix_and_prune(n, n // 32)
    n = mix_and_prune(n, n * 2048)
    return n

def nth_number(sn, cnt):
    for n in range(cnt):
        sn = next_number(sn)
    return sn        

def process(parsed):
    #ics(parsed)
    return sum(nth_number(sn, 2000) for sn in parsed)


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
price_cnt = 2000
#price_cnt = 10

def get_prices(sn):
    return [sn % 10] + [(sn := next_number(sn)) % 10 for n in range(price_cnt)]

#ic(get_prices(123)[:10])

def price_diffs(prices):
    return [b-a for a, b in pairwise(prices)]

def prices_with_4diffs(prices, price_diffs):
    return list(zip(prices[4:], seq(price_diffs).sliding(4).map(tuple).list()))

def get_first_price_at_diffs(prices_with_4diffs):
    # we want only the first occurence of any difference, so by reversing eaelir occurrences overwrite older ones
    dct = dict((dif, price) for price, dif in reversed(prices_with_4diffs))
    #ics(dct.get((2, 0, 6, -4)))
    return dct

def best_prices_per_diffs(all_first_price_at_diffs):
    if 1:
        cnt = Counter()
        
        for first_price_at_diffs in all_first_price_at_diffs:
            cnt.update(first_price_at_diffs)

        return cnt.most_common(1)
    else:
        totals = defaultdict(int)
    
        for first_price_at_diffs in all_first_price_at_diffs:
            for dif, price in first_price_at_diffs.items():
                totals[dif] += price

        ics(totals[-2,1,-1,3])
        ics(sorted(totals.items(), key=second, reverse=True)[:10])
        return max(totals.items(), key=second)

def process2(parsed):
    ics(parsed)
    all_prices = map_list(get_prices, parsed)
    all_price_diffs = map_list(price_diffs, all_prices)
    #ics(all_price_diffs)
    #ics(seq(all_price_diffs).sliding(4).list())
    all_prices_with_4diffs = starmap_list(prices_with_4diffs, zip(all_prices, all_price_diffs))
    ics(all_prices[0][:10], all_price_diffs[0][:10], all_prices_with_4diffs[0][:10])
    all_first_price_at_diffs = map_list(get_first_price_at_diffs, all_prices_with_4diffs)
    #ics(all_first_price_at_diffs[0][:10])

    best_dif = best_prices_per_diffs(all_first_price_at_diffs)
    ics(best_dif)
    return best_dif[0][1]
    #best_dif_key = best_dif[0][0]
    #ics(best_dif_key)
    
    #ics(list(zip(all_prices)
    #bananas = sum(first_price_at_diffs.get(best_dif_key, 0) for first_price_at_diffs in all_first_price_at_diffs)
    #return bananas


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
