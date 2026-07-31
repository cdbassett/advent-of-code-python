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
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, pathfinding_redblob
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module
import utils.pathfinding_redblob

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
#print(sample_data1)


# %% [markdown]
# # Parse

# %%
def parse(inp):
    return inp.strip().split("\n")


# %% [markdown]
# # Process

# %%
class InfiniteGrid(pathfinding_redblob.SquareGrid):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)

    def in_bounds(self, id: pathfinding_redblob.GridLocation) -> bool:
        return True

    def passable(self, from_id: pathfinding_redblob.GridLocation, id: pathfinding_redblob.GridLocation) -> bool:
        return (id[0] % self.width, id[1] % self.height) not in self.walls

def breadth_first_traversal(graph: pathfinding_redblob.Graph, start: pathfinding_redblob.Location, step_count: int):
    """
    When steps_available > 0:
    - If steps_available is odd, there is no way to get back to this location in the steps available.
      This location should be marked as seen.
    - If steps_available is even, then we can ALWAYS get back to this space in the steps available.
      This location should be marked as seen, but also as part of our solution set. """
    frontier = pathfinding_redblob.Queue()
    frontier.put((start, 0))
    final_locations = set()
    current: pathfinding_redblob.Location
    steps: int
    seen = set()

    while not frontier.empty():
        current, steps = frontier.get()
        steps_available = step_count - steps

        if steps == step_count:
            final_locations.add(current)
            seen.add(current)
            continue

        if steps_available % 2 == 0:
            final_locations.add(current)

        for next in graph.neighbors(current, None): # we can retrace steps, unlike standard BFS, but we know things when we do (see comment at beginning)
            if next in seen:
                continue

            frontier.put((next, steps+1))
            seen.add(next)

    return final_locations

def process(parsed, step_count):
    #ics(parsed)
    H = height(parsed)
    W = width(parsed)
    ic(W, H)
    grid = InfiniteGrid(W, H)
    relevant_points = dict(((x, y), c) for x, y in product(range(W), range(H)) if (c := parsed[y][x]) != ".")
    grid.walls = set(p for p, c in relevant_points.items() if c == "#")
    start = seq(p for p, c in relevant_points.items() if c == "S").one()
    final_locations = breadth_first_traversal(grid, start, step_count)
    #ics(final_locations)
    if 0 and is_sample:
        xs, ys = xs_and_ys(grid.walls)
        print_lines("garden", get_vis_map_multiline_str(xs, ys, min_val=0, max_val=max(H,W)-1, special_chars=[("O", x, y) for x, y in final_locations]))

    return len(final_locations)


# %%
def part1(inp, step_count):
    parsed = parse(inp)
    result = process(parsed, step_count)
    print_result(result)
    return result


# %%
def solve_quadratic(data, plot_counts: list[int], steps:int):
    """ Return the total number of reachable plots in a specified number of steps,
    by calculating the answer to the quadratic formula.
    Here we calculate the coefficients a, b and c by using three sample values,
    obtained from a smaller grid.

    Args:
        data (_type_): The original grid tile.
        plot_counts (list[int]): The plot counts determined for small step counts.
        steps (int): The number of steps we must take.
    """
    grid = [[char for char in row] for row in data]
    grid_size = len(grid)

    # determine coefficients
    c = plot_counts[0]
    b = (4*plot_counts[1] - 3*plot_counts[0] - plot_counts[2]) // 2
    a = plot_counts[1] - plot_counts[0] - b

    x = (steps - grid_size//2) // grid_size # number of whole tile lengths
    return a*x**2 + b*x + c

def part2(inp):
    parsed = parse(inp)
    step_counts = [65, 196, 327] # edge of inner grid, then neighbor, then neighbor's neighbor
#    plot_counts = [part1(real_inp, step_count) for step_count in step_counts]
    plot_counts = [process(parsed, step_count) for step_count in step_counts]
    result = solve_quadratic(parsed, plot_counts=plot_counts, steps=26501365)
    #result = process(parsed)
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
print_preface_notebook()
assert part1(sample_data1, 6) == 16

step_counts = [6, 10, 20, 50, 100, 500]
sample_answers = [16, 50, 216, 1594, 6536, 167004]

for sample_step_count, sample_answer in zip(step_counts, sample_answers):
    assert part1(sample_data1,sample_step_count) == sample_answer

#part2(sample_data2)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
print_preface_notebook()

assert part1(real_inp, 64) == 3764

part2(real_inp)
