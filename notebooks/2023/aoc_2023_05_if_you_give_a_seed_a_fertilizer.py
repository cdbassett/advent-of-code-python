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
import sys
from collections import *
from bisect import bisect_right

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0]
sample_data2 = sample_data1

# %%
amap = namedtuple("Amap","src,dest,entries")
arange = namedtuple("Arange","dest,src,length")

def chunk_to_map(chunk):
    map_desc, *lines = chunk
    map_from, map_to = map_desc.split("-to-")
    return amap(map_from, map_to, seq(lines).map(string_to_integers).starmap(arange).list())

def parse(inp):
    [seeds_str], *maps_strs = split_iterable(inp.strip().replace(" map:", "").split("\n"))
    #ics(seeds_str)
    #ics(maps_strs)
    seeds = string_to_integers(seeds_str)
    maps = seq(maps_strs).map(chunk_to_map)
    return seeds, maps.list()


# %% [markdown]
# # Process

# %%
def translate_ids(ids, working_map):
    #ics(working_map.entries)
    translator = sorted(working_map.entries, key=itemgetter(1))
    #ics(translator)
    new_ids = []

    for id in ids:
        new_id = id
        i = bisect_right(translator, id, key=itemgetter(1))

        if i:
            entry = translator[i-1]

            if entry.src <= id < entry.src + entry.length:
                new_id = id - entry.src + entry.dest
                #ics(id, new_id, entry)

        new_ids.append(new_id)

    #ics(new_ids)
    return new_ids

def process(parsed):
    #ics(parsed)
    seeds, maps = parsed
    ids = seeds
    map_from = "seed"
    map_dict = seq(maps).map(lambda m: (m.src, m)).dict()
    #ics(map_dict)

    while (working_map := map_dict.get(map_from)):
        #ics(map_from, ids)
        ids = translate_ids(ids, working_map)
        #map_to, map_from = working_map.dest, working_map.src
        map_from = working_map.dest

    return min(ids)


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def to_range(e):
    return range(e.src, e.src+e.length)

adjustEntry = namedtuple("AdjustEntry", "start,adjust")

def translate_ids2(ids, working_map):
    #ics(working_map.entries)
    translator = sorted(working_map.entries, key=itemgetter(1))
    intervals = []
    last = 0

    for entry in translator:
        if entry.src > last:
            intervals.append(adjustEntry(last, 0))

        intervals.append(adjustEntry(entry.src, entry.dest - entry.src))
        last = entry.src + entry.length

    intervals.append(adjustEntry(last, 0))
    intervals.append(adjustEntry(sys.maxsize, 0))

    #ics(intervals)
    new_ids = []
    last = len(intervals)-1

    for id, length in seq(ids).grouped(2):
        start = id
        end = id + length

        while start < end:
                # all(val <= x for val in a[lo : i]) for the left side and
                # all(val > x for val in a[i : hi]) for the right side.
            i = bisect_right(intervals, start, key=itemgetter(0))

            if i:
                found = intervals[i-1]
                found_next = intervals[i]
                use_end = min(found_next.start, end)
                #ics(start, end, found, found_next, use_end)
                new_ids.append(start + found.adjust)
                new_ids.append(use_end - start)
                start = found_next.start
            else:
                break

    #ics(new_ids)
    return new_ids

def process2(parsed):
    #ics(parsed)
    seeds, maps = parsed
    ids = seeds
    map_from = "seed"
    map_dict = seq(maps).map(lambda m: (m.src, m)).dict()

    for working_map in maps:
        for a, b in seq(working_map.entries).combinations(2):
            assert not len(range_intersection(range(a.src, a.src+a.length), range(b.src, b.src+b.length)))
    #ics(map_dict)

    while (working_map := map_dict.get(map_from)):
        ics(map_from, ids)
        ids = translate_ids2(ids, working_map)
        map_from = working_map.dest

    return seq(ids).grouped(2).min_by(itemgetter(0))[0]


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
