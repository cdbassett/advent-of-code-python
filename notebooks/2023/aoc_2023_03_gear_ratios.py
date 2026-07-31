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

# %%
# %load_ext autoreload

# %%
from collections import *
import re
import math

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module

# %%
sample_data1 = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
sample_data1 = """
12.......*..
+.........34
.......-12..
..78........
..*....60...
78..........
.......23...
....90*12...
............
2.2......12.
.*.........*
1.1.......56
"""
sample_data2 = sample_data1


# %%
def parse_line(line):
    return line

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()
    #return [parse_line(line) for line in inp.strip().split("\n")]


# %% [markdown]
# # Process

# %%
reIntegers = re.compile(r"\d+")

def number_positions(y, line):
    return [(m.start(), y, m.group()) for m in reIntegers.finditer(line, 0)]

def neighbors(x, y):
    return product(range(x-1, x+2), range(y-1, y+2))

def char_positions(parsed):
    return seq(product(range(width(parsed)), range(height(parsed)))).starmap(lambda x, y: (x, y, parsed[y][x]))

def symbol_positions(parsed):
    chars = char_positions(parsed)
    return chars.starfilter(lambda x, y, c: not c.isdigit() and c != ".").map(lambda t: t[:2])

def process(parsed):
    #ics(parsed)
    numbers = seq(enumerate(parsed)).starmap(number_positions).flatten()
    ics(numbers)
    sym_pos = symbol_positions(parsed)
    ics(sym_pos)
    sym_neighbors = sym_pos.starmap(neighbors).flatten().set()
    #ics(sym_neighbors)
    return numbers.starfilter(lambda x, y, number: (x, y) in sym_neighbors or (x + len(number) - 1, y) in sym_neighbors).map(lambda e: int(e[2])).sum()


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def star_positions(parsed):
    chars = char_positions(parsed)
    #return chars.filter(lambda e: e[2] == "*").map(lambda t: t[:2])
    return chars.starfilter(lambda x, y, c: c == "*").map(lambda t: t[:2]).list()

    # each element is a the two and only two numbers adjacent to a *
def gear_numbers(numbers, star_pos):
    if 1:
        #ics(numbers)
        pos_of_numbers = numbers.starmap(lambda x, y, number: ((x,y), (int(number),x,y))) \
            .concat(numbers.starmap(lambda x, y, number: ((x+len(number)-1, y), (int(number),x,y)))) \
            .dict()
        #ics(numbers)
    elif 1:
        ics(numbers)
        pos_of_numbers = numbers.starmap(lambda x, y, number: ((x,y), (int(number),x,y))).dict()
        ics(numbers)
        pos_of_numbers.update(numbers.starmap(lambda x, y, number: ((x+len(number)-1, y), (int(number),x,y))))
    else:
        pos_of_numbers = {}

        for x, y, number in numbers:
            num = int(number)

            for n in range(len(number)):
                pos_of_numbers[(x+n,y)] = num

    ics(pos_of_numbers)
        # each element is a set of all numbers adjacent to the star
    numbers_for_gears = seq(star_pos).map(lambda e: set(num for pos in neighbors(*e[:2]) if (num := pos_of_numbers.get(pos)) is not None))
    ics(numbers_for_gears)
    return numbers_for_gears.filter(lambda e: len(e) == 2).map(lambda e: [a[0] for a in e]).map(tuple).list()

def process2(parsed):
    numbers = seq(enumerate(parsed)).starmap(number_positions).flatten().build() # build creates new sequence based on list of sequence so far
    #ics(numbers._lineage)
    star_pos = star_positions(parsed)
    ics(star_pos)
    gear_nums = gear_numbers(numbers, star_pos)
    ics(gear_nums)
    #ic(gear_nums)
    return seq(gear_nums).map(math.prod).sum()


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
# Part 1: 413
# Part 2: 6756

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp) # 527369
part2(real_inp) # 73074886
# 72114486 is too low

# %%
