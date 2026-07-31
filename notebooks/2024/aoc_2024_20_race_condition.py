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

# %% editable=false
from aoc_utils import *
if is_notebook():
    print(get_aoc_url())

# %% [markdown]
# # Imports

# %%
# %load_ext autoreload

# %%
import os
import sys
from collections import *
import re
import math

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils, pathfinding_redblob
from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module
import pathfinding_redblob as pf

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
def parse_data(inp):
    return inp.strip().split("\n")


# %% [markdown]
# # Process

# %% [markdown]
#     min path length is min_skip 
#     point needs to be within 2 x / 2 y of later point
#     point may need to start with wall
#
# OR
#     track position in path of each point
#     for each non-wall point:
#         in each direction (but not outside) check if next point is further in path
#         from index determhow mant steps are saved
#         

# %%
def setup(parsed):
    W, H = width_height(parsed)
    start_pos = first(get_char_coords(parsed, "S"))
    end_pos = first(get_char_coords(parsed, "E"))
    grid = pf.SquareGrid(W, H)
    walls = grid.walls = set(get_char_coords(parsed, "#"))
    inner_walls = set(p for p in walls if not (p[0] == 0 or p[1] == 0 or p[0] == W-1 or p[1] == H-1))
    came_from, cost_so_far, current = pf.a_star_search(grid, start_pos, end_pos)
    path = pf.reconstruct_path(came_from, start_pos, end_pos)
    point_indices = dict((p, n) for n, p in enumerate(path))
    return start_pos, end_pos, grid, inner_walls, came_from, path, point_indices
    
# note, sample and actual data have no unused paths
def process(parsed, min_skip=100):
    def check_skip(p1, p2):
        grid.walls = walls.difference_update((p1, p2))
        came_from, cost_so_far, current = pf.a_star_search(grid, start_pos, end_pos)
        return path_length - cost_so_far[end_pos]
    
    def neighbors(p, *skip):
        return [pn for movement in movements if (pn := add_tuple(p, movement)) not in skip]
    
    start_pos, end_pos, grid, inner_walls, came_from, path, point_indices = setup(parsed)
    walls = grid.walls
    path_length = len(path)
    ic(min_skip, path_length)
    #ics(path)

    if is_sample:
        print(get_vis_map_multiline_str_def(grid.walls, path, end_pos))
        
    counts_by_skip = defaultdict(int)
    
    for (n, p), (_, pnext) in pairwise(enumerate(path)):
        for pn in neighbors(p, pnext): 
            if pn in inner_walls:
                for rp in neighbors(pn, p):
                    if (pi := point_indices.get(rp)) is not None and (skip := pi-n-2) >= min_skip:
                        #ics(n, p, pnext, pn, rp, pi, skip)
                        counts_by_skip[skip] += 1

    ics(sorted(counts_by_skip.items()))            
    return sum(counts_by_skip.values()) 


# %%
def part1(inp, min_skip=100):
    parsed = parse_data(inp)
    result = process(parsed, min_skip)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed, min_skip=100):
    start_pos, end_pos, grid, inner_walls, came_from, path, point_indices = setup(parsed)
    path_length = len(path)
    e_path = list(enumerate(path))
    counts_by_skip = defaultdict(set)

    # approximately same tiem either way, thinks it's slow bc tuples isntead of compelx
    if 1:
        for n1, p1 in e_path:
            for n2, p2 in e_path[n1 + min_skip + 1:]:
                if (md := manhattan(p1, p2)) <= 20 and (skip := n2 - n1 - md) >= min_skip:
                    counts_by_skip[skip].add((p1, p2))
    else:
        for n1, p1 in e_path:
            for p2 in manhattan_distance_neighbors(p1, 20):
                if (n2 := point_indices(p2)) is not None:
                    if (skip := n2 - n1 - md) >= min_skip:
                        counts_by_skip[skip].add((p1, p2))

    counts = sorted(starmap(lambda cnt, st: (cnt, len(st)), counts_by_skip.items()))
    ics(counts)
    return sum(map(second, counts))     


# %%
def part2(inp, min_skip=100):
    parsed = parse_data(inp)
    result = process2(parsed, min_skip)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

