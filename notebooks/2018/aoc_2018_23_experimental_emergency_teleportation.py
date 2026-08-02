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
# [Advent of Code 2018 - Day 23](https://adventofcode.com/2018/day/23)

# %% editable=false jupyter={"source_hidden": true}
from utils.aoc_utils import *
if is_notebook():
    print(get_aoc_url())

# %% [markdown]
# # Imports

# %%
# %load_ext autoreload

# %%
import sys
from collections import *
import re

import numpy as np
from scipy import spatial
from icecream import ic
import z3
from z3 import Int, Optimize, If, Real, Solver, Or, And

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
sample_data2 = \
"""pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5"""

# %% [markdown]
# # Parse

# %%
Robot = namedtuple("Robot","pos,radius")

def parse_line(line):
    return Robot(tuple(line[:3]), line[-1])

def parse_data(inp):
    return seq(inp.strip().split("\n")).map(string_to_integers_list).map(parse_line).list()


# %%
# oops... this finds the nanobot in range of the most, not the coordinate
def process2old(parsed):
    #ics(parsed)
    points = np.array(seq(parsed).map(lambda r: r.pos).list())
    radii = np.array(seq(parsed).map(lambda r: r.radius).list())
    #ics(radii)
    tree = spatial.KDTree(points)
    res = tree.query_ball_point(points, radii, p=1) # p=1 means manhattan
    ics(res)
    res_with_extra = [[-len(el), manhattan(parsed[n].pos)] + el for n, el in enumerate(res)]
    #results = sorted(res, key=len, reversed=True)
    results = sorted(res_with_extra)
    max_length = results[0][0]
    ics(results, max_length)
    return None


# %%
def to_cuboid(robot):
    p = robot.pos
    r = robot.radius
    return tuple((t-r, t+r) for t in p)

# big mistake: area in range of nanorobots is not a cuboids, it's a rough sphere
# with manhattan distance instead of euclidean
def process2old2(parsed):
    ics(parsed)
    points = np.array(seq(parsed).map(lambda r: r.pos).list())
    radii = np.array(seq(parsed).map(lambda r: r.radius).list())
    cuboids = seq(parsed).map(to_cuboid).list()
    ics(cuboids)
    intersections = [[cuboids[0], set([cuboids[0]])]]

    for cuboid in cuboids[1:]:
        found = False

        for one in intersections:
            #ics(cuboid, one)
            intersection = cubes_intersection(cuboid, one[0])

            if intersection:
                one[1].add(cuboid)
                one[0] = intersection
                found = True
                #break

        if not found:
            intersections.append([cuboid, set([cuboid])])

    # one more pass for ealier cuboids that may have missed intersecting with later intersections
    for cuboid in cuboids[1:]:
        for one in intersections:
            #ics(cuboid, one)
            intersection = cubes_intersection(cuboid, one[0])

            if intersection:
                one[1].add(cuboid)
                one[0] = intersection


    if 0:
        for one in intersections:
            if any(cubes_intersection(one[0], other[0]) for other in intersections if one != other):
            #if any(cubes_intersection(one[0], other[0]) for other in intersections):
                print("found additional intersections")

    ics(intersections)
    ic(len(intersections))
    ic(maplist(itemgetter(0), intersections))
    ic(seq(intersections).map(itemgetter(1)).map(len))
    primary_cuboid = seq(intersections).max_by(lambda e: len(e[1]))[0]
    ic(primary_cuboid)
    ic(seq(intersections).map(itemgetter(0)).level2_map(itemgetter(0)).map(list))
    ic(seq(intersections).map(itemgetter(0)).level2_map(itemgetter(0)).map(list).map(manhattan))
    # assuming positive
    p = maplist(itemgetter(0), primary_cuboid)
    ic(p)
    return sum(p)


# %% [markdown]
# # Process

# %%
def process(parsed):
    ic(len(parsed))
    #ics(parsed)
    strongest = seq(parsed).max_by(lambda r: r.radius)
    return seq(parsed).count(lambda r: manhattan(r.pos, strongest.pos) <= strongest.radius)


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    #ics(parsed[0])
    #ics(list(product(parsed[0].pos)))
    print_result(result)


# %% [markdown]
# # Process2

# %%
x = Real('x')
y = Real('y')
s = Solver()
s.add(x > 1, y > 1, Or(x + y > 3, x - y < 2))
print ("asserted constraints...")
for c in s.assertions():
    print (c)

print (s.check())
print ("statistics for the last check method...")
print (s.statistics())
# Traversing statistics
for k, v in s.statistics():
    print ("%s : %s" % (k, v))


# %%
def process2(parsed):
    def z3_abs(x):
        return If(x >= 0,x,-x)

    def z3_dist(a, b):
        return z3_abs(a[0] - b[0]) + z3_abs(a[1] - b[1]) + z3_abs(a[2] - b[2])

    x, y, z = (Int(c) for c in "xyz")
    opt = Optimize()
    origin = 0,0,0
    position = x, y, z
    bot_vars = [Int("b"+str(n)) for n, bot in enumerate(parsed)]
    bot_constraints = [ ]
    in_range_cnt = Int("in_range_cnt")

    for bot, bot_var in zip(parsed, bot_vars):
        opt.add(bot_var == If(z3_dist(bot.pos, position) <= bot.radius, 1, 0))

    dist_from_origin = Int("dist")
    opt.add(dist_from_origin == z3_dist(origin, position))
    opt.add(in_range_cnt == sum(bot_vars))
    opt.maximize(in_range_cnt)
    d = opt.minimize(dist_from_origin)

    ics(opt.check())
    ics(opt.lower(d))
    model = opt.model()
    #ics(model)
    ics(model[dist_from_origin])
    ics(model[in_range_cnt])
    return model[dist_from_origin].as_long()


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
part2(real_inp) # 99832660 is too low 112997634

