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
def parse_line(line):
    return string_to_integers(line)

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def setup(parsed):
    edges = defaultdict(list)

    for p, *rest in parsed:
        for r in rest:
            edges[p].append(r)
            edges[r].append(p)

    graph = SimpleGraph()
    graph.edges = edges
    return graph

def process(parsed):
    ics(parsed)
    graph = setup(parsed)
        # bread first search with no goal will traverse all nodes
    came_from, current = breadth_first_search(graph, 0, None)
    return len(came_from)


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    ics(parsed)
    graph = setup(parsed)
    all_nodes = list(graph.edges.keys())
    came_from, current = breadth_first_search(graph, 0, None)
    processed_nodes = set(came_from.keys())
    group_count = 1

    while (remaining_nodes := list(node for node in all_nodes if node not in processed_nodes)):
        ics(len(remaining_nodes))
        graph.edges = dict((node, graph.edges[node]) for node in remaining_nodes)
        came_from, current = breadth_first_search(graph, remaining_nodes[0], None)
        processed_nodes.update(came_from.keys())
        group_count += 1

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

# %%
