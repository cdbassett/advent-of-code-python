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

# %% [markdown]
# [Advent of Code 2018 - Day 3](https://adventofcode.com/2018/day/3)

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
sample_data2 = sample_data1

# %%
for sample in sample_data1s:
    print(sample)
    print("=======================")

# %% [markdown]
# # Parse

# %%
Claim = namedtuple("Claim","id,x,y,w,h")

def parse(inp):
    return seq(inp.strip().split("\n")).map(string_to_integers_list).starmap(Claim).list()


# %% [markdown]
# # Process

# %%
def rangex(x, w):
    return range(x, x + w)

def get_counts(parsed):
    cnts = Counter()

    for claim in parsed:
        cnts.update(product(rangex(claim.x, claim.w), rangex(claim.y, claim.h)))

    ic(len(cnts))
    #ics(cnts)
    return cnts

def process(parsed):
    ics(parsed)
    ic(len(parsed))
    cnts = get_counts(parsed)
    return sum(1 for v in cnts.values() if v > 1)


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    collides = set()

    if 0:
        for n, claim1 in enumerate(parsed):
            if not any(rects_intersect(claim1, claim2) for claim2 in parsed[n+1:]):
                return claim1.id
    #return

    for claim1, claim2 in combinations(parsed, 2):
        if rects_intersect(claim1, claim2):
            collides.update((claim1, claim2))

    return first_element(claim for claim in parsed if claim not in collides).id
    cnts = get_counts(parsed)

    cp = seq(cnts.items()).where(lambda i: i[1] == 1).head()[0]
    ic(seq(cnts.items()).count(lambda i: i[1] == 1))
    return seq(parsed).where(lambda claim: claim.x <= cp[0] < claim.x + claim.w and claim.y <= cp[1] < claim.y + claim.h).one().id


# %%
def part2(inp):
    parsed = parse(inp)
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
part2(real_inp)
