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
import os
import sys
from collections import *
import re
import math

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils, pathfinding_redblob
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module
import utils.pathfinding_redblob as pf

# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
example

# %%
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0]
sample_data2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""
sample_data1s = [sample_data1, sample_data2]

# %%
for sample in sample_data1s:
    print(sample)
    print("=======================")


# %% [markdown]
# # Parse

# %%
def parse_data(inp):
    return inp.strip().split("\n")


# %% [markdown]
# # Process

# %%
def is_turn(p1, p2, p3):
    diff1 = subtract_tuple(p2, p3)
    diff2 = subtract_tuple(p1, p2)
    return diff1 != diff2

class MazeGrid(pf.SquareGrid):
    def __init__(self, width: int, height: int, came_from: dict):
        super().__init__(width, height)
        self.came_from = came_from

    def cost(self, from_id: pf.Location, to_id: pf.Location) -> float:
        diff1 = subtract_tuple(from_id, to_id)
        prev = self.came_from.get(from_id)

        if prev is None:
            return 1
            
        diff2 = subtract_tuple(prev, from_id)
        #ics(prev, from_id, to_id, diff1, diff2)
        return 1 if diff1 == diff2 else 1001
        
def setup(parsed):
    W, H = width_height(parsed)
    start_pos = first(get_char_coords(parsed, "S"))
    end_pos = first(get_char_coords(parsed, "E"))
    came_from = dict()
    grid = MazeGrid(W, H, came_from)
    walls = grid.walls = set(get_char_coords(parsed, "#"))
    return grid, start_pos, end_pos, came_from

def process(parsed):
    #ics(parsed)
    grid, start_pos, end_pos, came_from = setup(parsed)
    came_from, cost_so_far, current = pf.a_star_search(grid, start_pos, end_pos, came_from=came_from)
    if 0:
        path = pf.reconstruct_path(came_from, start_pos, end_pos)
        #ics(path)
        special_chars = [(graph_char_circle_cross, x, y) for x, y in path] + [(graph_char_bullseye, end_pos[0], end_pos[1])]
        print(get_vis_map_multiline_str(map_list(itemgetter(0), grid.walls), map_list(itemgetter(1), grid.walls), special_chars=special_chars, filled_char=graph_char_light_block, blank_char=graph_char_small_dot))
    ics(cost_so_far[end_pos])
    return cost_so_far[end_pos]


# %%
#implementing with compelx numbers 
class MazeGridComplex(pf.ComplexDictGrid):
    def __init__(self, points, came_from: dict):
        super().__init__(points)
        self.came_from = came_from

    def cost(self, from_id: pf.Location, to_id: pf.Location) -> float:
        diff1 = from_id - to_id
        prev = self.came_from.get(from_id)

        if prev is None:
            return 1
            
        diff2 = prev - from_id
        #ics(prev, from_id, to_id, diff1, diff2)
        return 1 if diff1 == diff2 else 1001

def turn_cost():
    return 1000 if is_turn(p1, p2, p3) else 0

def process(parsed):
    #ics(parsed)
    W, H = width_height(parsed)
    start_pos = first(build_complex_points(parsed, sig_char="S"))
    end_pos = first(build_complex_points(parsed, sig_char="E"))
    points = dict((p, c) for p, c in build_complex_points_dict(parsed).items() if c != "#")
    came_from = dict()
    grid = MazeGridComplex(points, came_from)
    came_from, cost_so_far, current = pf.a_star_search(grid, start_pos, end_pos, came_from=came_from)
    ics(cost_so_far[end_pos])
    return cost_so_far[end_pos]


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %%
def step_cost(a, b, c):
    diff1 = subtract_tuple(b, c)
    diff2 = subtract_tuple(a, b)
    return 1 if diff1 == diff2 else 1001
    
def calc_cost(path):
    return sum(starmap(step_cost, triplewise(path)))+1

def sign(n):
    return 1 if n > 0 else -1 if n < 0 else 0
    
def tuple_sign(t):
    return tuple(sign(a) for a in t)

