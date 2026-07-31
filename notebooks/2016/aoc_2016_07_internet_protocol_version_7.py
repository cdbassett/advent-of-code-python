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
# * https://adventofcode.com/2016/day/7
#
# ## \--- Day 7: Internet Protocol Version 7 ---
#
# While snooping around the local network of EBHQ, you compile a list of [IP addresses](https://en.wikipedia.org/wiki/IP_address) (they're IPv7, of course; [IPv6](https://en.wikipedia.org/wiki/IPv6) is much too limited). You'd like to figure out which IPs support _TLS_ (transport-layer snooping).
#
# An IP supports TLS if it has an Autonomous Bridge Bypass Annotation, or _ABBA_. An ABBA is any four-character sequence which consists of a pair of two different characters followed by the reverse of that pair, such as `xyyx` or `abba`. However, the IP also must not have an ABBA within any hypernet sequences, which are contained by _square brackets_.
#
# For example:
#
# -   `abba[mnop]qrst` supports TLS (`abba` outside square brackets).
# -   `abcd[bddb]xyyx` does _not_ support TLS (`bddb` is within square brackets, even though `xyyx` is outside square brackets).
# -   `aaaa[qwer]tyui` does _not_ support TLS (`aaaa` is invalid; the interior characters must be different).
# -   `ioxxoj[asdfgh]zxcvbn` supports TLS (`oxxo` is outside square brackets, even though it's within a larger string).
#
# _How many IPs_ in your puzzle input support TLS?
#

# %%
from collections import *

from icecream import ic
from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
from iter_utils import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


# %%
def parse(inp):
    return inp.strip().split("\n")


# %%
def contains_abba(s):
    for a, b, c, d in seq(list(s)).sliding(4):
        if a == d and b == c and a != b:
            return True

    return False


# %%
def split_pieces(line):
    allpieces = seq(line.split("[")).map(lambda s: s.split("]")).flatten().to_list()
    outerpieces = allpieces[0::2]
    innerpieces = allpieces[1::2]
    #ic(outerpieces, innerpieces)
    #ic(line, allpieces)
    return outerpieces, innerpieces



# %%
def valid_TLS(line):
    outerpieces, innerpieces = split_pieces(line)
    return seq(outerpieces).exists(contains_abba) and not seq(innerpieces).exists(contains_abba)


# %%
def part1(inp):
    data = parse(inp)
    result = seq(data).count(valid_TLS)
    print_result(result)


# %%
def get_abas(pieces):
    for s in pieces:
        for a, b, c in seq(list(s)).sliding(3):
            if a == c and a != b:
                yield "".join((a, b, c))


# %%
set(get_abas("aba[bab]xyz"))


# %%
def valid_SSL(line):
    outerpieces, innerpieces = split_pieces(line)
    ics(outerpieces, innerpieces)
    outer_abas = set(get_abas(outerpieces))
    inner_abas = seq(get_abas(innerpieces)).map(lambda s: "".join((s[1], s[0], s[1]))).set()
    #inner_abas = seq(innerpieces).map(get_abas).to_set()
    ics(line, outer_abas, inner_abas)
    return outer_abas & inner_abas


# %%
def part2(inp):
    data = parse(inp)
    result = seq(data).count(valid_SSL)
    print_result(result)


# %%
insert_sample_functions(False, globals())
print_preface_notebook()
samp_inp1 = """
abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn
vjqhodfzrrqjshbhx[lezezbbswydnjnz]ejcflwytgzvyigz[hjdilpgdyzfkloa]mxtkrysovvotkuyekba
"""
part1(samp_inp1)
samp_inp2 = """
aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb
"""
part2(samp_inp2)

#for line in samp_inps.strip().split("\n"):
#    ic(line, valid_line(line))

# %%
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
print_preface_notebook()
part1(real_inp)
part2(real_inp)

# %%
data = real_inp.strip().split("\n")
for line in data:
    c = Counter(line)
    assert c["["] == c["]"] >= 1

# %%
