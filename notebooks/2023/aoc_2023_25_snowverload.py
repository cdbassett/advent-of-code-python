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
# [Advent of Code 2023 - Day 25](https://adventofcode.com/2023/day/25)

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
from dataclasses import dataclass,field
from typing import Protocol, Iterator, Tuple, TypeVar, Optional

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, pathfinding_redblob
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module
import utils.pathfinding_redblob as pathfinding_redblob

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
def parse_line(line):
    key, parts = line.split(":")
    return key, parts.split()

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
# long complicated attempt that doesn't work befcuase there are too many combinations
@dataclass
class JunctionGraph:
    junctions: dict # id -> list of ids

    def neighbors(self, id: pathfinding_redblob.Location, came_from: dict[pathfinding_redblob.Location, Optional[pathfinding_redblob.Location]]) -> Iterator[pathfinding_redblob.GridLocation]:
        #ics(id)
        return self.junctions[id]

def is_connected(a, b, connections):
    pass

def add_connection(connections, left, right):
    connections[left].add(right)
    connections[right].add(left)

def remove_connection_ex(connections, left, right):
    new_set = connections[left].difference([right])

    if new_set:
        connections[left] = new_set
    else:
        del connections[left]

def remove_connection(connections, left, right):
    remove_connection_ex(connections, left, right)
    remove_connection_ex(connections, right, left)

def process(parsed):
    #ics(parsed)
    connections = defaultdict(set)
    single_sided = []
    nodes = set()

    for left, rights in parsed:
        for right in rights:
            add_connection(connections, left, right)
            single_sided.append((left, right))
            nodes.add(left)
            nodes.add(right)

    ic(len(single_sided))
    ic(len(connections))
    ics(connections)
    candidate = None
    best = None
    node_count = len(nodes)
    ics(node_count)

    # possible early fail tests:
    #     all nodes are still connected
    #     one group is grossly over or undersized
    for n, (a, b, c) in seq(single_sided).combinations(3).enumerate():
        test_connections = connections.copy()
        side_nodes = set()
        # break the 3 connections
        for l, r in (a, b, c):
            remove_connection(test_connections, l, r)
            side_nodes.add(l)
            side_nodes.add(r)

        #ics(test_connections)
        side_nodes = list(s for s in side_nodes if s in test_connections)

        if len(side_nodes) < 2:
            continue

        junction_graph = JunctionGraph(test_connections)
        start_node, *goal_nodes = side_nodes
        goal_nodes = set(goal_nodes)
        final_paths = pathfinding_redblob.breadth_first_search_multi_goals(junction_graph, start_node, goal_nodes, first_reach_of_goals_only=True)
        found_goals = set(fp[-1] for fp in final_paths)

        # all nodes we directly disconnected are still connected together
        if len(found_goals) == len(goal_nodes):
            #print("continue")
            continue

        ics("=============")
        ics(n, a, b, c)
        ic(len(side_nodes))
        ics(start_node, len(goal_nodes), goal_nodes)
        ics(len(found_goals), found_goals)
        other_side_nodes = goal_nodes - found_goals

        if len(other_side_nodes) < 2:
            continue

        first_side_length = pathfinding_redblob.breadth_first_count(junction_graph, start_node)
        ics(first_side_length)

        start_node, *goal_nodes = other_side_nodes
        goal_nodes = set(goal_nodes)
        other_final_paths = pathfinding_redblob.breadth_first_search_multi_goals(junction_graph, start_node, goal_nodes, first_reach_of_goals_only=True)
        found_goals = set(fp[-1] for fp in final_paths)

        ic(len(side_nodes))
        ics(start_node, len(goal_nodes), goal_nodes)
        ics(len(found_goals), found_goals)
        other_side_length = pathfinding_redblob.breadth_first_count(junction_graph, start_node)
        ics(other_side_length)

        # we want all remaning nodes to be connected together
        if len(found_goals) != len(goal_nodes):
            ics("rejected bc other side not complete")
            continue

        score = first_side_length * other_side_length
        ics(score)
        return score

        if best is None or score < best:
            best = score
            candidate = a, b, c
            ics(best)


    return 0


# %%
# this method:
# finds 2 nodes far from each other
# BFS between them 3 times, keeping track of edges used
# BFS counts, this is how many nodes are on one side
@dataclass
class JunctionGraph:
    junctions: dict # id -> list of ids
    skip: set = field(default_factory=set) # edges to in neighbors

    def neighbors(self, id: pathfinding_redblob.Location, came_from: dict[pathfinding_redblob.Location, Optional[pathfinding_redblob.Location]]) -> Iterator[pathfinding_redblob.GridLocation]:
        #ics(id)
        if self.skip:
            return (n for n in self.junctions[id] if (id, n) not in self.skip)

        return self.junctions[id]

def add_connection(connections, left, right):
    connections[left].add(right)
    connections[right].add(left)

def process(parsed):
    def find_far_nodes(start_node):
        came_from, start_node, longest = pathfinding_redblob.breadth_first_count_longest(junction_graph, start_node)
        came_from, end_node, longest = pathfinding_redblob.breadth_first_count_longest(junction_graph, start_node)
        #ic(longest, start_node, end_node)
        return longest, start_node, end_node

    def one_pass(start_node, end_node):
        came_from, current = pathfinding_redblob.breadth_first_search(junction_graph, start_node, end_node)
        #ics(came_from, current)
        ics(current)
        path = pathfinding_redblob.reconstruct_path(came_from, start_node, end_node)
        ics(path, current)
        skip = set(pairwise(path))
        ics(skip)
        junction_graph.skip.update(skip)

    #ics(parsed)
    connections = defaultdict(set)
    single_sided = []
    nodes = set()

    for left, rights in parsed:
        for right in rights:
            add_connection(connections, left, right)
            single_sided.append((left, right))
            nodes.add(left)
            nodes.add(right)

    ic(len(single_sided))
    ic(len(connections))
    ics(connections)
    node_count = len(nodes)
    ics(node_count)

    junction_graph = JunctionGraph(connections)
    list_nodes = list(nodes)

    dist, start_node, end_node = max(find_far_nodes(start_node) for start_node in list_nodes[:10] + list_nodes[-10:])
    ic(start_node, end_node, dist)

    one_pass(start_node, end_node)
    one_pass(start_node, end_node)
    one_pass(start_node, end_node)
    cnt = pathfinding_redblob.breadth_first_count(junction_graph, start_node)
    ics(cnt)
    return cnt * (node_count - cnt)


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
part1(sample_data1) # 54

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp) # 562912