class ReducedGrid(pf.ReducedGraph):
    def __init__(self, junctions: dict, came_from: dict):
        super().__init__(junctions)
        self.came_from = came_from
        
    def heuristic(self, id: pf.Location, goal: pf.Location) -> float:
        (x1, y1, *_) = id
        (x2, y2, *_) = goal
        return abs(x1 - x2) + abs(y1 - y2)
    if 0:
        def __init__(self, width: int, height: int, came_from: dict):
            super().__init__(width, height)
            self.came_from = came_from
    
        #def passable(self, from_id: pf.GridLocation, id: pf.GridLocation) -> bool:
        #    return id not in self.walls and id != self.came_from.get(from_id)
        
    def cost(self, from_id: pf.Location, to_id: pf.Location) -> float:
        base_cost = self.junctions[from_id][to_id]
        
        prev = self.came_from.get(from_id)

        if prev is None:
            return base_cost
            
        diff1 = tuple_sign(subtract_tuple(from_id, to_id))
        diff2 = tuple_sign(subtract_tuple(prev, from_id))
        #ics(prev, from_id, to_id, diff1, diff2)
        return base_cost if diff1 == diff2 else 1000 + base_cost

# determine corners, calc cost 

def process2(parsed):
    grid, start_pos, end_pos, came_from, cost_so_far = setup(parsed)
    points_dict = build_tuple_points_dict(parsed)

    def is_juncture(pt, ct):
        if ct == "#":
            return False
            
        neighbors = list(m for m in movements if (c := points_dict[(p := add_tuple(pt, m))]) != "#")
        #ics(pt, ct, neighbors)
        #assert len(neighbors) != 4
        if (nl := len(neighbors)) == 2:
            added = add_tuple(*neighbors)
            #ics(added)
            return added[0] and added[1]
            
        return nl > 2
        
    corners = set([p for p, c in points_dict.items() if is_juncture(p, c)] + [start_pos, end_pos])
    #ics(parsed)
    special_chars = [(graph_char_circle_cross, x, y) for x, y in corners]
    print(get_vis_map_multiline_str(map_list(itemgetter(0), grid.walls), map_list(itemgetter(1), grid.walls), special_chars=special_chars, filled_char=graph_char_light_block, blank_char=graph_char_small_dot))
    #ics(corners)

    #costs = dict()
    costs = defaultdict(dict)
    #cost_so_far = dict()
    
    def is_goal_corner(current, goal):
        if current != start_node and current in corners:
            #costs[start_node, current] = cost_so_far[current]
            end_nodes.append(current)
            return pf.GOAL_RES_SKIP
    
    for start_node in corners:
        end_nodes = []
        #came_from, cost_so_far, current = pf.dijkstra_search(grid, start_node, goal=None, is_goal = is_goal, cost_so_far = cost_so_far)
        came_from, current = pf.breadth_first_search(grid, start_node, goal=None, is_goal = is_goal_corner)
        #    ic(start)
        #ics(start_node, end_nodes)

        for end_node in end_nodes:
            path = pf.reconstruct_path(came_from, start_node, end_node)
            #ics(end_node, path, calc_cost(path))
            #costs[start_node][end_node] = calc_cost(path)
            costs[start_node][end_node] = len(path) - 1

    ics(costs)

    came_from = dict()
    graph = ReducedGrid(costs, came_from)

    if 0:
        # this demonstrates that we can get teh same value with our reduced graph
        came_from, cost_so_far, current = pf.a_star_search(graph, start_pos, end_pos, came_from=came_from)
        #ics(start_pos, end_pos, cost_so_far, came_from)
        ic(cost_so_far[end_pos])

    if 1:
        def reduced_cost(path):
            return sum(costs[a][b] for a, b in pairwise(path))

        # stop this branch if cost gets hihigher than best
        def is_goal_cost(current, path, goal):
            if reduced_cost(path) > best_len:
                return pf.GOAL_RES_SKIP
                
            return current == goal
        
        path = pf.reconstruct_path(came_from, start_pos, end_pos)
        ics(calc_cost(path))
        best_len = cost_so_far[end_pos]
        ics(best_len)
        final_paths = pf.breadth_first_search_all_paths(graph, start_pos, end_pos, is_goal = is_goal_cost)
        nodes = set()
        #ics(sorted(map_list(calc_cost, final_paths)))

        def step_cost2(a, b, c):
            base_cost = costs[b][c]
            diff1 = tuple_sign(subtract_tuple(b, c))
            diff2 = tuple_sign(subtract_tuple(a, b))
            #ics(a, b, c, base_cost, diff1, diff2)
            return base_cost if diff1 == diff2 else 1000 + base_cost

        def calc_cost2(path):
            return costs[path[0]][path[1]] + sum(starmap(step_cost2, triplewise(path)))

            # we know it will always be a straight line
        def plot_path(a, b):
            diff = subtract_tuple(b, a)
            #diff = subtract_tuple(a, b)
            step = tuple_sign(diff)
            node = a

            while node != b:
                yield node
                node = add_tuple(node, step)
            yield b                

        for path in final_paths:
            if ics(calc_cost2(path)) == best_len:
                for a, b in pairwise(path):
                    nodes.update(plot_path(a, b))

        special_chars = [(graph_char_circle_cross, x, y) for x, y in nodes]
        print(get_vis_map_multiline_str(map_list(itemgetter(0), grid.walls), map_list(itemgetter(1), grid.walls), special_chars=special_chars, filled_char=graph_char_light_block, blank_char=graph_char_small_dot))
        return len(nodes)


