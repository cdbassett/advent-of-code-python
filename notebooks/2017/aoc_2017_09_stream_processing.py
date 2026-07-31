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
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
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

# %%
def parse(inp):
    return inp.strip()


# %% [markdown]
# # Process

# %%
def skip_garbage(s):
    in_garbage = False
    skip_next = False

    for c in s:
        if in_garbage:
            if skip_next:
                skip_next = False
                continue

            if c == "!":
                skip_next = True
            elif c == ">":
                in_garbage = False
        elif c == "<":
            in_garbage = True
        else:
            yield c


def score(s, base_score = 0):
    group_score = 0

    for c in s:
        match c:
            case "{":
                group_score += score(s, base_score + 1)
            case "}":
                return group_score + base_score
            case ",":
                pass
            case _:
                raise Exception("Uknown char")

#    ics(group_score)
#    raise Exception("Uknown state")
    return group_score

def process(parsed):
    ics(parsed)
    ics(sjoin(skip_garbage(parsed)))
    #ics(score(skip_garbage(parsed)))
    return score(skip_garbage(parsed))


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def count_garbage(s):
    in_garbage = False
    skip_next = False
    cnt = 0

    for c in s:
        if in_garbage:
            if skip_next:
                skip_next = False
                continue

            if c == "!":
                skip_next = True
            elif c == ">":
                in_garbage = False
            else:
                cnt += 1
        elif c == "<":
            in_garbage = True
    return cnt

def process2(parsed):
    ics(parsed)
    return count_garbage(parsed)


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

part2("<<<<>")
part2("<{!>}>")
part2("<!!>")
part2("<!!!>>")
part2("<{o\"i!a,<{i<a>,")

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)
# 24529 is too high
