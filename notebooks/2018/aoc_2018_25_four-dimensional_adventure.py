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
from collections import *

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module

# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0]
sample_data2 = sample_data1


# %% [markdown]
# # Parse

# %%
def parse_data(inp):
    return maplist(tuple, string_to_integers_list(inp))


# %% [markdown]
# # Process

# %%
def process(parsed):
    ic(len(parsed))
    ics(parsed)
    H = height(parsed)
    W = width(parsed)
    ic(W, H)

    designators = cycle(string.ascii_letters)

    if 0 and is_sample:
        for p1, p2 in combinations(zip(designators, parsed), 2):
            if (ma := manhattan(p1[1], p2[1])) <= 3:
                ic(p1, p2, ma)

    in_const = {}
    constellations = []

    # intial naive approach was to iterate points and either find a constellation it fit into or create new one
    # however this led to situations where two separate constellations were created before the joining point was encountered
    # so here we start off with poitns that are connected to each other
    for p1, p2 in combinations(parsed, 2):
        if manhattan(p1, p2) <= 3:
            p1_const, p2_const = in_const.get(p1), in_const.get(p2)
            #assert p1_const == p2_const or p1_const is None or p2_const is None, f"p1 ({p1}) and p2 {p2} are in different constellations ({p1_const}, {p2_const})"

            if p1_const != p2_const and p1_const is not None and p2_const is not None:
                # merge two constellations
                constellations.remove(p1_const)
                p2_const.update(p1_const)

                for one_p in p1_const:
                    in_const[one_p] = p2_const
            else:
                constellation = p1_const or p2_const

                if not constellation:
                    constellation = set([p1, p2])
                    constellations.append(constellation)

                constellation.add(p1)
                constellation.add(p2)
                in_const[p1] = constellation
                in_const[p2] = constellation

    for line in parsed:
        if line not in in_const:
            constellation = set([line])
            constellations.append(constellation)

    ics(constellations)
    return len(constellations)


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

if 1:
    for n, sample_data1 in enumerate(sample_data1s, 1):
        print(f"Sample {n}:")
        part1(sample_data1)
        print()
else:
    part1(sample_data1s[2])

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp) # 607 is too high

# %%
