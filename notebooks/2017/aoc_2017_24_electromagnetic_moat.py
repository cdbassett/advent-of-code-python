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
def parse_line(line):
    return tuple(string_to_integers_list(line))

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def strongest(from_i, from_p, s, lvl=0):

        # if we have a domino with both sides matching what we want to join, use it first every time, there's no downside
        # and it reduces the number of branches
    duplicate = (from_p, from_p)

    if duplicate in s:
        #return sum(duplicate) + strongest(from_i + [duplicate], from_p, set_without(s, duplicate), lvl+1)
        return sum(duplicate) + strongest(from_i, from_p, set_without(s, duplicate), lvl+1)

    candidates = [i for i in s for p in i if p == from_p]
    #hdr = lvl * "    "

    if not candidates:
        #tally = sum(map(sum, from_i))
        #ics(hdr, tally, from_i, from_p)
        return 0

    #ics(hdr, from_i, from_p, s)
    #return max((sum(i) + strongest(from_i + [i], i[n-1], set_without(s, i), lvl+1) for i in candidates for n, p in enumerate(i) if p == from_p), default=0)
    return max((sum(i) + strongest(i, i[n-1], set_without(s, i), lvl+1) for i in candidates for n, p in enumerate(i) if p == from_p), default=0)

def process(parsed):
    ics(parsed)
    ic(len(parsed))
    available = set(parsed)
    assert len(parsed) == len(available)
    assert (0,0) not in available

    counts = Counter(p for i in parsed for p in i)
    #ic(counts)

    #for num in sorted(counts.keys()):

    # reduce starting set
    for num, cnt in counts.items():
        chk = (num, num)
#        if cnt == 1:
#            ic(num, chk)

        if cnt == 2 and chk in available:
            #ic(num, chk)
            available.remove(chk)
            print(f"removed {chk}")

    if 0:
        counts = Counter(p for i in available for p in i)

        for num, cnt in sorted(counts.items()):
            num_with = [i for i in available if num in i]
            ic(num, cnt, num_with)

    # anything
       # find max recursively
        # first bridge must start with 0 on non-connected end

    return max(sum(i) + strongest([i], max(i), set_without(available, i)) for i in available if min(i) == 0)


# %%
def bridges(from_i, from_p, s, lvl=0):
        # if we have a domino with both sides matching what we want to join, use it first every time, there's no downside
        # and it reduces the number of branches
    duplicate = (from_p, from_p)

    if duplicate in s:
        return [[duplicate] + b for b in (bridges(from_i, from_p, set_without(s, duplicate), lvl+1))]

    candidates = [i for i in s for p in i if p == from_p]
#    hdr = lvl * "    "

    #if 0:
    if not candidates:
        #tally = sum(map(sum, from_i))
        #ics(hdr, tally, from_i, from_p)
        return [[]]

    #ics(hdr, from_i, from_p, s)
    return [[i] + b for i in candidates for n, p in enumerate(i) if p == from_p for b in (bridges(i, i[n-1], set_without(s, i), lvl+1))]

def process_full_lists(parsed):
    ics(parsed)
    ic(len(parsed))
    available = set(parsed)
    assert len(parsed) == len(available)
    assert (0,0) not in available

    counts = Counter(p for i in parsed for p in i)
    #ic(counts)

    # reduce starting set
    for num, cnt in counts.items():
        chk = (num, num)

        if cnt == 2 and chk in available:
            #ic(num, chk)
            available.remove(chk)
            print(f"removed {chk}")

    if 0:
        counts = Counter(p for i in available for p in i)

        for num, cnt in sorted(counts.items()):
            num_with = [i for i in available if num in i]
            ic(num, cnt, num_with)

       # find max recursively
    # first bridge must start with 0 on non-connected end
    all_bridges = list([i] + b for i in available if min(i) == 0 for b in (bridges([i], max(i), set_without(available, i))))
    #ics(all_bridges)
    return all_bridges


# %%
def score(b):
    return sum(map(sum, b))

def part1(inp):
    parsed = parse(inp)
    if 0:
        result = process(parsed)
    else:
        all_bridges = process_full_lists(parsed)
        scores = seq(all_bridges).map(score).list()
        #res = seq(scores).zip(all_bridges).sorted(reverse=True).list()[:10]
        #ic(res)
        result = max(scores)
    print_result(result)


# %%
def score(b):
    return sum(map(sum, b))

def part2(inp):
    parsed = parse(inp)
    all_bridges = process_full_lists(parsed)
    scores = seq(all_bridges).map(score).list()
    lengths = seq(all_bridges).map(len).list()
    res = max(zip(lengths, scores))
    #res = seq(scores).zip(all_bridges).sorted(reverse=True).list()[:10]
    #ic(res)
    result = res[1]
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
