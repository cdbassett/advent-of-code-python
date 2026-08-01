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

import numpy as np
from scipy import ndimage

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils, aoc_2019_intcode, pathfinding_redblob
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module
from utils.aoc_2019_intcode import process_intcodes, parse_intcodes
from utils.pathfinding_redblob import *


# %% [markdown]
# # Parse

# %%
def parse_data(inp):
    return parse_intcodes(inp)


# %% [markdown]
# # Process

# %%
def get_char_lines(parsed):
    view = list(process_intcodes(parsed))
    #print(view)
    char_grid = sjoin(map(chr, view))
    char_lines = char_grid.strip().split("\n")
    return char_lines

def process(parsed):
    char_lines = get_char_lines(parsed)
    W, H = width(char_lines), height(char_lines)
    ic(W, H)

    if 1: # with numpy
        with np.printoptions(threshold=np.inf):
            a = np.array(maplist(lambda l: [int(c == "#") for c in l], char_lines))
            #ic(a)
            k = np.array([[0,1,0],[1,1,1],[0,1,0]])
            cr = ndimage.convolve(a, k, mode='constant', cval=0.0)
            #ic(cr)
            intersections = np.argwhere(cr.T==5)
    else:
        intersections = set()
        corners = set()

        for xs, ys in product(sliding_window(range(W), 3), sliding_window(range(H), 3)):
            cx, cy = xs[1], ys[1]
            if char_lines[cy][cx] == "#":
                joining = sum(1 for x, y in ((cx, ys[0]), (cx, ys[2]), (xs[0], cy), (xs[2], cy)) if char_lines[y][x] == "#")
            #ic(xs, ys)
                if joining == 4:
                    intersections.add((cx, cy))
                elif joining == 2:
                    corners.add((cx, cy))

            ic(len(corners))

    ic(len(intersections))
    #ics(intersections)
    res = sum(x * y for x, y in intersections)
    ics(res)

    if is_sample:
        print(njoin(char_lines))

    return res


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
class RobotGrid(SquareGrid):
    def __init__(self, width: int, height: int, chars):
        super().__init__(width, height)
        self.chars = chars

    def passable(self, from_id: GridLocation, id: GridLocation) -> bool:
        return self.chars[id[1]][id[0]] == "#"

    def neighbors(self, id: GridLocation, came_from: dict[Location, Optional[Location]]) -> Iterator[GridLocation]:
        results = list(super().neighbors(id, came_from))
        x, y, *_ = id

            # if an intersection, assume we're only going straight through it
        if len(results) == 4:
            f = came_from[id]

            if x == f[0]: # vertical
                results = [r for r in results if r[0] == x]
            else:
                results = [r for r in results if r[1] == y]

        results = [r+(int(r[0] == x),) for r in results] # 1 if vertical else 0
        return results

def process2(parsed):
    def callback(cbi):
        ic(cbi.iterations, cbi.current, cbi.neighbors, cbi.queue_len)
        path = reconstruct_path(cbi.came_from, robot_pos, cbi.current)
        special_chars = [(graph_char_circle_cross, x, y) for x, y, *_ in path] + [(graph_char_bullseye, cbi.current[0], cbi.current[1])]
        #print(get_vis_map_multiline_str([], [], special_chars=special_chars, filled_char=graph_char_light_block, blank_char=graph_char_small_dot))

    char_lines = get_char_lines(parsed)
    #print(njoin(char_lines))
    W, H = width(char_lines), height(char_lines)
    ic(W, H)
    grid = RobotGrid(W, H, char_lines)
    #ic(maplist(rpartial(str.find, "^"), char_lines))
    robot_pos = max(zip(map(rpartial(str.find, "^"), char_lines), count())) + (0,)
    #robot_pos = yx[1], yx[0]
    ic(robot_pos)
    start = robot_pos
    came_from, current = breadth_first_search(grid, robot_pos, None, callback=callback, callback_step=100)
    path = reconstruct_path(came_from, start, current)
    #ic(path, came_from, current)

    reduced_path = [robot_pos[:2]]
    last = robot_pos

    # skip in-between nodes
    for v, nodes in groupby(path, key = itemgetter(2)):
        nodes = list(nodes)
        reduced_path.append(nodes[-1][:2])

    #ic(reduced_path)
    turns = []

    # reduce to turns and lengths
    # add previous point for initial robot position to indicate pointing up
    for (fx, fy, *_), (tx, ty, *_), (nx, ny, *_) in triplewise([(robot_pos[0], robot_pos[1]+1, 1)] + reduced_path):
        if 1 or fx == tx: # vertical
            l = abs(nx-tx) + abs(ny-ty)
            turnc = complex(nx-tx, ny-ty)
            fromc = complex(tx-fx, ty-fy)
            #ic(fromc, fromc, turnc/fromc)
            # direction * j/-j = right turn direction
            # j/-j = right turn direction / direction
            # determine turn via complex number division
            turn = "R" if (turnc/fromc).imag > 0 else "L"
            turns.append((turn, int(l)))

    ics(len(turns), turns)
    if 0:
        special_chars = [(graph_char_circle_cross, x, y) for x, y, *_ in path] + [(graph_char_bullseye, current[0], current[1])]
        print(get_vis_map_multiline_str([], [], special_chars=special_chars, filled_char=graph_char_light_block, blank_char=graph_char_small_dot))

    A = "R,12,L,8,R,12"
    B = "R,8,R,6,R,6,R,8"
    C = "R,8,L,8,R,8,R,4,R,4"

    if 1: # check to make sure what we're using matches what was calcualted
        needed = [A, B, A, B, C, C, B, C, B, A]
        full = ",".join(needed)
        calced_full = ",".join(str(c) for t in turns for c in t)
        print(calced_full)
        print(full)
        assert full == calced_full

    memory = list(parsed)
    memory[0] = 2 # per instructions set memory address 0 to 2 to wake up
    generator = process_intcodes(memory)
    generator.send(None) # start it
    outputs = []

    for n, s in enumerate(["A,B,A,B,C,C,B,C,B,A", A, B, C, "n"]):
        output = [generator.send(ord(c)) for c in s+"\n"]
        ic(n, s, sjoin(map(chr, output)))
        outputs.extend(output)

    outputs.extend(generator)
    #ic(outputs)
    print(sjoin(map(chr, outputs)))
    return outputs[-1]

    # now we need 3 chunks of turns alnegths that can be combined into previously determiend turns
    # broke it down with search in notepad
    """
    A R,12,L,8,R,12,
    B R,8,R,6,R,6,R,8,
    A R,12,L,8,R,12,
    B R,8,R,6,R,6,R,8,
    C R,8,L,8,R,8,R,4,R,4,
    C R,8,L,8,R,8,R,4,R,4,
    B R,8,R,6,R,6,R,8,
    C R,8,L,8,R,8,R,4,R,4,
    B R,8,R,6,R,6,R,8,
    A R,12,L,8,R,12
    """


# %%
def part2(inp):
    parsed = parse_data(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)

# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())
part1(real_inp)
part2(real_inp)
