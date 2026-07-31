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
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils, aoc_2019_intcode
from aoc_utils import * # this includes adding c:\ut to sys.path
from utilities import *
from iter_utils import *
from aoc_2019_intcode import process_intcodes, parse_intcodes
import seq_extensions # when running standalone, apparently need this import explicitly in main module


# %% [markdown]
# # Parse

# %%
def parse_data(inp):
    return parse_intcodes(inp)


# %% [markdown]
# # Process

# %%
def process(parsed):
    #ics(parsed)
    generator = process_intcodes(parsed)
    screen = set()

    for x, y, id in batched(generator, 3):
        coord = x, y

        if id == 2:
            screen.add(coord)
        else:
            screen.discard(coord)

    if is_sample:
        print(get_vis_map_multiline_str(map_list(itemgetter(0), screen), map_list(itemgetter(1), screen)))

    return len(screen)


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
#    ics(parsed)
    memory = list(parsed)
    generator = process_intcodes(memory)

    screen = set()
    walls = set()
    special_chars = []
    min_x, max_x = 10000,0
    min_y, max_y = 10000,0

    for step, (x, y, id) in enumerate(batched(generator, 3)):
        coord = x, y
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        min_x = min(min_x, x)
        min_y = min(min_y, y)

        if x == y == 0:
            if walls:
                print(get_vis_map_multiline_str(map_list(itemgetter(0), walls), map_list(itemgetter(1), walls), special_chars=special_chars))
                ics(step, max_x, max_y, len(special_chars), len(walls))
                walls = set()
                special_chars = []
                break

        if id == 1:
            walls.add(coord)
        elif id == 2:
            special_chars.append(("$", x, y))
        elif id == 3:
            special_chars.append(("=", x, y))
        elif id == 4:
            special_chars.append(("*", x, y))

    ics(step, min_x, min_y, max_x, max_y, len(special_chars), len(walls))
    print(get_vis_map_multiline_str(map_list(itemgetter(0), walls), map_list(itemgetter(1), walls), special_chars=special_chars))
    screen_size = (max_x+1) * (max_y+1)

    #if is_sample:
        #print(get_vis_map_multiline_str(map_list(itemgetter(0), screen), map_list(itemgetter(1), screen)))

    # proceed on assumption that we need an input every time the ball is painted

    memory = list(parsed)
    memory[0] = 2 # per instructions set memory address 0 to 2 to play for free
    generator = process_intcodes(memory)
    ball_x = None
    paddle_x = None
    score = None

    if 1:
        input = None

        try:
            for step in count():
            #for step in range(screen_size * 2):
                x = generator.send(input)
                y = next(generator)
                id = next(generator)
                input = None

                if x == y == 0:
                    ics(step, "new screen")
                elif x == -1 and y == 0:
                    score = id
                    #ics(step, score)
                elif id == 4:
                    #ics(step, "ball painted", x, y)
                    ball_x = x

                    if paddle_x is None or ball_x == paddle_x:
                        input = 0
                    else:
                        input = (ball_x-paddle_x) // abs(ball_x-paddle_x)

                    #ics(step, input)
                elif id == 3:
                    #ics(step, "paddle painted", x, y)
                    paddle_x = x

        except StopIteration:
            ics("stopped", step)
        except GeneratorExit:
            ics("exited", step)

    return score



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
