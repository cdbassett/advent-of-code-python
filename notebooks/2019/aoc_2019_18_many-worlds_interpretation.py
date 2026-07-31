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

# %% [markdown] editable=true slideshow={"slide_type": ""}
# # Imports

# %% editable=true slideshow={"slide_type": ""}
# %load_ext autoreload

# %% editable=true slideshow={"slide_type": ""}
from collections import *

import numpy as np
from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils, pathfinding_redblob
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from iter_utils import *
from pathfinding_redblob import *
import pathfinding_redblob
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module


# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0]
sample_data2s = [
"""#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######""",
"""###############
#d.ABC.#.....a#
######@#@######
###############
######@#@######
#b.....#.....c#
###############""",
"""#############
#DcBa.#.GhKl#
#.###@#@#I###
#e#d#####j#k#
###C#@#@###J#
#fEbA.#.FgHi#
#############""",
"""#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba@#@BcIJ#
#############
#nK.L@#@G...#
#M###N#H###.#
#o#m..#i#jk.#
#############"""]


# %% [markdown]
# # Parse

# %%
def parse_data(inp):
    return build_numpy_array_from_string_graph(inp)


# %% [markdown]
# # Process

# %%
# contains collected keys as well as x and y
class KeyGrid(SquareGrid):
    def __init__(self, width: int, height: int, chars):
        super().__init__(width, height)
        self.chars = chars

    # allow empty space, keys, and doors we have keys for
    def passable(self, from_id: GridLocation, id: GridLocation) -> bool:
        x, y, *_ = id
        keys = from_id[2]
        c = self.chars[x, y]
        #res = c in ".@" or c.islower() and c.upper() not in keys or c in keys
        res = c in ".@" or c.islower() or c in keys
        #ics(from_id, id, c, keys, res)
        return res

    # regular neighbors but tack on keys - but only if it's not already present
    def neighbors(self, id: GridLocation, came_from: dict[Location, Optional[Location]]) -> Iterator[GridLocation]:
        results = list(super().neighbors(id, came_from))
        #ics("neighbors", results)
        x, y, keys = id
        results = [(x, y, sjoin(sorted(keys + c.upper() + c.lower()))) if (c := self.chars[x, y]).islower() and c not in keys else (x, y, keys) for x, y in results] # add keys, uppercased for simpler matching with locks
        return results

    def priority(new_cost: float, current: Location, next: Location) -> float:
        return (new_cost, -len(next[2]))


# contains collected keys as well as location
@dataclass
class KeyGraph:
    junctions: dict # id -> dict(id) (id -> cost) (such as returned from dijkstra_reduced_node_connections)
    key_count: int

    # allow empty space, keys, and doors we have keys for
    def passable(self, from_id: GridLocation, c: string) -> bool:
        keys = from_id[-1]
        res = c in ".@0123" or c.islower() or c in keys
        #ics(from_id,c, keys, res)
        return res

    # regular neighbors but tack on keys - but only if it's not already present
    def neighbors(self, id, came_from):
        results = self.junctions[id[0]].keys()
        c, keys = id
        results = [(c, sjoin(sorted(keys + c.upper() + c.lower()))) if c.islower() and c not in keys else (c, keys) for c in results if self.passable(id, c)] # add keys, uppercased for simpler matching with locks
        return results

        # based on the assumption that to_id is a neighbor of from_id
    def cost(self, from_id: Location, to_id: Location) -> float:
        # only one letter should be different
        return self.junctions[from_id[0]][to_id[0]]

    # for astar, try to estimate cost until goal reached
    # returning value lower than actual will reduce performance, returning value higher will cause incorrect result (not shortest path)
    def heuristic(self, id: Location, goal: Location) -> float:
        return (self.key_count - len(id[-1])) // 2

    def is_goal(self, current, goal):
        res = len(current[-1]) == self.key_count
        #ics(current, len(current[2]), key_count, res)
        return res

def convert_junctions(junction_nodes, parsed):
    return convert_junction_keys(junction_nodes, parsed.__getitem__)

