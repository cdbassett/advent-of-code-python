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
from dataclasses import dataclass

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, pathfinding_redblob
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module
import utils.pathfinding_redblob as pathfinding_redblob

# %% [markdown]
# # Parse

# %%
#node = namedtuple("Node","x,y,size,used,avail,useperc")
node = namedtuple("Node","name,x,y,size,used")

if 0:
    @dataclass
    class node:
        x: int
        y: int
        size: int
        used: int

        @property
        def avail(self):
            return self.size - self.used

        if 0:
                # act liek a tuple
            def __len__(self):
                return 4

            def __getitem__(self, index):
                return self.tup[index]

def make_node(line):
    ltr = chr(ord("A") + line[1])
    return node(*([f"{ltr}{line[0]}"] + line[:-2]))

def parse(inp):
    return seq(string_to_integers(inp)).map(make_node).list()


# %%
sample_data2 = """
Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%"""


# %% [markdown]
# # Process

# %%
def viable(from_node, to_node):
    #return from_node.used and to_node.avail >= from_node.used
    return from_node.used and (to_node.size - to_node.used) >= from_node.used

def viable_pair(node_pair):
    return viable(*node_pair)

def process(parsed):
    return seq(parsed).permutations(2).count(viable_pair)


# %%
def part1(inp):
    parsed = parse(inp)
    ic(len(parsed))
    result = process(parsed)
    print_result(result)

# %% [markdown]
# # Process2

# %% editable=true slideshow={"slide_type": ""}
# also checks if a neighbor
def true_viable(from_node, to_node):
    #return from_node.used and to_node.avail >= from_node.used and abs(from_node.x - to_node.x) == 1 and abs(from_node.y - to_node.y) == 1
    return from_node.used and (to_node.size - to_node.used) >= from_node.used and abs(from_node.x - to_node.x) == 1 and abs(from_node.y - to_node.y) == 1

# just want to return all possible next states
# DOES NOT need to have anything to do with passed node, other than what it did to change overall state (i.e. moved data from one node to another)
# state contains current storage of all nodes (possibly sparse, i.e. only when different from initial)
@dataclass
class ClusterGrid(pathfinding_redblob.Graph):
    nodes_by_x_y: dict
    node_neighbors: dict

    def neighbors(self, id: pathfinding_redblob.Location, came_from: dict[pathfinding_redblob.Location, Optional[pathfinding_redblob.Location]]) -> list[pathfinding_redblob.Location]:
        def get_node_used(x, y):
            return dct.get((x, y), self.nodes_by_x_y[x, y])
            #return id.get((node.x, node.y), node.used)

        #def get_node_avail(node):
        #    return node.size - get_node_used(node)

        # dict is x, y -> node whose data it is now holding
        dct = dict(id) # convert from hashable to dict

        # this is expression when nothing has moved yet
        #return [id for node, neighbors in node_neighbors.items() for nb in neighbors if node.used and nb.avail >= from_node.used]
        #return [dict_without(id, (nb.x, nb.y)) | {}  for node, neighbors in node_neighbors.items() for nb in neighbors if node.used and nb.avail >= from_node.used]
        if 1: # convert from dict to hashable
            #return [tuple(dict_without_key(dct | {(nb.x, nb.y): nu, (node.x, node.y): 0}).items())  # neighbor gets node's used added, node get used set to 0
            result = [tuple(sorted(((x,y), nd) for (x,y), nd in (dct | {(nb.x, nb.y): nu, (x, y): nbu}).items() if (x,y)!=(nd.x,nd.y) ) )  # neighbor get node's used added, node get used set to 0
                    for (x, y), neighbors in self.node_neighbors.items()
                    for nb in neighbors
                        if (nu := get_node_used(x, y)).used and (nbu := get_node_used(nb.x, nb.y)).used == 0]
            #ics(len(result))
            return result
        #else: # this is the general-use case, we will instead assume only use of completely empty node is applicable
        #    return [id | {(nb.x, nb.y):  nb.used+node.used, (node.x, node.y): 0}  # neighbor get node's used added, node get used set to 0
        #            for node, neighbors in self.node_neighbors.items()
        #            for nb in neighbors if get_node_avail(nb) >= get_node_used(node) > 0]


