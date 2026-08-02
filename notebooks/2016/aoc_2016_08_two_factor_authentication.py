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
# [Advent of Code 2016 - Day 8](https://adventofcode.com/2016/day/8)

# %% editable=false jupyter={"source_hidden": true}
from utils.aoc_utils import *
if is_notebook():
    print(get_aoc_url())


# %%
from collections import *

import numpy as np
from icecream import ic

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

# %%
# %load_ext autoreload
# %autoreload 2

# %%
W, H = 50, 6


# %%
def parse_line(line):
    pieces = line.replace("rotate ", "").split()
    nums = string_to_integers(line)
    return (pieces[0],) + tuple(nums)


# %%
def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %%
def part1(inp):
    global frames
    data = parse(inp)
    screen = np.zeros((H, W), dtype=np.int8)
    frames = [np.copy(screen)]

    for inst, a, b in data:
        if inst == "rect":
            rct = np.ones((b, a), dtype=np.int8)
            screen[0:b, 0:a] = rct
        elif inst == "row":
            screen[a:a+1, :] = np.roll(screen[a:a+1, :], b)
        else:
            screen[:, a:a+1] = np.roll(screen[:, a:a+1], b)
        frames.append(np.copy(screen))
    result = np.count_nonzero(screen)
    print_result(result)

    if not is_sample:
        s = build_string_from_numpy_int_array(screen, " #")
        print_result(ocr_aoc_letters(s), "Part 2")
#    ics(screen)
#    print_sample(s)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
print_preface_notebook()
samp_inp1 = """
rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
"""

part1(samp_inp1)

# %% [markdown]
# # Actual data

# %%
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
print_preface_notebook()
part1(real_inp)

# %% [markdown]
# # Animation frame render function

# %%
scale = 20

def image_frame(canvas, i):
    canvas.clear()
    grid = np.zeros((H + 2, W + 2), dtype=np.int8)
    grid[1:-1, 1:-1] = frames[i]
    blue_channel = np.array(grid * 255, dtype=np.int32)
    image_data = np.stack((blue_channel, blue_channel, blue_channel), axis=2)
    image_data = image_data.repeat(scale, axis=0).repeat(scale, axis=1)
    canvas.put_image_data(image_data, 0, 0)


# %% [markdown]
# # Animation display

# %% editable=true slideshow={"slide_type": ""}
if is_notebook():
    import utils.aoc_vis as aoc_vis
    from ipycanvas import RoughCanvas, hold_canvas
    canvas = RoughCanvas(width=(W + 2) * scale, height=(H + 2) * scale)
    aoc_vis.canvas_animation(canvas, len(frames), image_frame)
