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
import sys
from collections import *

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from iter_utils import *
from aoc_utils import * # this includes adding c:\ut to sys.path
from utilities import *
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
#Disk = namedtuple("Disk","pos_count,t0pos")

def parse_line(line):
    parts = string_to_integers_list(line)
    return tuple(parts[:2]), tuple(parts[2:])

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def process(parsed):
    ic(len(parsed))
    #ics(parsed)
    H = height(parsed)
    W = width(parsed)
    ic(W, H)

    points, movements = list(zip(*parsed))
    #ics(parsed, points, movements)
    positions = points[:]
    #ics(maplist(itemgetter(1), positions))
    iterations = 0
    min_d = sys.maxsize
    last_positions = positions

        # this is based on the observation that over time the points contract until the message and then expand again
        # so once we detect that they're epxanding again, go back to the previous position
    while (d := analyze_dimension(map(itemgetter(1), positions)))[0] <= min_d:
        min_d = min(min_d, d[0])

        if iterations % 1000 == 0:
            ic(iterations, d[0], min_d)

        last_positions = positions
        positions = starmaplist(add_tuple, zip(positions, movements))
        iterations += 1

    xs, ys, *_ = xs_and_ys(last_positions)
    print(get_vis_map_multiline_str(xs, ys, reversed = False, min_val=None, max_val=None, special_chars=tuple(), blank_char =".", filled_char = "#"))
    return iterations-1, last_positions


# %%
def part1(inp):
    parsed = parse(inp)
    steps, last_positions = process(parsed)
    xs, ys, *_ = xs_and_ys(last_positions)
    s = get_vis_map_multiline_str(xs, ys, show_axis=False)
#    ics(s)
    print_result(ocr_aoc_letters(s), part="Part 1")
    print_result(steps, part="Part 2")

# %%

def part2(inp):
    parsed = parse(inp)
    result, _ = process(parsed)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())
print_preface_notebook()

for sample_data1 in sample_data1s:
    part1(sample_data1)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
print_preface_notebook()
part1(real_inp)
