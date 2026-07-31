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
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module
from pathfinding_redblob import *

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
def parse(inp):
    return inp.strip()


# %% [markdown]
# # Process

# %%
def knot_hash_round(lengths, lst, cur_pos = 0, skip_size = 0):
    list_size = len(lst)

    for skip_size, length in enumerate(lengths, skip_size):
        if length > 1:
            use_pos = cur_pos % list_size
            pos_end = (cur_pos + length) % list_size
            #ic(skip_size, length, cur_pos, use_pos, pos_end)

            if pos_end <= use_pos:
                extracted = lst[use_pos:] + lst[:pos_end]
                cutoff = length - pos_end
                rev = list(reversed(extracted))
                #ics("         ", cutoff, extracted, rev)
                lst = rev[cutoff:] + lst[pos_end:use_pos] + rev[:cutoff]
            else:
                lst = lst[:use_pos] + list(reversed(lst[use_pos:pos_end])) + lst[pos_end:]

            #ics("         ", lst)

        cur_pos += length + skip_size

    return lst, cur_pos, skip_size+1

def to_hex(n):
    return  f'{n:02x}'

def knot_hash_str(s):
    parsed = map_list(ord, s.strip())
    lst = list(range(256))
    lengths = parsed + [17, 31, 73, 47, 23]
    cur_pos, skip_size = 0, 0

    for n in range(64):
        lst, cur_pos, skip_size = knot_hash_round(lengths, lst, cur_pos, skip_size)

    return sjoin(seq(lst).grouped(16).map(partial(reduce, operator.xor)).map(to_hex))

def one_row_hash(n, parsed):
    return knot_hash_str(f"{parsed}-{n}")

def process(parsed):
    ics(parsed)
    return seq.range(128).map(rpartial(one_row_hash, parsed)).map(rpartial(int, 16)).map(int.bit_count).sum()

#knot_hash_str("flqrgnkx-0")


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def to_bin(n):
    return f'{n:0128b}'

def setup(parsed):
    edges = defaultdict(list)

    for p, *rest in parsed:
        for r in rest:
            edges[p].append(r)
            edges[r].append(p)

    grid = DefragGrid()
    graph.edges = edges
    return graph

class DefragGrid(SquareGrid):
    def __init__(self, width: int, height: int, points):
        super().__init__(width, height)
        self.points = points

    def passable(self, from_id: GridLocation, id: GridLocation) -> bool:
        return id in self.points

def process2(parsed):
    ics(parsed)
    bin_rows = seq.range(128).map(rpartial(one_row_hash, parsed)).map(rpartial(int, 16)).map(to_bin).list()
    #ics(bin_rows[:2])

    points = set((x, nrow) for nrow, bin_row in enumerate(bin_rows) for x, c in enumerate(bin_row) if c == "1")
    ic(len(points))

    remaining_nodes = set(points)
    grid = DefragGrid(128, 128, remaining_nodes)
    group_count = 0
    processed_nodes = set()

    while True:
        #ics(len(remaining_nodes), group_count)
        start = first_element(remaining_nodes)
        came_from, current = breadth_first_search(grid, start, None)
        processed_nodes.update(came_from.keys())
        remaining_nodes.difference_update(came_from.keys())
        group_count += 1

        if not remaining_nodes:
            return group_count


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
# 1242 is too high
