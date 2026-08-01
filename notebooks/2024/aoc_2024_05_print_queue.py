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
sample_data1 = """
hijkl
"""
sample_data2 = sample_data1

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
    parts = inp.strip().split("\n\n")
    return seq(parts).map(string_to_integers_list).list()


# %% [markdown]
# # Process

# %%
def mid_num(update):
    return update[len(update) // 2]

def count_middles(updates):
    return seq(updates).map(mid_num).sum()

def correct_order(rule_set, update):
    for n, u in enumerate(update): 
        for b in update[:n]:
            if (u, b) in rule_set:
                #ics(n, u, b)
                return False
    return True                    

def process(parsed):
    #ics(parsed)
    rules, updates = parsed
    begins = defaultdict(list) # each element in list must be after key
    ends = defaultdict(list) # each element in list must be before key
    rule_set = seq(rules).map(tuple).set()
    #ics(rule_set)

    if 1:
        for b,e in rules:
            begins[b].append(e)
            ends[e].append(b)
        
        ics(begins, ends)
        
    for n, update in enumerate(updates):        
        if sum(e not in begins for e in update) > 1:
            ic(n, "not in begins")
            break
        if sum(e not in ends for e in update) > 1:
            ic(n, "not in ends")
            break
        continue            
        ics(update)
        ic(n, len(update), seq(update).count(lambda u: u not in begins))
        ic(n, seq(update).count(lambda u: u not in ends))

    correct_updates = seq(updates).filter(partial(correct_order, rule_set)).list()
    return count_middles(correct_updates)


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %%
#A comparison function is any callable that accepts two arguments, compares them, and returns a negative number for less-than, zero for equality, or a positive number for greater-than. A key function is a callable that accepts one argument and returns another value to be used as the sort key.
def cmp(rule_set, a, b):
    if (a, b) in rule_set:
        return -1
    if (b, a) in rule_set:
        return 1
    return 0

# we established that every element in the update is part of a rule
def reorder(rule_set, update):
    ics(update)
    corrected = sorted(update, key=cmp_to_key(partial(cmp, rule_set)))
    ics(corrected)
    return corrected

def process2(parsed):
#    ics(parsed)
    rules, updates = parsed
    rule_set = seq(rules).map(tuple).set()

    incorrect_updates = seq(updates).filter_not(partial(correct_order, rule_set))
    corrected = incorrect_updates.map(partial(reorder, rule_set)).list()
    
    #for n, update in enumerate(corrected):        
    #    ics(n, incorrect_updates[n], update, correct_order(rule_set, update))
        
    return count_middles(corrected)    


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
