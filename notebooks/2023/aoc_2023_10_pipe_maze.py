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
from utils.aoc_utils import *
if is_notebook():
    print(get_aoc_url())

# %% [markdown]
# # Imports

# %%
# %load_ext autoreload

# %%
from collections import *

import numpy as np
from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, pathfinding_redblob
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module
import pathfinding_redblob

# %% [markdown]
# # Sample Data

# %%
sample_data1 = """
.|F7.
.FJ|.
SJ.L7
|F--J
LJ-..
"""
sample_data2 = """
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""
sample_data3 = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""
sample_data4 = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""


# %% [markdown]
# # Parse

# %%
def parse(inp):
    return inp.strip().split("\n")


# %% [markdown]
# # Process

# %%
"""
build connected nodes
find sequence that leads back to S
"""
cnct_west = set("-LFS")
cnct_east = set("-7JS")
cnct_north = set("|7FS")
cnct_south = set("|LJS")
corner_chars =  set("LJF7S")

connections = {
    (0, 1): cnct_south,
    (0, -1): cnct_north,
    (1, 0): cnct_east,
    (-1, 0): cnct_west,
}
from pathfinding_redblob import *

class PipeGrid(SquareGrid):
    def __init__(self, width: int, height: int, parsed):
        super().__init__(width, height)
        self.parsed = parsed

    def valid_to(self, id, neighbor):
        x, y = neighbor
        c = self.parsed[y][x]
        diff = subtract_tuple(neighbor, id)
        chk = connections[diff]
        #ics("valid_to", neighbor, diff, chk, c)
        return c in chk

    def valid_from(self, id, neighbor):
        x, y = id
        c = self.parsed[y][x]
        diff = subtract_tuple(id, neighbor)
        chk = connections[diff]
        #ics("valid_from", neighbor, diff, chk, c)
        return c in chk

    def neighbors(self, id: GridLocation, came_from: dict[Location, Optional[Location]]) -> Iterator[GridLocation]:
        x, y = id
        c = self.parsed[y][x]
        #ics(id, c)
        neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]
        results = filter(self.in_bounds, neighbors)
        #ics(neighbors)
        results = [n for n in results if self.valid_to(id, n) and self.valid_from(id, n)]
        #ics(results)
        return results

def prep_graph(parsed):
    H = height(parsed)
    W = width(parsed)
    i = "".join(parsed).index("S")
    start_node = i % W, i // W
    ic(W, H, i, start_node)
    grid = PipeGrid(W, H, parsed)
    return start_node, grid

def bfs(parsed):
    start_node, grid = prep_graph(parsed)
    came_from, current = pathfinding_redblob.breadth_first_search(grid, start_node, None, frontier=FiFoQueue())
    return start_node, grid, current, came_from

def process(parsed):
    #ics(parsed)
    H = height(parsed)
    W = width(parsed)
    start_node, grid, current, came_from = bfs(parsed)
    cnt = len(came_from)
    ics(cnt)

    if 0:
        final_paths = pathfinding_redblob.breadth_first_search_all_paths(grid, start_node, None)
        ic(len(final_paths))
        ics(final_paths)
        lengths = seq(final_paths).map(len).list()
        ic(lengths)
        ends = seq(final_paths).map(lambda x: x[-1]).list()
        ic(ends)

    if is_sample:
        path = pathfinding_redblob.reconstruct_path(came_from, start_node, current)
        #ics(current, came_from, path)
        pathfinding_redblob.draw_grid(grid, point_to=came_from, start=start_node, path=path, goal=current)

    if 1:
        adjusted_inp = "\n".join(parsed).replace("J", "╝").replace("F", "╔").replace("|", "║").replace("L", "╚").replace("7", "╗").replace("-", "═")
        #print(adjusted_inp)
        parsed_adjusted_inp = adjusted_inp.split("\n")
        work = seq(parsed_adjusted_inp).map(list).list()

        for x, y in product(range(W), range(H)):
            if (x, y) not in came_from:
                work[y][x] = " "

        work_str = "\n".join(map(sjoin, work))
        print(work_str)
    return cnt // 2


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    #H = height(parsed)
    #W = width(parsed)
    #start_node, grid, current, came_from = bfs(parsed)

    start_node, grid = prep_graph(parsed)
        # should provide two paths, one in each direction
    final_paths = pathfinding_redblob.breadth_first_search_all_paths(grid, start_node, None)
    #ics(final_paths)
    use_path = final_paths[0]
    boundary = len(use_path)
    corners = [(x, y) for x, y in use_path if parsed[y][x] in corner_chars]

    #path = pathfinding_redblob.reconstruct_path(came_from, start_node, current)
    #ics(current, path)
    #boundary = len(came_from)
    #corners = [(x, y) for x, y in product(range(W), range(H)) if parsed[y][x] in corner_chars]
    xs = np.array([p[0] for p in corners], dtype=np.int_)
    ys = np.array([p[1] for p in corners], dtype=np.int_)
    area = int(round(polygon_area(xs, ys))) # area includes boundary on left and top side
    ic(len(corners), boundary, area)
    internal_only_area = area - boundary // 2 + 1# picks theorem https://en.wikipedia.org/wiki/Pick%27s_theorem
    return internal_only_area


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
part2(sample_data1)
part2(sample_data2)
part2(sample_data3)
part2(sample_data4)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)
# 8588 is too high

# %%
adjusted_inp = real_inp.replace("J", "╝").replace("F", "╔").replace("|", "║").replace("L", "╚").replace("7", "╗").replace("-", "═")
print(adjusted_inp)
parsed_adjusted_inp = adjusted_inp.split("\n")

# %%
