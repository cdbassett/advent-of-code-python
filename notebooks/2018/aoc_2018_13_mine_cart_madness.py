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
from icecream import ic

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
#print(sample_data1s[1])
sample_data2 = \
r"""/>-<\ .
|   | .
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/""".replace(".", " ")


# %% [markdown]
# # Parse

# %%
def parse(inp):
    return build_numpy_array_from_string_graph(inp)


# %% [markdown]
# # Process

# %%
from utils.aoc_utils import *

def setup(parsed):
    def cart_positions(n, position, direction):
        #for rot in cycle([left, straight, right]):
        turns = iter(cycle([left_vector_transform, straight_vector_transform, right_vector_transform]))

        while True:
            yield tuple(position)
            #ics(n, position, direction)
            position += direction
            next_char = data[*position]
            #ics("    ", position, next_char)
            is_vert = direction[0]

            match next_char:
                case "+":
                    turn = next(turns)
                    direction = np.dot(turn, direction)
                    #ics("    ", turn, direction)
                case "/":
                    turn = right_vector_transform if is_vert else left_vector_transform
                    direction = np.dot(turn, direction)
                    #ics("    ", turn, direction)
                case "\\":
                    turn = left_vector_transform if is_vert else right_vector_transform
                    direction = np.dot(turn, direction)
                    #ics("    ", turn, direction)
                case _:
                    pass


    #if is_sample:
        #print(njoin(parsed))


    data = parsed.T
    H = height(data)
    W = width(data)
    ic(len(data))
#    ics(data)
    ic(W, H)
    #ics(data)
    vehicles = []
#    array_movements = dict((c, np.array([t[0], t[1]])) for c, t in arrow_movements.items()) # we want movements as array and y first
    array_movements = dict((c, np.array([t[1], t[0]])) for c, t in arrow_movements.items()) # we want movements as array and y first

        # get cart positions
        # repair cart positions
    for c, a in array_movements.items():
        indices = data == c
        positions = np.argwhere(indices)
        #ic(c, a, positions)
        data[np.where(indices)] = "|" if a[0] else "-" # "heal" the grid
        vehicles.extend((p, a) for p in positions)

    ic(len(vehicles))
    #ic(vehicles)

    if is_sample:
        print(get_numpy_char_array_repr(data))
        #special_chars = [(data[y][x], x, y) for x, y in product(range(W), range(H))]
        #print(get_vis_map_multiline_str([], [], reversed = False, min_val=None, max_val=None, special_chars=special_chars))

        # create a generator for each cart
        # use pairwise to get last and new positions together
    generators = [pairwise(cart_positions(n, p, a)) for n, (p, a) in enumerate(vehicles)]
    return data, generators

def process(parsed):
    data, generators = setup(parsed)

        # for each iteration of loop, sort pairs so y then x last position dictates order of movement
    #for positions in take(5, zip(*generators)):
    for positions in zip(*generators):
        #ics(positions)
        #char_positions = [("▢", x1, y1) for (y1, x1), (y2, x2) in positions] + [("​▣", x2, y2) for (y1, x1), (y2, x2) in positions]
        #print(get_vis_map_multiline_str([], [], special_chars=special_chars+char_positions))
        vehicle_locations = set(prev for prev, cur in positions)

        # detect collisions during movement
        for prev, cur in sorted(positions):
            if cur in vehicle_locations:
                # crash
                return f"{cur[1]},{cur[0]}"
            else:
                vehicle_locations.remove(prev)
                vehicle_locations.add(cur)

    #ic(np.asarray(data == "v").nonzero()


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def process2(parsed):
    data, generators = setup(parsed)
    crashed = set()
    num_carts = len(generators)
    ic(num_carts)
    H = height(parsed)
    W = width(parsed)
#    special_chars = [(data[y][x], x, y) for x, y in product(range(W), range(H))]

        # for each iteration of loop, sort pairs so y then x last position dictates order of movement
    for iteration, positions in enumerate(zip(*generators)):
        valid_positions = [((prev, cur), cart) for cart, (prev, cur) in enumerate(positions) if cart not in crashed]
        #char_positions = [("0", x1, y1) for (y1, x1, _), (y2, x2, _) in valid_positions] + [("​#", x2, y2) for (y1, x1, _), (y2, x2, _) in valid_positions]
        #print(get_vis_map_multiline_str([], [], special_chars=special_chars+char_positions))
        vehicle_locations = dict((prev, cart) for (prev, cur), cart in valid_positions)
        sorted_positions = sorted(valid_positions)
        #ics()

        # detect collisions during movement
        for (prev, cur), cart in sorted_positions:
            if prev in vehicle_locations: # handle cart being removed by earlier iteration of sorted positions
                if cur in vehicle_locations:
                    # crash
                    crashed.add(cart)
                    other_cart = vehicle_locations[cur]
                    crashed.add(other_cart)
                    del vehicle_locations[prev] # our car
                    del vehicle_locations[cur] # other cart
                    ic(iteration, cur, cart, other_cart, len(crashed), crashed)

                    if len(crashed) == num_carts - 1:
                        curs = [(cart, cur) for cart, (prev, cur) in enumerate(positions) if cart not in crashed]
                        #ic(curs)
                        cart, cur = curs[0]
                        ic(cur, cart)
                        return f"{cur[1]},{cur[0]}"
                else:
                    del vehicle_locations[prev]
                    vehicle_locations[cur] = cart


# %%
def part2(inp):
    parsed = parse(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())
print_preface_notebook()

part1(sample_data1s[1])
part2(sample_data2)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
print_preface_notebook()
#print(real_inp.replace(" ", "."))
part1(real_inp) # 83,121
part2(real_inp) # 102,144
