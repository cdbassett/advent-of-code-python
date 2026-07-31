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


# %% [markdown]
# # Parse

# %%
def parse_line(line):
    return string_to_integers_list(line)

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).starmap(Point2D).list()


# %% [markdown]
# # Process

# %%
point_names = string.ascii_letters

def process(parsed):
    ic(len(parsed))
    #ics(parsed)
    W, H, min_x, min_y, max_x, max_y = analyze_points(parsed)
    singles = {}
    special_chars = []
    rim_min_x, rim_max_x = min_x - 1, max_x + 1
    rim_min_y, rim_max_y = min_y - 1, max_y + 1
    x_range, y_range = range(rim_min_x, rim_max_x+1), range(rim_min_y, rim_max_y+1)

    for p in product(x_range, y_range):
        distances = sorted((manhattan(point, p), c) for c, point in zip(point_names, parsed))
        closest = "." if distances[0][0] == distances[1][0] else distances[0][1]
        singles[p] = closest
        special_chars.append((closest, p[0], p[1]))

    rim_p = list(square_boundary_points(rim_min_x, rim_min_y, rim_max_x, rim_max_y))
    #ics(rim_p)
    assert len(rim_p) == W * 2 + H * 2 + 4, f"len={len(rim_p)}, expected {W * 2 + H * 2 + 4}"
    rim_chars = seq(rim_p).lookup(singles).set()

    ics(rim_chars)

    counts = Counter(c for c in singles.values() if c not in rim_chars)
    ics(counts)

    if is_sample:
        for c, p in zip(string.ascii_uppercase, parsed):
            special_chars.append((c, p[0], p[1]))
        #print(get_vis_map_multiline_str([], [], reversed = False, min_val=None, max_val=None, special_chars= [(val, x, y) for (x, y), val in singles.items()]))
        #print(get_vis_map_multiline_str([], [], reversed = False, min_val=0, max_val=10, special_chars=special_chars))
        print(get_vis_map_multiline_str([], [], reversed = False, special_chars=special_chars))

    return counts.most_common(1)[0][1]


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %% [markdown]
# Theory:
#    rather than calculate all, find some inner bound (diamond or square) such that every point on the boundary is within limits
#    calculate the summed distances for each point. then progress outward, adding the count (1 for each starting point) as we go
#
#    scratch that. actual data results in approachable poitns all being with min and max boundary like example

# %%
def process2(parsed, max_dist):
    def summed_distance(p):
        return seq(parsed).map(partial(manhattan, p)).sum()

    point_count = len(parsed)
    ic(point_count)
    W, H, min_x, min_y, max_x, max_y = analyze_points(parsed)
    if 0:
        x_factor, y_factor = max_dist // point_count - W//2, max_dist // point_count - H//2
        x_factor, y_factor = 0, 0
        ic(x_factor, y_factor)
        start_rim_min_x, start_rim_max_x = min_x - x_factor, max_x + x_factor
        start_rim_min_y, start_rim_max_y = min_y - y_factor, max_y + y_factor
        x_range, y_range = range(start_rim_min_x, start_rim_max_x+1), range(start_rim_min_y, start_rim_max_y+1)
        rim_p = list(square_boundary_points(start_rim_min_x, start_rim_min_y, start_rim_max_x, start_rim_max_y))
        ic(start_rim_min_x, start_rim_min_y, start_rim_max_x, start_rim_max_y)

        for p in rim_p:
            dist = summed_distance(p)
            assert dist <= max_dist, f"dist={dist}, expected <= {max_dist} for {p}"

    x_range, y_range = range(min_x, max_x+1), range(min_y, max_y+1)
    # this verifies that even exactly along the border nothing meets the criteria
    #cnt = seq(square_boundary_points(min_x, min_y, max_x, max_y)).map(summed_distance).count(rpartial(operator.lt, max_dist))
    #cnt = seq(square_boundary_points(min_x+50, min_y+50, max_x-50, max_y-50)).map(summed_distance).count(rpartial(operator.lt, max_dist))
    #ic(cnt)
    cnt = seq(product(x_range, y_range)).map(summed_distance).count(rpartial(operator.lt, max_dist))
    return cnt


# %%
def part2(inp, max_dist):
    parsed = parse(inp)
    result = process2(parsed, max_dist)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

for sample_data1 in sample_data1s:
    part1(sample_data1)
# example answer is wrong for part 2, it is the answer for <=, not <
part2(sample_data2, 30)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp, 10000)
