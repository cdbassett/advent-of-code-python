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

import numpy as np
from scipy.ndimage import generic_filter, correlate
from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils, pathfinding_redblob
from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module
from pathfinding_redblob import *

# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0]
sample_data2 = \
"""             Z L X W       C
             Z P Q B       K
  ###########.#.#.#.#######.###############
  #...#.......#.#.......#.#.......#.#.#...#
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###
  #.#...#.#.#...#.#.#...#...#...#.#.......#
  #.###.#######.###.###.#.###.###.#.#######
  #...#.......#.#...#...#.............#...#
  #.#########.#######.#.#######.#######.###
  #...#.#    F       R I       Z    #.#.#.#
  #.###.#    D       E C       H    #.#.#.#
  #.#...#                           #...#.#
  #.###.#                           #.###.#
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#
CJ......#                           #.....#
  #######                           #######
  #.#....CK                         #......IC
  #.###.#                           #.###.#
  #.....#                           #...#.#
  ###.###                           #.#.#.#
XF....#.#                         RF..#.#.#
  #####.#                           #######
  #......CJ                       NM..#...#
  ###.#.#                           #.###.#
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#
  #.....#        F   Q       P      #.#.#.#
  ###.###########.###.#######.#########.###
  #.....#...#.....#.......#...#.....#.#...#
  #####.#.###.#######.#######.###.###.#.#.#
  #.......#.......#.#.#.#.#...#...#...#.#.#
  #####.###.#####.#.#.#.#.###.###.#.###.###
  #.......#.....#.#...#...............#...#
  #############.#.#.###.###################
               A O F   N
               A A D   M                     """
sample_data2 = pad_multiline_string(sample_data2)
#print(sample_data2.replace(" ", "+"))

# %% [markdown]
# # Parse

# %%
def parse_data(inp):
    return build_numpy_array_from_string_graph(inp)


# %% [markdown]
# # Process

# %% [markdown]
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.generic_filter.html#scipy.ndimage.generic_filter
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.correlate.html

# %%
A_ord = ord("A")
Z_ord = ord("Z")
period = ord(".")
ic(period)

