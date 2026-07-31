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

import numpy as np
from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from iter_utils import *
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
Instruction = namedtuple("Instruction","dir,cnt,color")

def parse_line(line):
    return line.split()

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).multimap(identity, int).starmap(Instruction).list()


# %% [markdown]
# # Process

# %%
def PolyArea(x,y):
    return np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1))) // 2

# https://en.wikipedia.org/wiki/Polygon#Area_and_centroid

def poly_area(points):
    area = 0
    N = len(points)

    for i in range(N):
        area += (points[i].x * points[(i+1) % N].y - points[(i+1) % N].x * points[i].y)//2;

    return area

def process(parsed):
    #ics(parsed)
    pos = 0, 0
    corners = [Point2D(*pos)]
    corner = pos
    boundary = 0

    for inst in parsed:
        adjust = vertical_movements[inst.dir]
        boundary += inst.cnt
        corner = add_tuple(corner, multiply_scalar_tuple(adjust, inst.cnt))

        # if on right or lower edge, need to add 1
        corners.append(Point2D(*corner))

    #print(get_vis_map_multiline_str(*zip(*points)))
    corners = corners[:-1]
    xs = np.array([p.x for p in corners], dtype=np.int_)
    ys = np.array([p.y for p in corners], dtype=np.int_)

#    if is_sample:
#        ic((np.max(xs) - np.min(xs) + 1) * (np.max(ys) - np.min(ys) + 1))

    if 0:
        area = poly_area(corners)
    else:
        #area = PolyArea(xs, ys)
        area = polygon_area(xs, ys)

    ic(len(corners), len(parsed))
    ic(area)
    return round(picks_theorem(area, boundary)) # picks theorem https://en.wikipedia.org/wiki/Pick%27s_theorem


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %%
lookup = dict((str(n), c) for n, c in enumerate("RDLU"))
ic(lookup)

def convert(line):
    hex = line.color[2:-1]
    return Instruction(lookup[hex[-1]],int(hex[:-1],16),0)

def part2(inp):
    parsed = parse(inp)

    # convert parsed
    new_parsed = [convert(line) for line in parsed]
    result = process(new_parsed)
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
print_preface_notebook()
part1(sample_data1)
part2(sample_data2)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
print_preface_notebook()
#print(real_inp)
part1(real_inp)
part2(real_inp)
