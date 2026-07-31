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
import re
import math

import numpy as np
from icecream import ic
from colorama import Fore, Style

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
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
def to_ranges(e):
    c, (single, start, end) = e
    rng1 = range(single,single+1)
    rng2 = range(start,end+1)
    return (rng1, rng2) if c == "x" else (rng2, rng1)

def parse_line(line):
    return line[0], string_to_integers_list(line)

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).map(to_ranges).list()


# %% [markdown]
# # Process

# %%
def process(parsed):
    water_char = f"{Fore.BLUE}{Style.BRIGHT}~{Style.RESET_ALL}" if is_sample else "~"
    flow_char = f"{Fore.GREEN}{Style.BRIGHT}|{Style.RESET_ALL}" if is_sample else "|"

    def draw_map():
        if is_sample:
            xs, ys = xs_and_ys(clay)
            special_chars = [(flow_char, x, y) for x, y in drop_water] + [(water_char, x, y) for x, y in water]
            print(get_vis_map_multiline_str(xs, ys, special_chars = special_chars))

    ic(len(parsed))
    global ics
    #ics(parsed)
    ranges = parsed
    #ics(ranges)
    min_x, max_x = seq(ranges).map(itemgetter(0)).map(min).min(), seq(ranges).map(itemgetter(0)).map(max).max()
    min_y, max_y = seq(ranges).map(itemgetter(1)).map(min).min(), seq(ranges).map(itemgetter(1)).map(max).max()
    W, H = max_x - min_x + 1, max_y - min_y + 1
    ic(min_x, max_x, W)
    ic(min_y, max_y, H)
    point_cnt = seq(ranges).level2_map(len).map(math.prod).sum() # approximate, doesn't account for overlaps
    ic(W * H, point_cnt)
    clay = seq(ranges).starmap(product).flatten().set()
    ic(len(clay))
    #ics(clay)
    water = set()
    combined = clay.copy()
    left = min_x -2
    right = max_x + 2

    if 0 and is_sample:
        xs, ys = xs_and_ys(clay)
        print(get_vis_map_multiline_str(xs, ys))

        # each trickle turns into 1 or 2 trickles after it hits sand
    queue = []
    put, get = get_queue_functions_lifo(queue)
    put((500, min_y, 0))
    movement = (0, 1)
    drop_water = set()

    while queue:
        x, y_start, step = np.array(get())
        ics(x, y_start, step, len(queue))

        #if step == 844:
            #ics(x, y_start, step, len(queue))
            #draw_map()
            #ics = ic
        # track flowing water separately from pooled water
        # then if hit water going down, same behavior as hitting clay but starting one further down
        # if hit water sideways, that counts as a drop
        for y in range(y_start, max_y+1):
            next = x, y

            #if next in water: # we've hit water that's already filled
                #break
            #elif next not in clay:
            if next not in combined:
                drop_water.add(next)
            else:
                ics("    clay", next)
                # determine on each side which comes first, a drop or a wall
                drops = 0
                #flood_y = y if next in water else y - 1
                flood_y = y - 1

                while drops == 0 and flood_y > 0 and (x, flood_y) not in clay:
                    air_y = flood_y + 1
                    ics("  ", flood_y, air_y)
                    side_water = set()
                    side_water.add((x, flood_y))

                    for r in range(x-1, left, -1), range(x+1, right):
                        for check_x in r:
                            clay_point = check_x, flood_y

                            if clay_point in clay:
                                ics("    wall", clay_point)
                                break

                            side_water.add(clay_point) # whether a drop or wall comes, this point will be filled with water
                            air_point = check_x, air_y

                            if air_point not in clay and air_point not in water:
                                ics("    air", air_point)

                                if air_point not in drop_water: # don't start another drop process if it's already been done
                                    put(air_point + (step+1,))

                                drops += 1
                                break

                    if drops:
                         drop_water.update(side_water)
                    else:
                         water.update(side_water)
                         combined.update(side_water)
                    flood_y -= 1

                #ic("  ", step)
                if is_sample:
                    draw_map()

                # must have at least one drop, we already added to q
                # so we're done here (with this queue entry of one trickle)
                break

    draw_map()
    settled_cnt = len(water)
    ic(settled_cnt)
    ic(len(drop_water))
    water.update(drop_water)
    ic(len(water))
    return len(water), settled_cnt


# %%
def part1(inp, filt_func=None):
    parsed = parse(inp)

    if filt_func:
        parsed = list(filter(filt_func, parsed))

    result, _ = process(parsed)
    print_result(result)


# %%
def part2(inp):
    parsed = parse(inp)
    _, result = process(parsed)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())
if 0:
    sample_data1 = get_aocd_data()
elif 1:
    sample_data1 = sample_data1s[0]
elif 1:
    sample_data1 = \
    """x=492, y=2..11
y=11, x=492..509
x=509, y=3..11
x=502, y=5..8
x=504, y=5..8"""
else:
    sample_data1 = \
    """x=495, y=3..7
y=7, x=495..501
x=501, y=3..7
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""

part1(sample_data1, lambda r: r[1].stop < 140)
part2(sample_data2)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp) # 34383 is too high 34383
part2(real_inp)

# %%
# https://www.reddit.com/r/adventofcode/comments/a6wpup/comment/ebzesnu/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
def solve1():
    clay = defaultdict(bool)
    settled, flowing = set(), set()

    for line in real_inp.split("\n"):
        a, b, c = map(int, re.findall("([\d]+)", line))
        if line.startswith('x='):
            for y in range(b, c+1):
                clay[a + y * 1j] = True
        else:
            for x in range(b, c+1):
                clay[x + a * 1j] = True

    yl = [p.imag for p in clay]
    ymin, ymax = min(yl), max(yl)
    print("ymin", "ymax", ymin, ymax, "clay fields",len(clay))

    def fill(p, direction= 1j ):
        flowing.add(p)
        below, left, right = p+1j, p-1, p+1

        if not clay[below]:
            if below not in flowing and 1 <= below.imag <= ymax:
                fill(below)
            if below not in settled:
                return False

        l_filled = clay[left]  or left  not in flowing and fill(left , direction=-1)
        r_filled = clay[right] or right not in flowing and fill(right, direction=1)
        #print("left_right_filled", left_filled, right_filled)

        if direction == 1j and l_filled and r_filled:
            settled.add(p)

            while left in flowing:
                settled.add(left)
                left -= 1

            while right in flowing:
                settled.add(right)
                right += 1

        return direction == -1 and (l_filled or clay[left]) or \
               direction ==  1 and (r_filled or clay[right])

    fill(500)

    if 0:
        xs, ys = zip(*map(complex_to_tuple, (p for p in clay if ymin <= p.imag <= ymax)))
        special_chars = [("|", int(i.real), int(i.imag)) for i in flowing if ymin <= i.imag <= ymax] + [("~", int(i.real), int(i.imag)) for i in settled if ymin <= i.imag <= ymax]
        print(get_vis_map_multiline_str(xs, ys, special_chars = special_chars))

    print('part 1:', len([pt for pt in flowing | settled if ymin <= pt.imag <= ymax]))
    print('part 2:', len([pt for pt in settled if ymin <= pt.imag <= ymax]))


