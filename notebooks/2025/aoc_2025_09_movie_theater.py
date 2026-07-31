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
import os
import sys
from collections import *
import re
import math

from icecream import ic
import iteration_utilities as it_ut

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module

from shapely.geometry import Point, Polygon, box

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
def parse_data(inp):
    return maplist(tuple, string_to_integers_list(inp))


# %% [markdown]
# # Process

# %%
use_shapely = False

if use_shapely:
    def area2(poly):
        minx, miny, maxx, maxy = poly.bounds
        return (maxx-minx+1) * (maxy-miny+1)
        return poly.area
    def area3(p1, p2):
        return (abs(p1.x-p2.x)+1) * (abs(p1.y-p2.y)+1)
        
    def make_poly_from_points(p1, p2):
        minx = min(p1.x, p2.x)
        miny = min(p1.y, p2.y)
        maxx = max(p1.x, p2.x)
        maxy = max(p1.y, p2.y)
        # Create the rectangular polygon using box()
        return box(minx, miny, maxx, maxy)    
else:        
    def area(p1, p2):
        return (abs(p1[0]-p2[0])+1) * (abs(p1[1]-p2[1])+1)

def process(parsed):
    #ics(parsed)
    if use_shapely:
        points = seq(parsed).starmap(Point).list()
        return seq(combinations(points, 2)).starmap(make_poly_from_points).map(area2).max()
        
    return seq(combinations(parsed, 2)).starmap(area).max()


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def line_points(p1, p2):
    x, y = p1
    
    if x == p2[0]:
        b, e = sorted((y, p2[1]))
        line = [(x, y) for y in range(b, e+1)]
    else:
        b, e = sorted((x, p2[0]))
        line = [(x, y) for x in range(b, e+1)]

    #ics(p1, p2, line)
    return line

def process2(parsed):
    if use_shapely:
        polygon = Polygon(parsed)
        ics(polygon)
        points = seq(parsed).starmap(Point).list()
        
        def inside_poly(p):
            return polygon.contains(p)

        return seq(combinations(points, 2)).starmap(make_poly_from_points).filter(inside_poly).map(area2).max()

    @cache
    def inside_poly2(p):
        if p in colored:
            return True

        y = p[1]
        crosses = 0
        last_crossed = None
        last_x = None
        
        for x in range(p[0], max_x + 1):
            if (x, y) in colored:
                if last_crossed != last_x:
                    crosses += 1
                last_crossed = x
            last_x = x

        if not (0 <= crosses <= 2):
            ics(p, x, y, last_x, last_crossed)
            
        assert 0 <= crosses <= 2, f"invalid crosses {crosses} for point {p}"
        return crosses == 1


    def inside_poly(p1, p2):
        #ics("inside_poly")
        minx = min(p1[0], p2[0])
        miny = min(p1[1], p2[1])
        maxx = max(p1[0], p2[0])
        maxy = max(p1[1], p2[1])
        return all(inside_poly2(p) for p in product(range(minx, maxx+1), range(miny,maxy+1)))
    
    ics(parsed)
    colored = set()
    
    for p1, p2 in pairwise(parsed + parsed[0:1]):
        colored |= set(line_points(p1, p2))

    max_x = seq(parsed).map(itemgetter(0)).max()
    max_y = seq(parsed).map(itemgetter(1)).max()
    min_x = seq(parsed).map(itemgetter(0)).min()
    min_y = seq(parsed).map(itemgetter(1)).min()
    ic(min_x, max_x, min_y, max_y)                    

    #return seq(combinations(parsed, 2)).starfilter(inside_poly).starmap(area).max()


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
part2(real_inp) # 1569262188

# %% [markdown]
# # Others' solutions
