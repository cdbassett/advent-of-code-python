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

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
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

# %%
print(sample_data1)


# %% [markdown]
# # Parse

# %%
def parse(inp):
    return seq(inp.strip().split("\n")).split().list()


# %% [markdown]
# # Process

# %%
def process(parsed, match_func=operator.eq):
    ics(parsed)
    total = 0

    for n, pattern in enumerate(parsed):
        H = height(pattern)
        W = width(pattern)
        ics(n, W, H)
        ics(pattern)
        matched = False

        for top_cnt in range(1, H):
            use_count = min(top_cnt, H - top_cnt)
            ics(top_cnt, use_count)
            a, b = pattern[top_cnt-use_count:top_cnt], list(reversed(pattern[top_cnt:top_cnt + use_count]))
            ics(a)
            ics(b)

            if match_func(a, b):
                ics("match horiz")
                total += 100 * top_cnt
                matched = True
                break

        if not matched:
            for left_cnt in range(1, W):
                use_count = min(left_cnt, W - left_cnt)
                ics(left_cnt, use_count)
                a, b = [line[left_cnt-use_count:left_cnt] for line in pattern], [sjoin(reversed(line[left_cnt:left_cnt + use_count])) for line in pattern]
                ics(a)
                ics(b)

                if match_func(a, b):
                    ics("match vert")
                    total += left_cnt
                    matched = True
                    break

        if not matched:
            raise Exception(f"Couldn't find split for pattern {n}!")

    return total


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %%
# just need to know that one of the patterns has one more hash than the other
def match2(a, b):
    #return abs(len(build_points(a)) - len(build_points(b))) == 1
    return len(build_points(a) ^ build_points(b)) == 1


# %%
def part2(inp):
    parsed = parse(inp)
    result = process(parsed, match2)
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
part1(sample_data1)
part2(sample_data2)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)
# 25341 is too low