def upper_ords_to_string(num):
    vals = (num // 100) % 100, num % 100, num // 10000
    #ics(num, vals)
    s= sjoin(chr(n) for n in vals if n)
    return s if len(s) == 2 else None

upper_ords_to_string_v = np.vectorize(upper_ords_to_string)
original_method = False
#original_method = True

if original_method: # these are both performed with correlate plus some additional filterign afterwards, should perform much better
    # assuming all that is in array is zeros or ord of upper case letters
    # place a numeric value that indicate the 2 letter label in each of the positions it occupies
    def build_labels(image):
        #ics(image)
        #print(image)
        c = image[4]
        return (image[1]+image[3])*100 + c + (image[5]+image[7])*10000 if c else 0

    # if a location is a period and has a label adjacent, place that label in the period's location
    def place_labels(image):
        c = image[4]
        return sum(n for n in image[1:8:2] if n != period) if c==period else 0

def setup(parsed):
    #ics(parsed)
    walls = np.argwhere(parsed != ".")
    empty_idx = np.nonzero(parsed == ".")
    empty = np.argwhere(parsed == ".")
    #ics(np.argwhere(np.char.isupper(parsed)))
    as_ord_upper = np.zeros(parsed.shape, dtype=np.int32)
    upp_locs = np.char.isupper(parsed)
    as_ord_upper[upp_locs] = parsed.view(np.int32)[upp_locs] # tricky, view to array that acts like ord was applied to all
    #ics(as_ord_upper)
    if original_method:
        label_nums = generic_filter(as_ord_upper, build_labels, size=(3,3), mode="constant", cval=0) # every element is result of filter_func
    else:
        # these correlate operations make every entry in output a sum of products
        kernel = [[0, 100, 0],[100, 1, 10000],[0, 10000, 0]]
        label_nums = correlate(as_ord_upper, kernel, mode="constant", cval=0)
        label_nums[label_nums % 100 == 0] = 0 # remove entries where central char was not present

    #print_sample(build_string_from_numpy_int_array(1* (label_nums.T > 0), " #"))

    if original_method:
        label_nums[empty_idx] = period
        final_label_nums = generic_filter(label_nums, place_labels, size=(3,3), mode="constant", cval=0)
    else:
        kernel = [[0, 1, 0],[1, 0, 1],[0, 1, 0]]
        final_label_nums = correlate(label_nums, kernel, mode="constant", cval=0)
        final_label_nums[parsed != "."] = 0 # remove entries where central position was not a period

    #print_sample(build_string_from_numpy_int_array(1* (final_label_nums.T > 0), " #"))
    #ics(final_label_nums)
    labels_arr = upper_ords_to_string_v(final_label_nums)
    label_locs = labels_arr != None

    if 0 and is_sample:
        diag = np.char.add(parsed, " ")
        diag[label_locs] = labels_arr[label_locs]
        print_sample(build_string_from_numpy_string_array(diag.T))

    #ics(labels, labels_arr)
    #ics(labels_arr)
    label_points = maplist(tuple, np.argwhere(labels_arr))
    labels_idx = np.nonzero(label_locs)
    labels = labels_arr[labels_idx]
    #ics(label_points, labels)
    #ics(list(zip(labels, label_points)))
    #grid = SquareGrid(len(parsed[0]), len(parsed)) # we look at grid transposed so x comes before y
    grid = SquareGrid(len(parsed), len(parsed[0])) # we look at grid transposed so x comes before y
    grid.walls = set(map(tuple, walls))
    nodes = maplist(tuple, walls)
    junction_nodes = dijkstra_reduced_node_connections(grid, label_points, nearest_neighbors_only=True)
    return labels, label_points, junction_nodes

def process(parsed):
    labels, label_points, junction_nodes = setup(parsed)

    if 0:
        portal_dict = dict(zip(label_points, labels))
        #junction_nodes_by_portal = convert_junction_keys(junction_nodes, portal_dict.__getitem__)
        junction_nodes_by_portal = convert_junction_keys(junction_nodes, lambda k: (portal_dict[k], k))
        ics(junction_nodes_by_portal)

    portal_locations = defaultdict(list) # label -> list of points (2)

    for label_point, label in zip(label_points, labels):
        portal_locations[label].append(label_point)

    # set up junctions between portal pairs
    # each portal occurs twice (AA and ZZ don't but aren't portals)
    for label, points in portal_locations.items():
        if len(points) == 2:
            lp1, lp2 = points
            junction_nodes[lp1][lp2] = 1 # moving across a portal costs 1
            junction_nodes[lp2][lp1] = 1

    #ics(junction_nodes)
    graph = ReducedGraph(junction_nodes)
    start = portal_locations["AA"][0]
    goal = portal_locations["ZZ"][0]
    came_from, cost_so_far, current = dijkstra_search(graph, start, goal)
    return cost_so_far[goal]


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
# nodes contain level
@dataclass
class ReducedRecursiveGraph:
    junctions: dict # id -> dict(id) (id -> cost) (such as returned from dijkstra_reduced_node_connections)

    def neighbors(self, id: GridLocation, came_from: dict[Location, Optional[Location]]) -> Iterator[GridLocation]:
        label, level = id
        base_label = label[:2]
        keys = self.junctions[label].keys()

        if level:
            neighbors = [(key, level) for key in keys if key not in ("AAo", "ZZo")]
        else:
            neighbors = [(key, level) for key in keys if key in ("AAo", "ZZo") or key[-1] != "o"]

        if label[-1] == "i":
            # go from inside of current level to outside of next level
            neighbors.append((base_label + "o", level+1))
        elif level:
            # go from outside of current level to inside of previous level, but not on first level
            neighbors.append((base_label + "i", level-1))

        return neighbors

        # based on the assumption that to_id is a neighbor of from_id
    def cost(self, from_id: Location, to_id: Location) -> float:
        # if trnasitioning between inner and outer, cost is 1, otherwise previously calculated
        return 1 if from_id[-1] != to_id[-1] else self.junctions[from_id[0]][to_id[0]]

# first level is special because outer nodes are removed, AA and ZZ are present
# every other inner level outer nodes connect to inner nodes of outer level and vice versa, AA and ZZ are not present
def process2(parsed):
    def callback(cbi):
        ics(cbi.iterations, cbi.current, cbi.neighbors, cbi.queue_len)
        #return iterations > 50

    labels, label_points, junction_nodes = setup(parsed)
        # we need to know whether portals are inner or outer
    W, H, min_x, min_y, max_x, max_y = analyze_points(label_points)
    inside_x_range = range(min_x+1, max_x)
    inside_y_range = range(min_y+1, max_y)
    if 0:
        inside_portals, outside_portals = seq(zip(labels, label_points)).partition(lambda x: x[1][0] in inside_x_range and x[1][1] in inside_y_range)
        ics(inside_portals, outside_portals)
    inside_portals, outside_portals = seq(label_points).partition(lambda x: x[0] in inside_x_range and x[1] in inside_y_range)
    inside_portals, outside_portals = set(inside_portals), set(outside_portals)
    #ics(len(labels), len(label_points), len(inside_portals), len(outside_portals), len(inside_portals)+len(outside_portals))

    base_portal_dict = dict(zip(label_points, labels)) # point -> base label
    junction_nodes_by_inside_outside = convert_junction_keys(junction_nodes, lambda k: (base_portal_dict[k] + "oi"[int(k in inside_portals)]))
    if 0:
        ics(junction_nodes, junction_nodes_by_inside_outside)
        io_portal_dict = dict((v+"oi"[int(k in inside_portals)], k) for k, v in base_portal_dict.items()) # io label -> point
        ics(io_portal_dict)

    graph = ReducedRecursiveGraph(junction_nodes_by_inside_outside)
    start = "AAo", 0
    goal = "ZZo", 0
    came_from, cost_so_far, current = dijkstra_search(graph, start, goal, callback=callback, callback_step=100)

    if current == goal:
        return cost_so_far[goal]


# %%
def part2(inp):
    parsed = parse_data(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

if 0:
    for sample_data1 in sample_data1s:
        #part2(sample_data1)
        part1(sample_data1)

for sd2 in [sample_data1s[0], sample_data2]:
    part2(sd2)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)

# %% [markdown]
# # Others' solutions
