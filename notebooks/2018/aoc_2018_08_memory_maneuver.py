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
import pyperclip

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
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

# %%
for sample in sample_data1s:
    print(sample)
    print("=======================")


# %% [markdown]
# # Parse

# %%
def parse(inp):
    return string_to_integers_list(inp)


# %% [markdown]
# # Process

# %%
def sum_meta(sq):
    child_cnt, meta_count = islice(sq, 2)
    #ics(child_cnt, meta_count)
    child_sum = sum(sum_meta(sq) for _ in range(child_cnt))
    meta_data = islice(sq, meta_count)
    #ics(child_sum, meta_data)
    return child_sum + sum(meta_data)

def process(parsed):
    ic(len(parsed))
    ics(parsed)
    return sum_meta(iter(parsed))


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
Node = namedtuple("Node","children,meta_data")

def build_nodes(sq):
    child_cnt, meta_count = islice(sq, 2)
    children = [build_nodes(sq) for _ in range(child_cnt)]
    meta_data = list(islice(sq, meta_count))
    return Node(children, meta_data)

def node_value(node):
    ics(node)
    if not node.children:
        return sum(node.meta_data)

    return sum(node_value(node.children[i-1]) for i in node.meta_data if 0 <= i-1 < len(node.children))

def process2(parsed):
    nodes = build_nodes(iter(parsed))
    ics(nodes)
    return node_value(nodes)


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
