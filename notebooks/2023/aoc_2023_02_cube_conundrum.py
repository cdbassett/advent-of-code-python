from operator import itemgetter
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
from Utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module

# %%
sample_data1 = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
sample_data2 = sample_data1


# %%
def parse_piece(p):
    #ics(p)
    n, color = p.split(" ")
    return color, int(n)

def parse_seg(seg):
    #ics(seg)
    return seq(seg.split(", ")).map(parse_piece).dict()

def parse_line(line):
    #ics(line)
    _, id, rest = line.split(" ", 2)
    return int(id[:-1]), seq(rest.split("; ")).map(parse_seg).list()

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()
    #return [parse_line(line) for line in inp.strip().split("\n")]


# %% [markdown]
# # Process

# %%
def process(parsed, maxes):
    #ics(parsed, maxes)

    def draw_passes(draw):
        #ic(draw)
        return all(draw.get(clr, 0) <= m for clr, m in maxes.items())

    def game_passes(game):
        id, draws = game
        #ic(draws)
        return seq(draws).for_all(draw_passes)

    passing_ids = seq(parsed).filter(game_passes).map(first_element)
    ics(passing_ids)
    return passing_ids.sum()


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed, {'blue': 14, 'green': 13, 'red': 12})
    print_result(result)


# %% [markdown]
# # Process2

# %%
colors = "red,green,blue".split(",")

def min_powers(game):
    id, draws = game
    power = defaultdict(int)

    for draw in draws:
        for clr in colors:
            power[clr] = max(power[clr], draw.get(clr, 0))
    return id, math.prod(power.values())

def process2(parsed):
    all_min_powers = seq(parsed).map(min_powers)
    ics(all_min_powers)
    return all_min_powers.map(lambda game: game[1]).sum()


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

# %%
