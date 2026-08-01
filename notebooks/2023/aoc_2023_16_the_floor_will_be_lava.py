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


# %% [markdown]
# # Parse

# %%
def parse(inp):
    return inp.strip().split("\n")


# %% [markdown]
# # Process

# %%
Point = build_arithmetic_namedtuple(Point2D)
right = Point(1, 0)
left = Point(-1, 0)
down = Point(0, 1)
up = Point(0, -1)

def process(parsed, start=Point(0, 0), dir=right):
    ics(parsed)
    grid = parsed
    H = len(grid)
    W = len(grid[0])
    visited = set()
    traveled = set()
    queue = []
    queue = deque()
    put, get = get_queue_functions_fifo(queue)
    put((start, dir))
    iterations = 0
    prog_step = 100

    while queue:
        iterations += 1
        pos, dir = get()

        if 0 <= pos.y < H and 0 <= pos.x < W:
            visited.add(pos)
            check = pos.x, pos.y, dir.x, dir.y

            if check in traveled:
                continue

            traveled.add(check)

            if is_sample and not (iterations % prog_step):
                ics(get_vis_map(visited))

            match grid[pos.y][pos.x]:
                case "|" if dir.x:
                    put((pos + up, up))
                    put((pos + down, down))

                case "-" if dir.y:
                    put((pos + left, left))
                    put((pos + right, right))

                case "\\":
                    dir = Point(dir.y, dir.x)
                    put((pos + dir, dir))

                case "/":
                    dir = Point(-dir.y, -dir.x)
                    put((pos + dir, dir))

                case _:
                    put((pos + dir, dir))

    #follow_path(Point(0, 0), right)
    ics(get_vis_map(visited))
    return len(visited)


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    grid = parsed
    H = len(grid)
    W = len(grid[0])
    bot = H - 1
    right_side = W - 1
    max_by_x = max(max(process(parsed, Point(x, 0), down), process(parsed, Point(x, bot), up))  for x in range(W))
    max_by_y = max(max(process(parsed, Point(0, y), right), process(parsed, Point(right_side, y), left)) for y in range(H))
    return max(max_by_x, max_by_y)

def part2(inp):
    parsed = parse(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
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
