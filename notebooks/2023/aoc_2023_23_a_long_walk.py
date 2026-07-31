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
from collections import *

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, pathfinding_redblob
from aoc_utils import * # this includes adding c:\ut to sys.path
from utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module
import pathfinding_redblob

# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
example

# %%
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0]
sample_data2 = sample_data1


# %% [markdown]
# # Parse

# %%
def parse(inp):
    assert "<" not in inp
    assert "^" not in inp
    return inp.strip().split("\n")


# %% [markdown]
# # Process

# %%
def assumptions_check(relevant_points):
    # make sure that we only encounter slopes bordered on both sides by walls
    for (x, y), c in relevant_points.items():
        if c == "v":
            assert relevant_points[(x+1,y)] == "#" and relevant_points[(x-1,y)] == "#"

        if c == ">":
            assert relevant_points[(x,y+1)] == "#" and relevant_points[(x,y-1)] == "#"


# %%
class GridWithSlopes(pathfinding_redblob.SquareGrid):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)

    def valid_traversal(self, neighbor: pathfinding_redblob.GridLocation, prev: pathfinding_redblob.GridLocation):
        c = self.relevant_points.get(neighbor)

        if c == ">" and prev[0] > neighbor[0] or c == "v" and prev[1] > neighbor[1]:
            #ics("rejected", c, neighbor, prev)
            return False

        return True

    def neighbors(self, id: pathfinding_redblob.GridLocation, came_from: dict[pathfinding_redblob.Location, Optional[pathfinding_redblob.Location]]) -> Iterator[pathfinding_redblob.GridLocation]:
        neighbors = list(super().neighbors(id, came_from))
        #ics(neighbors)
        #last = came_from[id]
        neighbors = [n for n in neighbors if self.valid_traversal(n, id)]
        return neighbors

def process(parsed, part2=False):
    def callback(cbi):
        #came_from = strip_came_from(came_from)
        #use_goal = first(k for k, v in came_from.items() if k[:2] == current[:2])
        ics(cbi.iterations, cbi.current, goal, len(cbi.came_from))

    #ics(parsed)
    H = height(parsed)
    W = width(parsed)
    ic(W,H)
    start = 1, 0
    goal = W-2, H-1
    grid = pathfinding_redblob.SquareGrid(W, H) if part2 else GridWithSlopes(W, H)
    relevant_points = dict(((x, y), c) for x, y in product(range(W), range(H)) if (c := parsed[y][x]) != ".")
    assumptions_check(relevant_points)
    grid.walls = set(p for p, c in relevant_points.items() if c == "#")
    grid.relevant_points = relevant_points
    #came_from, cost_so_far, final = pathfinding_redblob.breadth_first_search_all_paths(grid, start, goal, callback_step=100, callback=callback if is_sample else None)
    final_paths = pathfinding_redblob.breadth_first_search_all_paths(grid, start, goal)
    lengths = [len(p)-1 for p in final_paths] # start is included
    ics(lengths)

    #if is_sample:
    #    pathfinding_redblob.draw_grid(grid, path=pathfinding_redblob.reconstruct_path(came_from, start=start, goal=goal), point_to=came_from, start=start, goal=goal)

    #return cost_so_far[final]
    return max(lengths)


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
from pathfinding_redblob import *

def calc_cost(path, junctions):
    return seq(path).sliding(2).starmap(lambda a, b: junctions[a][b]).sum()

def process2(parsed):
    def callback(cbi):
        print(".")
        ic(cbi.iterations, cbi.current, cbi.queue_size, cbi.path)

    ics(parsed)
    H = height(parsed)
    W = width(parsed)
    start = 1, 0
    goal = W-2, H-1
    ic(W,H,start,goal)
    grid = pathfinding_redblob.SquareGrid(W, H)
    relevant_points = dict(((x, y), c) for x, y in product(range(W), range(H)) if (c := parsed[y][x]) != ".")
    grid.walls = set(p for p, c in relevant_points.items() if c == "#")
    test_walls = [(4,5)]
    test_walls = []
    grid.walls = grid.walls.union(test_walls)
    grid.relevant_points = relevant_points

    #ics(len(keep_nodes), keep_nodes)
    junctions = [(x, y) for x, y in product(range(1,W-1), range(1,H-1)) \
                  if parsed[y][x]=="." and len([c for c in (parsed[y+1][x],parsed[y-1][x],parsed[y][x+1],parsed[y][x-1]) if c in ">v."])>2]
    junctions.append(start)
    junctions.append(goal)
    ic(len(junctions))
    ics(junctions)

    if 0 and is_sample:
        xs, ys = xs_and_ys(grid.walls)
        print_lines("forest", get_vis_map_multiline_str(xs, ys, min_val=0, max_val=max(H,W)-1, special_chars=[(graph_char_circle_cross, x, y) for x, y in junctions], blank_char=graph_char_small_dot, filled_char=graph_char_light_block))

    keep_nodes = pathfinding_redblob.breadth_first_reduced_node_connections(grid, junctions)
    ic(len(keep_nodes))
    ics(keep_nodes)
    junction_nodes = defaultdict(dict)

    for from_loc, to_loc, cost in keep_nodes:
        junction_nodes[from_loc][to_loc] = cost
        junction_nodes[to_loc][from_loc] = cost

    ic(len(junction_nodes))
    ics(junction_nodes)
    reduced_grid = ReducedGraph(junction_nodes)
    final_paths = pathfinding_redblob.breadth_first_search_all_paths(reduced_grid, start, goal, callback_step=100000, callback=callback if is_sample else None)
    ic(len(final_paths))
    #ics(final_paths)
    lengths = [calc_cost(p, junction_nodes) for p in final_paths]
    ic(len(lengths))
    ics(lengths)
    return max(lengths)


# %%
def part2(inp):
    parsed = parse(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
part1(sample_data1) # 94
part2(sample_data2) # 154

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp) # 2250
part2(real_inp) # 6470
