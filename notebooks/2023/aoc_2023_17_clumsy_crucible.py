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
# [Advent of Code 2023 - Day 17](https://adventofcode.com/2023/day/17)

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
sample_data1, sample_data2 = sample_data1s

# %% [markdown]
# # Parse

# %%
def parse(inp):
    return inp.strip().split("\n")


# %% [markdown]
# # Process

# %% editable=true slideshow={"slide_type": ""}
# location is x, y, direction to current (we add dir as part of location because for this puzzle the same coordinates can be reused (crossed))
class MaxLengthGrid(pathfinding_redblob.GridWithWeights):
    def __init__(self, width: int, height: int, max_run: int, min_run: int, goal):
        super().__init__(width, height)
        self.max_run = max_run
        self.min_run = min_run
        self.goal = goal

    def cost(self, from_node: pathfinding_redblob.GridLocation, to_node: pathfinding_redblob.GridLocation) -> float:
        xl, xh = sorted((to_node[0], from_node[0]))
        yl, yh = sorted((to_node[1], from_node[1]))
        cost_pos = [(x, y) for x in range(xl, xh+1) for y in range(yl, yh+1) if (x,y) != from_node[:2]]
        #ics(from_node, to_node, cost_pos)
        #assert(cost_pos[0] == from_node[:2])
        return sum(self.weights.get(p, 1) for p in cost_pos)

    def neighbors(self, id: pathfinding_redblob.GridLocation, came_from: dict[pathfinding_redblob.Location, Optional[pathfinding_redblob.Location]]) -> Iterator[pathfinding_redblob.GridLocation]:
        def gen(xn, yn, new_dir, i):
            return x + xn * i, y + yn * i, new_dir, -1

        x, y, dir, consec = id
        new_dirs = ((0, 1, "v"), (0, -1, "^")) if dir in "><" else ((1, 0, ">"), (-1, 0, "<"))

            # special case at start bc not moving yet
        if x == y == 0:
            new_dirs = ((0, 1, "v"), (1, 0, ">"))

        neighbors = [gen(xn, yn, new_dir, i) for i in range(self.min_run, self.max_run+1) for xn, yn, new_dir in new_dirs]
        results = filter(self.in_bounds, neighbors)
        neighbors = list(neighbors)
        #ics(self.min_run, self.max_run, id, neighbors)
        return results


# %%
def strip_came_from(came_from):
    return dict((id[:2], node[:2] if node else None) for id, node in came_from.items())

path_letters = [chr(n) for n in [0x24ea] + list(range(0x2460, 0x2460+9))]
#print(path_letters)

def draw_grid(parsed, graph, came_from, start, goal, **style):
    if 1:
        chars = seq(parsed).map(list).list()
        path=pathfinding_redblob.reconstruct_path(came_from, start=start, goal=goal)

        for x, y, dir, cos in path:
            #chars[y][x] = path_letters[ord(chars[y][x]) - ord("0")]
            chars[y][x] = f"{Fore.YELLOW}{Style.BRIGHT}{chars[y][x]}{Style.RESET_ALL}"

        print("\n".join("".join(line) for line in chars))
    else:
        path=pathfinding_redblob.reconstruct_path(came_from, start=start, goal=goal)
        #ics(path, final)
        path = [a[:2] for a in path]
        #ic(seq(path).map(lambda e: grid.weights[e]).sum())
        stripped_came_from = strip_came_from(came_from)
        pathfinding_redblob.draw_grid(graph, path=path, point_to=stripped_came_from, start=start, goal=goal, is_goal = pathfinding_redblob.base_grid_id_eq, **style)

def process(parsed, max_run: int = 3, min_run: int = 1):
    def callback(cbi):
        #if 1:
        #if iterations % 100 == 0 or current[:2] in (callback_locations):
        if 0 and cbi.current[:2] in (callback_locations):
            #use_goal = first(k for k, v in came_from.items() if k[:2] == current[:2])
            ics(cbi.iterations, cbi.current, cbi.cost_so_far[cbi.current], goal, cbi.came_from[cbi.current], len(cbi.came_from), cbi.queue_len, cbi.neighbors)
            #draw_grid(grid, came_from, start, current)

    #ics(parsed)
    H = height(parsed)
    W = width(parsed)
    ic(W, H)
    callback_locations = set([(7,0), (8,0)])
    callback_locations = set([(11,7), (10,7), (9,7)])
    callback_locations = set([(W-1,7), (7,0)])
    callback_locations = set([(7,0)])
    callback_locations = set([(7,H-1),(8,H-1),(9,H-1),(10,H-1)])
    start = 0, 0, ">", 0 # shouldn't track direction of starting cell?
    goal = W-1, H-1
    grid = MaxLengthGrid(W, H, max_run, min_run, goal)
    grid.weights = {(x, y): int(parsed[y][x]) for x, y in product(range(W), range(H))}
    came_from, cost_so_far, final = pathfinding_redblob.a_star_search(grid, start, goal, is_goal = pathfinding_redblob.base_grid_id_eq, callback_step=1, callback=callback if is_sample else None)

    ics(final)

    if is_sample:
        draw_grid(parsed, grid, came_from, start, final)

    #ics(cost_so_far)
    return cost_so_far[final]


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %%
def part2(inp):
    parsed = parse(inp)
    result = process(parsed, max_run = 10, min_run = 4)
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
print_preface_notebook()
part1(sample_data1) # 102
part2(sample_data1) # 94
part2(sample_data2) # 71

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
print_preface_notebook()
part1(real_inp)
part2(real_inp)

# %%
# WTF! complete correct solution!
# https://www.reddit.com/r/adventofcode/comments/18k9ne5/comment/kdqp7jx/?utm_source=share&utm_medium=web2x&context=3
def solve1():
    from heapq import heappop, heappush as push

    G = {i + j*1j: int(c) for i,r in enumerate(real_inp.split("\n"))
                          for j,c in enumerate(r.strip())}

    def f(min, max, end=[*G][-1], x=0):
        todo = [(0,0,0,1), (0,0,0,1j)]
        seen = set()

        while todo:
            val, _, pos, dir = heappop(todo)

            if (pos==end): return val
            if (pos, dir) in seen: continue
            seen.add((pos,dir))

            for d in 1j/dir, -1j/dir:
                for i in range(min, max+1):
                    if pos+d*i in G:
                        v = sum(G[pos+d*j] for j in range(1,i+1))
                        push(todo, (val+v, (x:=x+1), pos+d*i, d))

    print(f(1, 3), f(4, 10))
#solve1()
