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
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from aoc_utils import * # this includes adding c:\ut to sys.path
from utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module

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
print(sample_data1)


# %% [markdown]
# # Parse

# %%
def parse(inp):
    return inp.strip().split("\n")


# %% [markdown]
# # Process

# %%
# either hit a cubed rock or top of grid
def min_y(p, cube_rocks):
    for y in range(p.y-1, -1, -1):
        next_p = (p.x, y)

        if next_p in cube_rocks:
            return y+1

    return 0

def move_rock_north(p, cube_rocks, round_rocks):
    earliest_row = min_y(p, cube_rocks)
    same_column_ys = [p2.y for p2 in round_rocks if p2.x == p.x and p2.y >= earliest_row]
    min_row = max(same_column_ys)+1 if same_column_ys else earliest_row
    #ics(min_row)
    return Point2D(p.x, min_row)

def move_round_rocks_north(cube_rocks, round_rocks):
    new_round_positions = set()

        # process rocks with lowest y first
    for p in sorted(round_rocks, key = itemgetter(1)):
        new_p = move_rock_north(p, cube_rocks, new_round_positions)
        #ics(new_round_positions, new_p)
        #ics(new_p)
        new_round_positions.add(new_p)

    return new_round_positions

def determine_load(parsed, new_round_positions):
    def calc_load(p):
        return H - p.y

    H = height(parsed)
    return seq(new_round_positions).map(calc_load).sum()

def print_map(cube_rocks, round_rocks):
    #xs, ys = xs_and_ys(cube_rocks)
    #print(get_vis_map_multiline_str(xs, ys, special_chars=[("O", p.x, p.y) for p in round_rocks]))
    xs, ys = xs_and_ys(cube_rocks)
    (round_rock_min_x, round_rock_max_x), (round_rock_min_y, round_rock_max_y) = get_point_set_bounds(round_rocks)
    min_val = min(min(xs), min(ys), round_rock_min_x, round_rock_min_y)
    max_val = max(max(xs), max(ys), round_rock_max_x, round_rock_max_y)
    print(get_vis_map_multiline_str(xs, ys, min_val=min_val, max_val=max_val, special_chars=[("O", p.x, p.y) for p in round_rocks]))

def process(parsed):
    H = height(parsed)
    W = width(parsed)
    ic(W, H)
    ics(parsed)
    cube_rocks = build_points(parsed)
    round_rocks = build_points(parsed, "O")
    ic(len(cube_rocks), len(round_rocks))
    new_round_positions = move_round_rocks_north(cube_rocks, round_rocks)

    if is_sample:
        print_map(cube_rocks, new_round_positions)

    load = determine_load(parsed, new_round_positions)
    return load


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def hashable(points):
    return tuple(sorted(map(tuple, points)))

def rotate_neg_90(points, W):
    return [Point2D(W-p.y, W-p.x) for p in points]
    #return [Point2D(p.y, W-p.x) for p in points]

def rotate_90(points, W):
    return [Point2D(W-p.y-1, p.x) for p in points]
    #return [Point2D(p.y, W-p.x) for p in points]

def print_cuberock_map(cube_rocks):
    if is_sample:
        xs, ys = xs_and_ys(cube_rocks)
        print(get_vis_map_multiline_str(xs, ys))

def process2(parsed):
    def state_by_index(idx):
        return first_element(k for k, v in seen.items() if v == idx)

    def points_from_state(state):
        return seq(state).starmap(Point2D).list()

    def process_next(round_rocks):
        for r in range(4):
            cube_rocks = all_cube_rocks[r]
            round_rocks = move_round_rocks_north(cube_rocks, round_rocks)

            if 0 and idx < 3 and is_sample:
                ics(r)
                if r:
                    print("moved orientation")
                    print_map(cube_rocks, round_rocks)
                use_round_rocks = round_rocks

                    # rotate 0-3 times to return to original orientation for display
                for _ in range((4-r) % 4):
                    use_round_rocks = rotate_90(use_round_rocks, W)

                print_map(all_cube_rocks[0], use_round_rocks)

            round_rocks = rotate_90(round_rocks, W)
            #W, H = H, W

        if 0 and idx < 3 and is_sample:
            ics(idx, "====== oriented =======")
            print_map(all_cube_rocks[0], round_rocks)

        return round_rocks

    def generator(round_rocks):
        for idx in range(cycles):
            #ics(idx)
            round_rocks = process_next(round_rocks)
            yield hashable(round_rocks)


    H = height(parsed)
    W = width(parsed)
    assert W == H
    cube_rocks = build_points(parsed)
    round_rocks = build_points(parsed, "O")
    seen = { }
    cycles = 1000000000
        # cube rocks don't move, so precalc positions
    #print_cuberock_map(cube_rocks)
    all_cube_rocks = [cube_rocks]
    cube_rocks = rotate_90(cube_rocks, W)
    #print_cuberock_map(cube_rocks)
    all_cube_rocks.append(set(cube_rocks))
    cube_rocks = rotate_90(cube_rocks, W)
    #print_cuberock_map(cube_rocks)
    all_cube_rocks.append(set(cube_rocks))
    cube_rocks = rotate_90(cube_rocks, W)
    #print_cuberock_map(cube_rocks)
    all_cube_rocks.append(set(cube_rocks))
    #ics(all_cube_rocks)

    if 1:
        last_state = predict(generator(round_rocks), cycles)
        final_round_rocks = points_from_state(last_state)
    else:
            # each cyle rotates all 4 directions
        for idx in range(cycles):
            #ics(idx)
            round_rocks = process_next(round_rocks)
            new_state = hashable(round_rocks)

            if new_state in seen:
                break

            seen[new_state] = idx

        first_idx_of_cycle = seen[new_state]

        if 0 and is_sample:
            ics(idx+1, "=============")
            print_map(all_cube_rocks[0], process_next(round_rocks))
            ics(first_idx_of_cycle+1, "=============")
            print_map(all_cube_rocks[0], points_from_state(state_by_index(first_idx_of_cycle+1)))

        #ics(state_by_index(idx+1), state_by_index(first_idx_of_cycle+1))
        assert hashable(process_next(round_rocks)) == state_by_index(first_idx_of_cycle+1)
        cycle_length = idx - first_idx_of_cycle
        final_cycle_idx = (cycles - 1 - first_idx_of_cycle) % (cycle_length) + first_idx_of_cycle
        ic(idx, first_idx_of_cycle, cycle_length, final_cycle_idx)
        final_round_rocks = points_from_state(state_by_index(final_cycle_idx))

    if is_sample:
        #ics(idx, "====== final =======")
        ics("====== final =======")
        print_map(all_cube_rocks[0], final_round_rocks)

    load = determine_load(parsed, final_round_rocks)
    return load


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
part2(sample_data2)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)
