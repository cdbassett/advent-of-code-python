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
sample_data1 = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
sample_data2 = sample_data1

# %% [markdown]
# # Parse

# %%
hand = namedtuple("hand","cards,bid")

def parse_line(line):
    p = line.split()
    return hand(p[0], int(p[1]))

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
suit = "A,K,Q,J,T,9,8,7,6,5,4,3,2".split(",")
#rank_by_face = seq(suit).reverse().zip_with_index().dict()
rank_by_face = seq(suit).zip_with_index().dict()
five_of_a_kind, four_of_a_kind, full_house, three_of_a_kind, two_pair, two_of_a_kind, one_of_a_kind = range(1,8)

def hand_type(hand):
    counts = Counter(hand)
    matches = counts.most_common(2)
    #ics(hand, matches)

    match matches:
        case [(face, 5)]:
            return 1
        case [(face, 4), _]:
            return 2
        case [(face1, 3), (face2,2)]:
            return 3
        case [(face, 3), _]:
            return 4
        case [(face1, 2), (face2, 2)]:
            return 5
        case [(face, 2), _]:
            return 6
        case _:
            return 7

def hand_order(hand):
    return [hand_type(hand.cards)] + seq(list(hand.cards)).map(rank_by_face.get).list()

def process(parsed):
    ics(parsed)
    types = seq(parsed).map(itemgetter(0)).map(hand_type).zip(parsed).list()
    #ics(types)
    ordered = seq(parsed).order_by(hand_order).reverse().enumerate(1).list()
    #ics(ordered)
    return seq(ordered).starmap(lambda rank, hand: rank * hand.bid).sum()


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
suit2 = "A,K,Q,T,9,8,7,6,5,4,3,2,J".split(",")
rank_by_face2 = seq(suit2).zip_with_index().dict()
#    five_of_a_kind, four_of_a_kind, full_house, three_of_a_kind, two_pair, two_of_a_kind, one_of_a_kind = range(1,8)

def hand_type2(hand):
    counts = Counter(hand)
    # TODO! order cards by highest value first!
    matches = counts.most_common(2)
    j_count = counts.get("J", 0)
    ics(hand, j_count, matches)

    match matches:
        case [(face, 5)]:
            return five_of_a_kind
        case [(face, 4), _]:
            return [four_of_a_kind, five_of_a_kind, -1, -1, five_of_a_kind][j_count]
        case [(face1, 3), (face2, 2)]:
            return [full_house, -1, five_of_a_kind, five_of_a_kind][j_count] # can't have only one joker, woudln't match
        case [(face, 3), _]:
            return [three_of_a_kind, four_of_a_kind, five_of_a_kind, four_of_a_kind][j_count]
        case [(face1, 2), (face2, 2)]:
            return [two_pair, full_house, four_of_a_kind][j_count] # 1 is full house, 2 is 4 of a kind
        case [(face, 2), _]:
            return [two_of_a_kind, three_of_a_kind, three_of_a_kind][j_count]
        case _:
            return [one_of_a_kind, two_of_a_kind][j_count] # should never have more than one joker bc it woudl trigger earlier match

def hand_order2(hand):
    #ics(hand.cards, seq(list(hand.cards)).map(rank_by_face2.get).list())
    return [hand_type2(hand.cards)] + seq(list(hand.cards)).map(rank_by_face2.get).list()

def process2(parsed):
    ics(parsed)
    types = seq(parsed).map(itemgetter(0)).map(hand_type2).zip(parsed).list()
    ics(types)
    ordered = seq(parsed).order_by(hand_order2).reverse().enumerate(1).list()
    ics(ordered)
    return seq(ordered).starmap(lambda rank, hand: rank * hand.bid).sum()

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
# 249400220
