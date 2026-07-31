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
import sympy as sp
from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils, aoc_2019_intcode
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module
from aoc_2019_intcode import process_intcodes, parse_intcodes


# %% [markdown]
# # Parse

# %%
def parse_data(inp):
    return parse_intcodes(inp)    


# %% [markdown]
# # Process

# %%
def get_on(parsed, x, y):
    generator = process_intcodes(parsed)
    generator.send(None)
    generator.send(x)
    return generator.send(y)

def process(parsed, w=50):
    #ics(parsed)
    affected = set()

    for x, y in product(range(w), range(w)):
        if get_on(parsed, x, y):
            affected.add((x, y))
    #ics(affected)
    xs, ys = xs_and_ys(affected)
    print_sample(get_vis_map_multiline_str(xs, ys, special_chars=[("O", 0, 0)]))
    return len(affected)


# %%
def part1(inp, w=50):
    parsed = parse_data(inp)
    result = process(parsed, w=w)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    def get_top_bot(start):
        x = start
    
        for y in count(start, -1):
            if get_on(parsed, x, y):
                bot = y
                break
            
        top = y
        
        for y in count(bot, -1):
            if not get_on(parsed, x, y):
                break
            top = y
            
        return top, bot

    def calc_slopes_etc(start):
        print(f"===== {start} =====")
        ix, iy = 0, 0
        #ix, iy = 3, 2
        run = start + 1 - ix
        top, bot = get_top_bot(start)
        ics(bot, top)
        bot_slope = (bot+1-iy) / run
        top_slope = (top+1-iy) / run
        ics(bot_slope, top_slope)
        if 0:
            x = np.array([ix, start, start ,0])
            y = np.array([iy, bot, top, iy])
            ics(polygon_area(x,y))
        return top, bot, top_slope, bot_slope, top_slope

        # direction means if point is on, which direction on y axis do we look for off
    def find_boundary(x, start_y, direction):
        print(f"looking at {x}, {start_y}, going {'up' if direction == -1 else 'down'}")
        initially_on = get_on(parsed, x, start_y)

        if not initially_on:
            direction = -direction

        on_y = start_y
            
        for y in count(start_y+direction, direction):
            if get_on(parsed, x, y) != initially_on:
                break
            on_y = y
            
        off_y = y
        
        if not initially_on:
            on_y, off_y = off_y, on_y

        ics(on_y, off_y)           
        return on_y
    
    #ics(parsed)
    x = 500
    top, bot, top_slope, bot_slope, top_slope = calc_slopes_etc(x)
    #calc_slopes_etc(999)
    #top, bot, top_slope, bot_slope, top_slope = calc_slopes_etc(9999)
    find_boundary(x, top, -1)
    find_boundary(x, bot, 1)

    x = 49
    print("-----")
    find_boundary(x, round(x * top_slope), -1)
    find_boundary(x, round(x * bot_slope), 1)
    
    x = 10000
    print("-----")
    find_boundary(x, round(x * top_slope), -1)
    find_boundary(x, round(x * bot_slope), 1)

    # y = mx
    # yt = mxt
    # yb = mxb
    # yb = yt + 99
    # xt = xb + 99
    xt, yt, xb, yb = unknowns = sp.symbols('xt yt xb yb')
    equations = []
    equations.append(sp.Eq(yt, top_slope * xt))
    equations.append(sp.Eq(yb, bot_slope * xb))
    equations.append(sp.Eq(yb, yt + 99))
    equations.append(sp.Eq(xt, xb + 99))
    solution = sp.solve(equations, unknowns)
    print(solution)

    initial_xt = int(round(solution[xt]))
    initial_yt = int(round(solution[yt]))
    initial_xb = int(round(solution[xb]))
    initial_yb = int(round(solution[yb]))
    ics(repr(initial_xt), repr(initial_yt), initial_xb, initial_yb)
    
    use_yt = find_boundary(initial_xt, initial_yt, -1)
    use_xt = initial_xt
    ics(use_yt)

    use_yb = find_boundary(initial_xb, initial_yb, 1)
    use_xb = initial_xb
    ics(use_yb)

    while True:
        if any(get_on(parsed, use_xb-(dxu:=dx), use_yb-(dyu:=dy)) and get_on(parsed, use_xt-dx, use_yt-dy) for dx, dy in product(range(1,4), range(1,4))):
        #if get_on(parsed, use_xb-1, use_yb-1) and get_on(parsed, use_xt-1, use_yt-1):
            ics("decrementing all", dxu, dyu)
            use_xb -= dxu
            use_xt -= dxu
            use_yt -= dyu
            use_yb -= dyu
        elif get_on(parsed, use_xb-1, use_yb):
            ics("decrementing x")
            use_xb -= 1
            use_xt -= 1
        elif get_on(parsed, use_xt, use_yt-1):
            ics("decrementing y")
            use_yt -= 1
            use_yb -= 1
        else:
            break
    
    ics(use_xt, use_yt, use_xb, use_yb)
    ics(use_xt - use_xb, use_yb - use_yt)

    if is_sample:
        affected = set()
        x_range=range(use_xb, use_xb+100) 
        y_range=range(use_yt, use_yt+100) 
    
        for x, y in product(range(use_xb-10, use_xb+110), range(use_yt-10, use_yt+110)):
            if x in x_range and y in y_range:
                continue
                
            if get_on(parsed, x, y):
                affected.add((x, y))
        #ics(affected)
        xs, ys = xs_and_ys(affected)
        print_sample(get_vis_map_multiline_str(xs, ys, special_chars=[("O", x, y) for x, y in square_boundary_points(use_xb, use_yt, use_xb+99, use_yt+99)]))
    
    #if use_yt == initial_yt and check_yb == initial_yb:
    return use_xb * 10000 + use_yt


# %%
def part2(inp):
    parsed = parse_data(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
real_inp = get_aocd_data()
insert_sample_functions(False, globals())
#part1(real_inp, 50)
part2(real_inp)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
#part1(real_inp)
part2(real_inp) # 10180726
# 10230829 is too high, 10230730 is too high, 4670368 is too low

# %% [markdown]
# # Others' solutions

# %%
# https://github.com/ephemient/aoc2019/blob/py/src/aoc2019/day19.py
def solve1():
    mem = parse_data(real_inp)
    x, y = 0, 99
    while True:
        while not get_on(mem, x, y):
            x += 1
        if get_on(mem, x + 99, y - 99):
            return 10000 * x + y - 99
        y += 1
print(solve1())        