def process(parsed):
    def callback(cbi):
        ic(cbi.iterations, cbi.current, cbi.neighbors, cbi.queue_len, cbi.cost_so_far[current])
        #path = reconstruct_path(came_from, robot_pos, current)
        #special_chars = [(graph_char_circle_cross, x, y) for x, y, *_ in path] + [(graph_char_bullseye, current[0], current[1])]
        #print(get_vis_map_multiline_str([], [], special_chars=special_chars, filled_char=graph_char_light_block, blank_char=graph_char_small_dot))

    chars_yx = parsed.T # parsed is transposed for index like x,y
    W, H = width(chars_yx), height(chars_yx)
    ic(W, H)

    if is_sample:
        print(get_numpy_char_array_repr(chars_yx))

    key_count = np.count_nonzero(np.char.islower(parsed)) * 2 # goal is to collect all keys, we need to know how many there are - we collect upper and lower of each key for lookup speed

    # this approach reduces grids to graph of only relevant nodes
    # not doing this made the real input take 28 seconds vs. 0,4
    if 1:
        start = tuple(np.argwhere(parsed == "@")[0])
        grid = SquareGrid(W, H)
        grid.walls = set(map(tuple, np.argwhere(parsed == "#")))
        goals = set(map(tuple, np.argwhere(parsed != "."))) - grid.walls # we want everything but dots and walls
        ic(len(goals))
        # build costs from every interesting node to every other interesting node
        junction_nodes = pathfinding_redblob.dijkstra_reduced_node_connections(grid, goals, nearest_neighbors_only=True)
        ic(len(junction_nodes))
            # convert junctions from x,y to characters - should all be unique
        junctions_by_char = convert_junctions(junction_nodes, parsed)
        start = ("@", "") # start with empty keys
        ic(start, key_count)
        graph = KeyGraph(junctions_by_char, key_count)
        came_from, cost_so_far, current = a_star_search(graph, start, goal=None, callback=None, callback_step=1000)
        ic(current)
        return cost_so_far[current]
    else:
        starts = tuple(np.argwhere(parsed == "@")) + ("",)
        grid = KeyGrid(W, H, parsed)
        grid.walls = set(map(tuple, np.argwhere(parsed == "#")))

        if 0:
            came_from, cost_so_far, current = dijkstra_search(grid, start, goal=None, callback=callback, callback_step=1000) # prioritize paths having more keys
        else:
            came_from, cost_so_far, current = a_star_search(grid, start, goal=None, callback=None, callback_step=1000)

        ic(current)
        return cost_so_far[current]


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
# nodes contain strings for each of the 4 robots, plus all the keys they jointly hold
@dataclass
class MultiKeyGraph(KeyGraph):
    # inherit passasle, works for single subnode change at a time
    # inherit heuristic

    # regular neighbors but tack on keys - but only if it's not already present
    def neighbors(self, id, came_from):
        results = []
        robots, keys = id

        for n, r in enumerate(robots):
            sub_results = self.junctions[r].keys()
            pre,post = robots[:n], robots[n+1:]
            #ics(n, r, pre, post, sub_results)
            results.extend([(pre+c+post, sjoin(sorted(keys + c.upper() + c.lower()))) if c.islower() and c not in keys else (pre+c+post, keys) for c in sub_results if self.passable(id, c)]) # add keys, uppercased for simpler matching with locks

        #ics(results)
        return results

        # based on the assumption that to_id is a neighbor of from_id
    def cost(self, from_id: Location, to_id: Location) -> float:
        # only one letter should be different
        #ics(from_id, to_id)
        return sum(self.junctions[a][b] for a, b in zip(from_id[0], to_id[0]) if a != b )

def process2(parsed):
    chars_yx = parsed.T # parsed is transposed for index like x,y
    W, H = width(chars_yx), height(chars_yx)
    ic(W, H)
    inlay = np.array(list(batched(list("0#1###2#3"),3)))
    ic(inlay)
    parsed[W//2-1:W//2+2, H//2-1:H//2+2] = inlay
    if is_sample:
        print(get_numpy_char_array_repr(parsed.T))
    starts = maplist(tuple, np.argwhere(np.char.isdigit(parsed)))
    ic(starts)
    # can use one grid for all 4 quarters at once for reduced nodes
    grid = SquareGrid(W, H)
    walls = set(map(tuple, np.argwhere(parsed == "#")))
    goals = set(map(tuple, np.argwhere(parsed != "."))) - walls # we want everything but dots and walls
    ic(len(goals))
    grid.walls = walls
    junction_nodes = pathfinding_redblob.dijkstra_reduced_node_connections(grid, goals, nearest_neighbors_only=True)
    ic(len(junction_nodes))
        # convert junctions from x,y to characters - should all be unique
    junctions_by_char = convert_junctions(junction_nodes, parsed)
    #ic(junctions_by_char)
    key_count = np.count_nonzero(np.char.islower(parsed)) * 2 # goal is to collect all keys, we need to know how many there are - we collect upper and lower of each key for lookup speed


    # build costs from every interesting node to every other interesting node
    #for start, grid in zip(starts, grids):
    if 1:
        start = ("0123", "") # start with empty keys
        ic(start, key_count)
        graph = MultiKeyGraph(junctions_by_char, key_count)
        came_from, cost_so_far, current = a_star_search(graph, start, goal=None, callback=None, callback_step=1000)
        ic(current)
        return cost_so_far[current]

    return None


# %%
def part2(inp):
    parsed = parse_data(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

if 1:
    if 1:
        for sample_data1 in sample_data1s:
            part1(sample_data1)
    else:
        part1(sample_data1s[1])

if 1:
    for sample_data2 in sample_data2s:
        part2(sample_data2)
else:
    part2(sample_data2s[-1])

#part2(sample_data2) sample data doesn't work for part 2

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp) # 3512
part2(real_inp) # 1514

# %% [markdown]
# # Others' solutions
