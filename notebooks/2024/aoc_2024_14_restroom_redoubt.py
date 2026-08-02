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
# [Advent of Code 2024 - Day 14](https://adventofcode.com/2024/day/14)

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
example

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
Robot = namedtuple("Robot","px,py,vx,vy")

def parse_data(inp):
    return seq(string_to_integers_list(inp)).smap(Robot).list()


# %% [markdown]
# # Process

# %%
def mod_c(c, x, y):
    return c.real % x + (c.imag % y) * 1j

def process(parsed, W, H, seconds=100):
    #ics(parsed)
    #positions = seq(parsed).map(l)
    positions = [r.px + r.py * 1j for r in parsed]
    velocities = [r.vx + r.vy * 1j for r in parsed]
    new_positions = [mod_c(p + v * seconds, W, H) for p, v in zip(positions, velocities)]
    points = sorted(map(complex_to_tuple, new_positions))
    #xs, ys = xs_and_ys(coords)
    #print_lines("robots", get_vis_map_multiline_str([], [], special_chars=[("*", x, y) for x, y in points]))
    
    hx, hy = W//2, H//2
    #ics(hx, hy)
    left, right = seq(new_positions).where(lambda c: c.imag != hy and c.real != hx).partition(lambda c: c.real < hy)
    ics(left, right)
    vert_split = lambda c: c.imag < hy
    top_left, bot_left = left.partition(vert_split)
    top_right, bot_right = right.partition(vert_split)
    #ics(top_left, bot_left, top_right, bot_right)

    lengths = maplist(len, [top_left.list(), bot_left.list(), top_right.list(), bot_right.list()])
    #ics(lengths)
    return math.prod(lengths)


# %%
mod_c(2+3j, 2, 2)
mod_c(2+4j + (2-3j) * 5, 11, 7)


# %%
def part1(inp, W, H):
    parsed = parse_data(inp)
    result = process(parsed, W, H)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed, W, H):
    positions = [r.px + r.py * 1j for r in parsed]
    velocities = [r.vx + r.vy * 1j for r in parsed]
    robot_cnt = len(positions)

    for seconds in range(1, 10000):
        new_positions = [mod_c(p + v * seconds, W, H) for p, v in zip(positions, velocities)]

        if len(set(new_positions)) == robot_cnt:
            print(f"Seconds: {seconds}")
            points = map(complex_to_tuple, new_positions)
            print_lines("robots", get_vis_map_multiline_str([], [], min_val=0, max_val=102, blank_char =" ", special_chars=[(graph_char_circle_cross, x, y) for x, y in points]))
            
    return None


# %%
def part2(inp, W, H):
    parsed = parse_data(inp)
    result = process2(parsed, W, H)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

for sample_data1 in sample_data1s:
    part1(sample_data1, 11, 7)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp, 101, 103)
part2(real_inp, 101, 103)

# %% [markdown]
# # Animation frame render function

# %%
parsed = parse_data(get_aocd_data())
positions = [r.px + r.py * 1j for r in parsed]
velocities = [r.vx + r.vy * 1j for r in parsed]
combined = list(zip(positions, velocities))
W, H = 101, 103

def plotstate(canvas, step):
    #print(f"plotstate(canvas, {step})")
    new_positions = [mod_c(p + v * step, W, H) for p, v in combined]
    points = map(complex_to_tuple, new_positions)
    lines = ["Step " + str(step)] + get_vis_map_multiline_str([], [], min_val=0, max_val=102, blank_char =" ", special_chars=[(graph_char_circle_cross, x, y) for x, y in points]).split("\n")

    with hold_canvas():
        canvas.clear()  # Clear the old animation step

        for n, t in enumerate(lines):
            canvas.fill_text(t, 0, 15 + 15 * n)


# %% [markdown]
# # Animation display

# %%
if is_notebook():
    from ipycanvas import Canvas, hold_canvas
    import utils.aoc_vis as aoc_vis
    print("test")
    canvas = Canvas(width=1000, height=1000)
    canvas.font = "12px monospace"
    canvas.fill_style = "green"
    
    aoc_vis.canvas_animation(canvas, 1000, plotstate)
    print("test2")
