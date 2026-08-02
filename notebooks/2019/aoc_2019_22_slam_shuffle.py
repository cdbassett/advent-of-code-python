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
# [Advent of Code 2019 - Day 22](https://adventofcode.com/2019/day/22)

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
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module

# %% [markdown]
# # Sample Data

# %%
sample_data1s = [
"""
deal with increment 7
deal into new stack
deal into new stack""",
"""
cut 6
deal with increment 7
deal into new stack""",
"""
deal with increment 7
deal with increment 9
cut -2""",
"""
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1"""]
sample_data1s = maplist(str.strip, sample_data1s)
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
    lines = inp.strip().split("\n")
    return seq(lines).map(itemgetter(0)).zip(seq(lines).map(string_to_integers_list).map(first_element)).list()
#string_to_integers_list("Asdasdas 7\n6\nsgdfn8")


# %% [markdown]
# # Process

# %%
def shuffle(parsed, deck):
    cards_cnt = len(deck)

    for s, n in parsed:
        if s == "d":
            if n is None:
                deck.reverse()
            else:
                new_deck = [None] * cards_cnt
                i = 0

                for card in deck:
                    new_deck[i] = card
                    i = (i + n) % cards_cnt

                deck = deque(new_deck)
        elif s == "c":
            deck.rotate(-n)
        else:
            raise Exception("unexpected value!")

    return deck

def shuffle2(parsed, cards_cnt, card_pos):
    for s, n in parsed:
        if s == "d":
            if n is None:
                card_pos = cards_cnt - card_pos - 1
            else:
                card_pos = (n * card_pos) % cards_cnt
        elif s == "c":
            card_pos = (card_pos - n) % cards_cnt
        else:
            raise Exception("unexpected value!")

    return card_pos

def shuffle3(parsed, cards_cnt, card_pos):
    # card x ends up at position A * x + B after one complete shuffle    
    ics(cards_cnt, card_pos)
    a, b = 1, 0

    for s, num in parsed:
        if s == "d":
            if num is None:
                la, lb = -1, -1
            else:
                la, lb = num, 0
        elif s == "c":
            la, lb = 1, -num
        else:
            raise Exception("unexpected value!")
        # la * (a * x + b) + lb == la * a * x + la*b + lb
        # The `% n` doesn't change the result, but keeps the numbers small.
        a = (la * a) % cards_cnt
        b = (la * b + lb) % cards_cnt

    card_pos = (a * card_pos + b) % cards_cnt
    return card_pos

"""
the following statements are equivalent:
    A equiv B (mod C)
    A mod C = B mod C
    A = B + K * C (where K is some integer)

(A + B) mod C = (A mod C + B mod C) mod C
(A * B) mod C = (A mod C * B mod C) mod C
A^B mod C = ( (A mod C)^B ) mod C

The modular inverse of A (mod C) is A^-1. The modular inverse of A mod C is the B value that makes A * B mod C = 1
    (A * A^-1) ≡ 1 (mod C) or equivalently (A * A^-1) mod C = 1
    Only the numbers coprime to C (numbers that share no prime factors with C) have a modular inverse (mod C)
math.gcd(*integers) returns the greatest common divisor of the specified integer arguments
A = R + B * Q (where B is some integer)
If A = B⋅Q + R and B≠0 then GCD(A,B) = GCD(B,R) where Q is an integer, R is an integer between 0 and B-1

Fermat's little theorem states that if p is a prime number, then for any integer a, the number ap − a is an integer multiple of p.
"""

def process(parsed, cards_cnt = 10007, track_card = 2019):
    ics(parsed)
    card_pos = track_card
    if 1:
        card_pos = shuffle3(parsed, cards_cnt, card_pos)
        res = card_pos
        ics(res)
    else:
        deck = shuffle(parsed, deque(range(cards_cnt)))
        res = deck.index(card_pos)
        ics(deck)

    if not is_sample:
        return res


# %%
def part1(inp, cards_cnt = 10007, track_card = 2019):
    parsed = parse_data(inp)
    result = process(parsed, cards_cnt, track_card)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def generator(parsed):
    card_pos = 2020

    for step in range(101741582076661):
        card_pos = shuffle2(parsed, 119315717514047, card_pos)
        yield card_pos

def process2(parsed):
    assert not is_sample

    card_pos = predict(generator(parsed), 119315717514047)

    if 0:
        card_pos = 2020

        for step in range(101741582076661):
            card_pos = shuffle2(parsed, 119315717514047, card_pos)

    return card_pos


# %%
def part2(inp):
    return
    parsed = parse_data(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

for sample_data1 in sample_data1s:
    part1(sample_data1, 10, 5)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)