for sample_data1 in sample_data1s:
    part1(sample_data1, min_skip=1)

part2(sample_data2, min_skip=50)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp) # 982425


# %% [markdown]
# # Others' solutions

# %%
# modified from https://topaz.github.io/paste/#XQAAAQDzBQAAAAAAAAAzHIoib6pXbueH4X9F244lVRDcOZab5q1+VXn364pL+SRffja30hdXttaE7WNKeQ7YQYfCmvNmXtMmPnp9VoAipCPPCSFVXbF3C6Hazfev55pCCwcduNm1Cm0ag6t477DDXN2xIUcA2sUEU+xMoPYNrd4kF/rO5udiZtPNoGWw2ZhvcboSwhac3+q0PSnoQA4ONuLcT8CbUQeZuUwGVy9UHjyqpBDeXaouWSbRdXAdi3qUQcpCDzVPcR/Z9Fy2qN6Th6nIaE2G8mEcM9Lw52yfFVlEPSu50IEYIDYHNd78OdbaXisAWjQB7VzMlaDema2dgLeXh+x9MPSUG7ohCJCqd2lxRUBQf9PUcImYcrurniYc5zjB4+eYbFZRcZBExi7olC9/37dNilcYPf9bd8WxrfBauMgBVqhDJiR9rNErgtKDgpt89o1v78qfPS9KXEUyvs8/07lWsmdnneaZKCM6m+lSAfy96vx59YgoxelKoNS4Z90c0wX2yJgWJ0zPqQy/KQaxpEg351aN0MKcy0DSMfZFcBJcZUhljrOQNZLqmbi5TETepqZhod5FNJMHnbslKrhGUXx9jYxsUNM357CIO8icVNsD5N9fxXgO5vaCxd2U7sXxiSs6M+QFc6BE3rjEO7QMg9heRe+8O4IwpELAlgyBv7wGIFpnLqbs+WZpZhZg2w8/upJslSeVwhe+KWqX7PZbuihWtiw+dlaw1OHRiehzeGsTD+0jyTUTq6sei4DYgtjSfO/z8i9TuTU2TLuF5AK3gwgoX9lkx6C17XXQFbQZFCcbYvMZv/u2JhsOQ1MkL0i32Jpq1uSUOg92zedoOBn71Doo/wniFTYDkVc8PB9t/y6tsAA=
def solve():
    from collections import deque
    from aocd.models import Puzzle
    #from util import grid, directions, manhattan_distance, manhattan_distance_neighbors
    
    aoc_puzzle = Puzzle(year=2024, day=20)
    lines = aoc_puzzle.input_data.split('\n')
    g = build_complex_points_dict(lines)
    
    start = next(p for p, c in g.items() if c == 'S')
    end = next(p for p, c in g.items() if c == 'E')
    g[start] = '.'
    g[end] = '.'
    
    bfs = deque([(start, 0, [start])])
    
    best_no_cheat = None
    best_track = None
    visited = set()
    directions = movements_c
    
    while True:
        pos, score, v = bfs.popleft()
    
        if pos == end:
            best_no_cheat = score
            best_track = {vv: e for e, vv in enumerate(v)}
            break
        elif pos not in visited:
            visited.add(pos)
            for d in directions:
                track = g.get(new_pos := pos + d) == '.'
                if track:
                    bfs.append((new_pos, score + 1, v + [new_pos]))
    
    best_two_sec_cheats = {}
    for pos, e in best_track.items():
        for d in directions:
            if g.get(one := pos + d) == '#':
                if (e2 := best_track.get(two := pos + 2 * d)) and e2 > e:
                    best_two_sec_cheats[one, two] = e2 - e - 2
    
    print(sum(v >= 100 for v in best_two_sec_cheats.values()))
    
    best_twenty_sec_cheats = {}
    for pos1, e in best_track.items():
        for pos2 in manhattan_distance_neighbors_c(pos1, r=20):
            if (e2 := best_track.get(pos2)) and e2 > e:
                best_twenty_sec_cheats[pos1, pos2] = e2 - e - manhattan_c(pos1, pos2)
    
    print(sum(v >= 100 for v in best_twenty_sec_cheats.values()))
    
solve()
