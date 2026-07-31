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

# %%
# %load_ext autoreload

# %%
from collections import *
import math

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from aoc_utils import * # this includes adding c:\ut to sys.path
from utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module

# %%
sample_data1 = """
Time:      7  15   30
Distance:  9  40  200
"""
sample_data2 = sample_data1


# %%
def parse(inp):
    values = seq(inp.strip().split("\n")).map(string_to_integers).list()
    return values


# %% [markdown]
# # Process

# %%
def calc_dist(button_dur, time):
    res = button_dur * (time - button_dur)
    #ics(button_dur, time, res)
    return res
"""
dist = button_dur * (time - button_dur) = button_dur*time - button_dur^2 = button_dur * (time - button_dur)
0 = -button_dur^2 + button_dur*time  - dist
a = -1, b = time, c = -dist
x = (-b ± √ (b^2 - 4ac) )/2a = (-time +- sqrt(time^2 -4*dist))/(-2)
"""
    # parabolic equation means we should
def calc_margin(time, beat_dist):
    start_time = 1
    end_time = time-1
    ics(beat_dist)

    while (dist := calc_dist(start_time, time)) < beat_dist:
        start_time += 1
        #ics(dist, start_time)

    while (dist := calc_dist(end_time, time)) < beat_dist:
        end_time -= 1
        #ics(dist, end_time)

    margin = end_time - start_time + 1
    ics(start_time, end_time, margin)
    return margin

    # quadratic equation solving
def calc_margin(time, beat_dist):
    time1 = math.ceil((-time + math.sqrt(time**2 -4*beat_dist))/-2)
    time2 = math.floor((-time - math.sqrt(time**2 -4*beat_dist))/-2)
    return time2 - time1 + 1

def process(parsed):
    ic(parsed)
    margins = seq(zip(*parsed)).starmap(calc_margin).list()
    ic(margins)
    return math.prod(margins)


# %%
calc_margin(30, 200)


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    values = seq(parsed).map(lambda ns: sjoin(map(str, ns))).map(int).list()
    ic(values)
    margins = calc_margin(*values)
    return margins


# %%
def part2(inp):
    parsed = parse(inp)
    result = process2(parsed)
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