def process2(parsed):
    # a is state, b is goal
    def is_goal(a, b):
        return dict(a).get((0,0)) == b # top-left node contains contents of top-right node

    #ic(parsed[:2])
    ic(len(parsed))
    #max_x = seq(parsed).max_by(itemgetter(0))
    #max_y = seq(parsed).max_by(itemgetter(1))
    max_x = seq(parsed).max_by(lambda a: a.x)
    max_y = seq(parsed).max_by(lambda a: a.y)
    ic(max_x, max_y)
    H = max_y.y+1
    W = max_x.x+1
    ic(W, H, W*H)
    assert len(parsed) == W*H # we're assuming we have a rectangle with every entry filled
    nodes_by_x_y = dict(((node.x, node.y), node) for node in parsed)
    #ics(nodes_by_x_y)
    empty_node = first_element(node for node in parsed if not node.used)
    ic(empty_node)
    #can_move_other_than_empty = seq(parsed).filter(lambda node: node != empty_node and viable(node, empty_node)).len()
    #ic(can_move_other_than_empty)
    node_neighbors = dict(((node.x, node.y), [nb for x, y in [(0, 1), (0, -1), (1, 0), (-1, 0)] if (nb := nodes_by_x_y.get((node.x + x, node.y + y)))]) for node in parsed)
    #ics(node_neighbors)

    #immediate_viable_nodes = seq(parsed).filter(lambda node: node != max_x).filter(partial(viable, max_x)).list()
    #ic(immediate_viable_nodes)
    #viable_nodes = seq(parsed).filter(lambda node: node != max_x).filter(partial(viable, max_x)).list()
    #viable_nodes = seq(parsed).permutations(2).starfilter(true_viable).list()
    #ic(viable_nodes)

    walls = seq(parsed).filter(lambda node: node != empty_node and not viable(node, empty_node)).map(lambda node: Point2D(node.x, node.y)).set()
    #ic(walls)
    xs, ys = xs_and_ys(walls)
    # , max_val=max(W,H)
    # finally solved by printing out map of walls and counting on it
    print(get_vis_map_multiline_str(xs, ys, min_val=0, special_chars=[("G", 0, 0), ("D", W-1, 0), ("O", empty_node.x, empty_node.y)]))

    #came_from, cost_so_far, final = pathfinding_redblob.a_star_search(grid, start, goal, is_goal = lambda a, b: a[:2] == b[:2])
    def callback(cbi):
        if iterations > 1000:
            raise Exception("Stopping to investigate")
        if 1:
        #if iterations % 100 == 0 or current[:2] in (callback_locations):
        #if 0 and current[:2] in (callback_locations):
            #use_goal = first(k for k, v in came_from.items() if k[:2] == current[:2])
            ics(cbi.iterations, cbi.current, cbi.queue_len)
            #ics(iterations, current, cost_so_far[current], len(came_from), queue_len, neighbors)
            #draw_grid(grid, came_from, start, current)

    grid = ClusterGrid(nodes_by_x_y, node_neighbors)
    start = tuple() # start with nothing changed
    goal = nodes_by_x_y[(0, 0)]
    goal = nodes_by_x_y[(W-1, 0)]
    ic(goal)
    if 0:
        came_from, cost_so_far, final = pathfinding_redblob.dijkstra_search(grid, start, goal, is_goal = is_goal, callback_step=100, callback=callback if is_sample else None)

    # ended up calculating by hand
    #return cost_so_far[final]


# %%
def part2(inp):
    parsed = parse(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
part2(sample_data2)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)