# %% [markdown]
# # Process2

# %%
# yield possible paths recursively
def reconstruct_paths(came_from: dict[pf.Location, pf.Location], start: pf.Location, goal: pf.Location, equal_branches, max_length: int = 0, level = 0, start_path = []) -> list[pf.Location]:
    current: pf.Location = goal
    path: list[pf.Location] = start_path[:]
    length = len(path)
    #ics(level, start, goal, length, path)

    if not max_length:
        max_length = len(came_from) # always check length to avoid possible infinite loops

    while current != start and length < max_length:
        path.append(current)

        for from_node in equal_branches.get(current, []):
            if from_node not in path:
                for other_path in reconstruct_paths(came_from, start, from_node, equal_branches, max_length, level+1, path):
                    #ics(current, came_from[current], from_node, path, other_path)
                    yield other_path
        
        current = came_from[current]
        length += 1

    if start is not None:
        path.append(start) # optional
    else:
        raise Exception(f"start postion {start} not found!")

    path.reverse() # optional
    yield path

def process2(parsed):
    # modified to track equal branch points
    def a_star_search(graph: pf.WeightedGraph, start: pf.Location, goal: pf.Location, is_goal = None, cost_so_far = None, came_from = None, callback_step: int=1, callback=None):
        frontier = pf.PriorityQueue()
        frontier.put(start, 0)
        if came_from is None: came_from: dict[pf.Location, Optional[pf.Location]] = {}
        came_from[start]=None
        if cost_so_far is None: cost_so_far: dict[pf.Location, float] = {}
        cost_so_far[start] = 0
        equal_branches = defaultdict(set)
        iterations = 0
        is_goal = is_goal or getattr(graph, "is_goal", operator.eq)
        found_cost = -1
    
        while not frontier.empty():
            iterations += 1
            current: pf.Location = frontier.get()
            #ic(iterations, current)
            current_cost = cost_so_far[current]

                # allow alternate same cost paths to reach goal - second sample didn't work wihtout this, but oddly actual data did
            if found_cost > 0 and current_cost > found_cost:
                break
    
            if (goal_res := is_goal(current, goal)) == pf.GOAL_RES_SKIP:
                continue
            elif goal_res:
                #ic("Reached goal", current, goal)
                found_cost = current_cost
                continue
    
            neighbors = list(graph.neighbors(current, came_from))
    
            for next in neighbors:
                new_cost = current_cost + graph.cost(current, next)
    
                if next not in cost_so_far or new_cost < (next_cost := cost_so_far[next]):
                    cost_so_far[next] = new_cost
                    priority = new_cost + graph.heuristic(next, goal)
    #                ic("    ", next, new_cost, priority)
                    frontier.put(next, priority)
                    came_from[next] = current
                elif len(list(graph.neighbors(next, came_from))) > 2: # track alternate paths, only relevant when more than one neighbor
                        # don't put backtracks in
                    if next != came_from[current]:
                        equal_branches[next].add(current)
    
        return came_from, cost_so_far, current, equal_branches
    
    grid, start_pos, end_pos, came_from = setup(parsed)
    came_from, cost_so_far, current, equal_branches = a_star_search(grid, start_pos, end_pos, came_from=came_from)
    #came_from, cost_so_far, current, equal_branches = dijkstra_search(grid, start_pos, end_pos, came_from=came_from)
    path = pf.reconstruct_path(came_from, start_pos, end_pos)
    #ics(path)
    ic(len(path))
    best_len = cost_so_far[end_pos]
    ics(best_len)
    special_chars = [(graph_char_circle_cross, x, y) for x, y in path] + [(graph_char_bullseye, end_pos[0], end_pos[1])]
    print(get_vis_map_multiline_str(map_list(itemgetter(0), grid.walls), map_list(itemgetter(1), grid.walls), special_chars=special_chars, filled_char=graph_char_light_block, blank_char=graph_char_small_dot))
    #pf.draw_grid(grid, point_to=came_from, start=start_pos, path=path, goal=end_pos)
    #ics(equal_branches)
    count_nodes = set(path)
    holy_nodes = set(path)
    #ics(holy_nodes)

    for n, chk_path in enumerate(reconstruct_paths(came_from, start_pos, end_pos, equal_branches)):
        if calc_cost(chk_path) == best_len:
            count_nodes.update(chk_path)

    #ics(count_nodes)
    special_chars = [(graph_char_circle_cross, x, y) for x, y in count_nodes] + [(graph_char_bullseye, end_pos[0], end_pos[1])]
    print(get_vis_map_multiline_str(map_list(itemgetter(0), grid.walls), map_list(itemgetter(1), grid.walls), special_chars=special_chars, filled_char=graph_char_light_block, blank_char=graph_char_small_dot))
    
    return len(count_nodes)


