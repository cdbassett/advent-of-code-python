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
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from iter_utils import *
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

# %% [markdown]
# # Others' solutions

# %% [markdown]
# In the end my solution combines the input instructions into a pair of integers A and B, where card x ends up at position A * x + B after one complete shuffle. To get A and B after n shuffles, it uses the formula x’ = A’ x + B’ = An * x + B * (An - 1) / (A - 1). Finally it rearranges the equation to x = (x’ - B’) / A’ and plugs in the known values for x’, A’ and B’ to get the answer. Oh and I used repeated squaring to calculate An, of course.

# %%
# https://topaz.github.io/paste/#XQAAAQAgBQAAAAAAAAAzHIoib6pENkSmUIKIED8dy140D1lKWSMhNhZz+hjKgIgfJKPuwdqIBP14lxcYH/qI+6TyUGZUnsGhS4MQYaEtf9B1X3qIIO2JSejFjoJr8N1aCyeeRSnm53tWsBtER8F61O2YFrnp7zwG7y303D8WR4V0eGFqtDhF/vcF1cQdZLdxi/WhfyXZuWC+hs8WQCBmEtuId6/G0PeMA1Fr78xXt96Um/CIiLCievFE2XuRMAcBDB5We73jvDO95Cjg0CF2xgF4yt3v4RB9hmxa+gmt6t7wRI4vUIGoD8kX2k65BtmhZ7zSZk1Hh5p1obGZ6nuuFIHS7FpuSuv1faQW/FuXlcVmhJipxi37mvPNnroYrDM3PFeMw/2THdpUwlNQj0EDsslC7eSncZQPVBhPAHfYojh/LlqSf4DrfsM926hSS9Fdjarb9xBYjByQpAxLDcmDCMRFH5hkmLYTYDVguXbOCHcY+TFbl+G/37emZRFh/d+SkeGqbFSf64HJToM2I7N2zMrWP7NDDY5FWehD5gzKsJpEg34+sG7x2O82wO39qBlYHcYg1Gz4cLBrH1K1P+KWvEdcdj/NBtrl6yftMlCu6pH4WTGUe9oidaiRuQZOGtw71QsTQUuhpdoWO4mEH0U9+CiPZCZLaQolFDSky1J9nDhZZHy3+ETcUeDOfSu+HI3WuKC0AtIRPdG8B9GhtxZQKAx+5kyi/ek7A2JAY9SjrTuvRADxx5AikbHWXIsegZQkupAc2msammSkwY8dRMk0ilf5vh6kR0jHNbSi0g0KJLCJfqggeX24fKk5Mdh8ULZXnMfMZOmwEGfegByYbu91faLijfW4hoXCB1nlsWTPZEw2PCZqqhl9oc1q25H2YkkvKLxEZWl6a9eFuRzxhB840I1zdBjUVgfKd9/V4VdodzU2Z2e+VEh7RbJjQNFC/rG8dg==
# did not give correct answer

real_inp = get_aocd_data()
n = 119315717514047
c = 2020

a, b = 1, 0
for l in real_inp.split("\n"):
    if l == 'deal into new stack\n':
        la, lb = -1, -1
    elif l.startswith('deal with increment '):
        la, lb = int(l[len('deal with increment '):]), 0
    elif l.startswith('cut '):
        la, lb = 1, -int(l[len('cut '):])
    # la * (a * x + b) + lb == la * a * x + la*b + lb
    # The `% n` doesn't change the result, but keeps the numbers small.
    a = (la * a) % n
    b = (la * b + lb) % n

M = 101741582076661
# Now want to morally run:
# la, lb = a, b
# a = 1, b = 0
# for i in range(M):
#     a, b = (a * la) % n, (la * b + lb) % n

# For a, this is same as computing (a ** M) % n, which is in the computable
# realm with fast exponentiation.
# For b, this is same as computing ... + a**2 * b + a*b + b
# == b * (a**(M-1) + a**(M) + ... + a + 1) == b * (a**M - 1)/(a-1)
# That's again computable, but we need the inverse of a-1 mod n.

# Fermat's little theorem gives a simple inv:
# Fermat's little theorem states that if p is a prime number, then for any integer a, the number ap − a is an integer multiple of p.
def inv(a, n): return pow(a, n-2, n)

Ma = pow(a, M, n)
Mb = (b * (Ma - 1) * inv(a-1, n)) % n

# This computes "where does 2020 end up", but I want "what is at 2020".
#print((Ma * c + Mb) % n)

# So need to invert (2020 - MB) * inv(Ma)
print(((c - Mb) * inv(Ma, n)) % n)
#102042899980172 is too high

# %%
# https://github.com/metalim/adventofcode.2019.python/blob/master/22_cards_shuffle.ipynb
# gave correct answer
# convert rules to linear polynomial.
# (g∘f)(x) = g(f(x))
def parse(L, rules):
    a,b = 1,0
    for s in rules[::-1]:
        if s == 'deal into new stack':
            a = -a
            b = L-b-1
            continue
        if s.startswith('cut'):
            n = int(s.split(' ')[1])
            b = (b+n)%L
            continue
        if s.startswith('deal with increment'):
            n = int(s.split(' ')[3])
            z = pow(n,L-2,L) # == modinv(n,L)
            a = a*z % L
            b = b*z % L
            continue
        raise Exception('unknown rule', s)
    return a,b

# modpow the polynomial: (ax+b)^m % n
# f(x) = ax+b
# g(x) = cx+d
# f^2(x) = a(ax+b)+b = aax + ab+b
# f(g(x)) = a(cx+d)+b = acx + ad+b
def polypow(a,b,m,n):
    if m==0:
        return 1,0
    if m%2==0:
        return polypow(a*a%n, (a*b+b)%n, m//2, n)
    else:
        c,d = polypow(a,b,m-1,n)
        return a*c%n, (a*d+b)%n

def shuffle2(L, N, pos, rules):
    a,b = parse(L,rules)
    a,b = polypow(a,b,N,L)
    return (pos*a+b)%L

L = 119315717514047
N = 101741582076661
rules = get_aocd_data().split("\n")
shuffle2(L,N,2020,rules)
