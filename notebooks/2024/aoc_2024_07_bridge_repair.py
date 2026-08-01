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
from math import log10

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
    return string_to_integers_list(inp)


# %% [markdown]
# # Process

# %%
# this reduced runtime from 1:30 to 30
@cache
def build_ops(operators, cnt):
    return tuple(product(*repeat(operators, cnt - 1)))
    
def possible(operators, line):
    #ics(list(product(*repeat(operators, len(line) - 1))))
    total, first, second, *rest = line
    #assert all(n > 0 for n in line) # verified that all numbers are positive

    for ops in build_ops(operators, len(line) - 1):
        first_op = ops[0]
        chk = first_op(first, second)
        #last_op = ops[-1]

        for val, op in zip(rest, ops[1:]):
            if chk > total: # this seems to improve time but marginally
                break
                
            chk = op(chk, val)

        if chk == total:
            return total
    
    return 0

def process(parsed):
    ics(parsed)
    operators = (int.__add__, int.__mul__)
    return seq(parsed).map(partial(possible, operators)).sum()


# %%
# rewrote based on my understanding of anohter solution, time went down to 150ms for both together
def is_possible(total, values, include_concat=False):
    *rest, last = values
    #ics(total, values, rest, last)

    if not rest:
        return last == total
        
    quot, rem = divmod(total, last)

    if rem == 0:
        if is_possible(quot, rest, include_concat):
            return True

    if include_concat:
        assert total >= 0
        last_digits = count_integer_digits(last)
        #digits = count_integer_digits(total)
        str_total = str(total)
        #ics(str_total, last, last, str_total.endswith(str(last)), int(str_total[:-last_digits]))
        
        if str_total.endswith(str(last)):
            preceding = str_total[:-last_digits]
            
            if preceding and is_possible(int(preceding), rest, True):
                return True
        
        #a * 10**num_digits + b
    
    return total > last and is_possible(total-last, rest, include_concat)

def process(parsed):
    ics(parsed)
    #ics(is_possible(parsed[0][0], parsed[0][1:]))
    #ics(sum(total for total, *values in parsed))
    combined_total = sum(total for total, *values in parsed if is_possible(total, values))
    return combined_total


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def concatenation(a, b):
    #num_digits = int(math.log10(b)) + 1
    #ics(a, b, num_digits, 10**num_digits, a * 10**num_digits + b, int(str(a) + str(b)))
    #return a * 10**num_digits + b
    return int(str(a) + str(b))

def process2(parsed):
    #operators = (int.__add__, int.__mul__, concatenation)
    #return seq(parsed).map(partial(possible, operators)).sum()
    combined_total = sum(total for total, *values in parsed if is_possible(total, values, True))
    return combined_total


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
part2(real_inp) # 91377448644679