# %%
def part2(inp):
    parsed = parse_data(inp)
    result = process2(parsed)
    print_result(result)


# %%
# idea taken from  https://old.reddit.com/r/adventofcode/comments/1hfboft/2024_day_16_solutions/m2ep953/
# "For part 2 I had Dijkstra return a dict of positions to distance from starting node. Then I used that a node lies on an optimal path if the distance from the start to the node plus the distance from the end to the node equals the distance from the start to the end"
# trickiest part was detecting a turn occurring immediately before/after a node, as the cost of the turn would'nt be included in either direction
def process2(parsed):
    def turn_at_node_cost(p1, p2, p3):
        if p1 is None or p3 is None or not is_turn(p1, p2, p3):
            return 0
        return 1000                    
        
    grid, start_pos, end_pos, came_from = setup(parsed)
    came_from_start, cost_so_far_start, _ = pf.a_star_search(grid, start_pos, end_pos, came_from = grid.came_from)
    grid.came_from = dict()
    came_from_end, cost_so_far_end, _ = pf.a_star_search(grid, end_pos, start_pos, came_from = grid.came_from)
    #ics(cost_so_far_end[start_pos], cost_so_far_start[end_pos])
    best_cost = cost_so_far_start[end_pos]
    assert cost_so_far_end[start_pos] == best_cost
    mathing_points = set((p for p, cost in cost_so_far_start.items() if cost + cost_so_far_end.get(p,1000000) + turn_at_node_cost(came_from_start.get(p), p, came_from_end.get(p)) == best_cost))
    return len(mathing_points)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

for sample_data1 in sample_data1s:
    part1(sample_data1)

for sample_data1 in sample_data1s:
    part2(sample_data1)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp) # answers in sample data were 1000 too high
part2(real_inp) # 65436 is not the right answer, too high

# %% [markdown]
# # Others' solutions

# %%
