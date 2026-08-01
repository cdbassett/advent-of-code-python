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
Tower = namedtuple("Tower","program,weight,supporting")

def parse_line(line):
    parts = replace_multi(line, ",()->").split()
    return Tower(parts[0], int(parts[1]), parts[2:])

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def get_base(towers):
    all_child_towers = sets_union(t.supporting for t in towers)
    #ics(all_child_towers)
    base = seq(towers).where(lambda t: t.supporting and t.program not in all_child_towers).one()
    return base

def process(parsed):
    #ics(parsed)
    #towers_by_prog = dict((t.program, t) for t in parsed)
    base = get_base(parsed)
    return base.program


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
from utils.pathfinding_redblob import *

def process2(parsed):
    def is_goal(current, goal):
        return False

    @cache
    def children_costs(program):
        tower = towers_by_prog[program]
        #return [towers_by_prog[p].weight for p in tower.supporting]
        return tower.weight + sum(children_costs(p) for p in tower.supporting)


    #ics(parsed)
    base = get_base(parsed)
    graph = SimpleGraph()
    towers_by_prog = dict((t.program, t) for t in parsed)
    assert all(len(tower.supporting) != 1 for tower in parsed)
    parents = {}

    for tower in parsed:
        for program in tower.supporting:
            parents[program] = tower.program

    base_children = base.supporting
    child_costs = [children_costs(p) for p in base_children]
    ics(child_costs)

    checking = base
    parent = base
    parent_wrong = None

    while True:
        #tower = towers_by_prog[checking]
        child_costs = [children_costs(p) for p in checking.supporting]
        ic(checking, child_costs)

        if len(set(child_costs)) == len(child_costs):
            ics("found", checking)
            break
        else:
            cnt = Counter(child_costs)
            mc = cnt.most_common(2)
            correct = mc[0][0]

            if len(mc) == 1:
                # parent tower was faulty
                ic(parent, parent_wrong)
                #return parent.weight + parent_wrong
                return checking.weight + parent_wrong
                break

            ic(correct, cnt)
            #ics(seq(zip(checking.supporting, child_costs)))
            bad = seq(zip(checking.supporting, child_costs)).where(lambda a: a[1] != correct).one()[0]
            parent = checking
            parent_wrong = correct - mc[1][0]
            checking = towers_by_prog[bad]


    if 0:
        for tower in parsed:
            #graph.edges[tower.program] = [towers_by_prog[program] for program in tower.supporting]
            graph.edges[tower.program] = tower.supporting

        came_from, current = breadth_first_search(graph, base, None) # no goal so process everything, we just want came_from
    # came_from[program should be parent of program]


    #offending_tower

    return None


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

ics(sum([]))
part2(sample_data2)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)
# 11646 is too high
