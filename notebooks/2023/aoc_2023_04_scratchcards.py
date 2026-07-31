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

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module

# %%
sample_data1 = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
sample_data2 = """
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
    line = line.split(":")[1]
    parts = line.split("|")
    return seq(parts).map(string_to_integers).map(tuple).list()

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def card_wins(card):
    return seq(card[0]).intersection(card[1]).len()

def card_score(card):
    count = card_wins(card)
    return 1 << (count-1) if count else 0

def process(parsed):
    #ics(parsed)
    scores = seq(parsed).map(card_score)
    ics(scores)
    return scores.sum()


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    @functools.cache
    def cards_won(card_no):
        ics(card_no)
        last_card = len(parsed)+1
        wins = card_wins(parsed[card_no-1])
        won_count = 1
        rng = range(card_no+1, min(last_card, card_no+wins+1))
        ics(wins, rng)

        for n_card in rng:
            won_count += cards_won(n_card)

        return won_count

    won_count = 0
    ics(len(parsed))

    for n_card in range(1, len(parsed)+1):
        won_count += cards_won(n_card)

    #ic(gear_nums)
    return won_count


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
#1211208199278692103371798080032700331973188 is too high

# %%
r = range(5)
ic(r)
ic(r)


# %%
p=seq(product(range(3),range(4))).starmap(lambda x, y: (x+1, y*2)).starfilter(lambda x, y: True).map(identity)
ic(p)
ic(p)
