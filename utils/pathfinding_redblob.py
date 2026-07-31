# https://www.redblobgames.com/pathfinding/a-star/implementation.html
# Sample code from https://www.redblobgames.com/pathfinding/a-star/
# Copyright 2014 Red Blob Games <redblobgames@gmail.com>
#
# Feel free to use this code in your own projects, including commercial projects
# License: Apache v2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>

from __future__ import annotations
# some of these types are deprecated: https://www.python.org/dev/peps/pep-0585/
from typing import Protocol, Iterator, Tuple, TypeVar, Optional
import operator
import sys
import functools
from collections import *
import collections
from dataclasses import dataclass, field


from icecream import ic

print("loaded pathfinding_redblob")

T = TypeVar('T')

Location = TypeVar('Location')

class Graph(Protocol):
    def neighbors(self, id: Location, came_from: dict[Location, Optional[Location]]) -> list[Location]: pass

        # based on the assumption that to_id is a neighbor of from_id
    def cost(self, from_id: Location, to_id: Location) -> float:
        return 1

        # used for a_star_search
    def heuristic(self, id: Location, goal: Location) -> float:
        return 0

        # used for dijkstra and a_star_search
    def priority(self, new_cost: float, current: Location, next: Location) -> float:
        return new_cost

    def is_goal(self, id: Location, goal: Location) -> bool:
        return id == goal


class SimpleGraph:
    def __init__(self):
        self.edges: dict[Location, list[Location]] = {}

    def neighbors(self, id: Location, came_from: dict[Location, Optional[Location]]) -> list[Location]:
        return self.edges[id]


example_graph = SimpleGraph()
example_graph.edges = {
    'A': ['B'],
    'B': ['C'],
    'C': ['B', 'D', 'F'],
    'D': ['C', 'E'],
    'E': ['F'],
    'F': [],
}


class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self) -> bool:
        return not self.elements

    def put(self, x: T):
        self.elements.append(x)

    def get(self) -> T:
        return self.elements.popleft()

    def len(self) -> int:
        return len(self.elements)

LiFoQueue = Queue

class FiFoQueue(Queue):
    def get(self) -> T:
        return self.elements.pop()


# utility functions for dealing with square grids
def from_id_width(id, width):
    return (id % width, id // width)

def base_grid_id_eq(a, b):
    return a[:2] == b[:2]

def draw_tile(graph, id, style):
    r = " . "
    if 'number' in style and id in style['number']: r = " %-2d" % style['number'][id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1, *_) = id
        (x2, y2, *_) = style['point_to'][id]
        if x2 == x1 + 1: r = " > "
        if x2 == x1 - 1: r = " < "
        if y2 == y1 + 1: r = " v "
        if y2 == y1 - 1: r = " ^ "
    if 'path' in style and id in style['path']:   r = " @ "
    if 'start' in style and id == style['start']: r = " A "
    is_goal = style.get("is_goal", operator.eq)
    if 'goal' in style and is_goal(id, style['goal']): r = " Z "
    if id in graph.walls: r = "###"
    return r

def draw_grid(graph, **style):
    print("___" * graph.width)

    for y in range(graph.height):
        for x in range(graph.width):
            print("%s" % draw_tile(graph, (x, y), style), end="")

        print()

    print("~~~" * graph.width)

# data from main article
DIAGRAM1_WALLS = [from_id_width(id, width=30) for id in [21,22,51,52,81,82,93,94,111,112,123,124,133,134,141,142,153,154,163,164,171,172,173,174,175,183,184,193,194,201,202,203,204,205,213,214,223,224,243,244,253,254,273,274,283,284,303,304,313,314,333,334,343,344,373,374,403,404,433,434]]

GridLocation = Tuple[int, int]

#@dataclass
class SquareGrid(Graph):
#    width: int
#    height: int
#    walls: set

    def __init__(self, width: int, height: int, left: int=0, top: int=0):
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.walls: list[GridLocation] = []

    def in_bounds(self, id: GridLocation) -> bool:
        x, y, *_ = id
        return self.left <= x < self.width and self.top <= y < self.height

    def passable(self, from_id: GridLocation, id: GridLocation) -> bool:
        return id not in self.walls

    def neighbors(self, id: GridLocation, came_from: dict[Location, Optional[Location]]) -> Iterator[GridLocation]:
        x, y, *_ = id
        neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)] # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0: neighbors.reverse() # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(functools.partial(self.passable, id), results)
        return results

        # based on the assumption that to_id is a neighbor of from_id
    def cost(self, from_id: Location, to_id: Location) -> float:
        return 1

    def heuristic(self, id: Location, goal: Location) -> float:
        (x1, y1, *_) = id
        (x2, y2, *_) = goal
        return abs(x1 - x2) + abs(y1 - y2)


class CubeGrid(SquareGrid):
    def __init__(self, width: int, height: int, depth: int, left: int=0, top: int=0, front: int=0):
        super().__init__(width, height, left, top)
        self.depth = depth
        self.front = front

    def in_bounds(self, id: GridLocation) -> bool:
        x, y, z, *_ = id
        return self.left <= x < self.width and self.top <= y < self.height and self.front <= z < self.depth

    def neighbors(self, id: GridLocation, came_from: dict[Location, Optional[Location]]) -> Iterator[GridLocation]:
        x, y, z, *_ = id
        neighbors = [(x+1, y, z), (x-1, y, z), (x, y-1, z), (x, y+1, z), (x, y, z-1), (x, y, z+1)]
        results = filter(self.in_bounds, neighbors)
        results = filter(functools.partial(self.passable, id), results)
        return results

    def heuristic(self, id: Location, goal: Location) -> float:
        (x1, y1, z1, *_) = id
        (x2, y2, z2, *_) = goal
        return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


# coords are complex, bounds are determined by presence in dict
# problematic for optimal path finding, complex values can't be sorted for prioirity queue
# look at heapq.heapify(heap, key=complex_compare)
class ComplexDictGrid(Graph):
    def __init__(self, points):
        self.points = points
        self.walls = set()

    def in_bounds(self, id: complex) -> bool:
        return id in self.points

    def passable(self, from_id: complex, id: complex) -> bool:
        return id not in self.walls

    def neighbors(self, id, came_from: dict[Location, Optional[Location]]) -> Iterator[GridLocation]:
        dirs = (-1, 1, -1j, 1j) # E W N S
        neighbors = [id + d for d in dirs]
        results = filter(self.in_bounds, neighbors)
        results = filter(functools.partial(self.passable, id), results)
        return results

        # based on the assumption that to_id is a neighbor of from_id
    def cost(self, from_id: complex, to_id: complex) -> float:
        return 1

    def heuristic(self, id: complex, goal: complex) -> float:
        return int(abs(id.real - goal.real) + abs(id.imag - id.imag))


class WeightedGraph(Graph):
    def cost(self, from_id: Location, to_id: Location) -> float: pass


class GridWithWeights(SquareGrid):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.weights: dict[GridLocation, float] = {}

    def cost(self, from_node: GridLocation, to_node: GridLocation) -> float:
        return self.weights.get(to_node, 1)


diagram4 = GridWithWeights(10, 10)
diagram4.walls = [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8)]
diagram4.weights = {loc: 5 for loc in [(3, 4), (3, 5), (4, 1), (4, 2),
                                       (4, 3), (4, 4), (4, 5), (4, 6),
                                       (4, 7), (4, 8), (5, 1), (5, 2),
                                       (5, 3), (5, 4), (5, 5), (5, 6),
                                       (5, 7), (5, 8), (6, 2), (6, 3),
                                       (6, 4), (6, 5), (6, 6), (6, 7),
                                       (7, 3), (7, 4), (7, 5)]}

# this is to allow using heapq with uncomparable objects like complex
# idea is to only try to compare the first element, which is the priority
class MaxTuple(tuple):
    def __lt__(self, other):
        return self[0] < other[0]

import heapq

class PriorityQueue:
    def __init__(self):
        self.elements: list[tuple[float, T]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, MaxTuple((priority, item)))

    def get(self) -> T:
        return heapq.heappop(self.elements)[1]

# =======================================================


# thanks to @m1sp <Jaiden Mispy> for this simpler version of
# reconstruct_path that doesn't have duplicate entries

def reconstruct_path(came_from: dict[Location, Location], start: Location, goal: Location, max_length: int = 0) -> list[Location]:
#    ic(start, goal, came_from)
    current: Location = goal
    path: list[Location] = []
    length = 0

    if not max_length:
        max_length = len(came_from) # always check length to avoid possible infinite loops

    if goal not in came_from: # no path was found
        return []

    while current != start and length < max_length:
        path.append(current)
        current = came_from[current]
        length += 1

    if start is not None:
        path.append(start) # optional
    #else:
    #    raise Exception(f"start position {start} not found!")

    path.reverse() # optional
    return path


# =======================================================


# for legacy use, first two value roughly correspond to true/false from old is_goal function style where only boolean was returned
(
GOAL_RES_CONTINUE,  # keep searching normally
GOAL_RES_STOP,  # goal was found, stop processing
GOAL_RES_SKIP,  # keep searching but don't process current node any further
_) = range(4)



SearchCallBackInfo = namedtuple("SearchCallBackInfo",
    "cost_so_far,came_from,current,iterations,queue_len,neighbors,path")

def dijkstra_search(graph: WeightedGraph, start: Location, goal: Location, is_goal = None, cost_so_far = None, came_from = None, callback_step: int=1, callback=None):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    if came_from is None: came_from: dict[Location, Optional[Location]] = {}
    if cost_so_far is None: cost_so_far: dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0
    iterations = 0
    is_goal = is_goal or getattr(graph, "is_goal", operator.eq)
    priority_func = getattr(graph, "priority", lambda new_cost, current, next: new_cost)

    while not frontier.empty():
        iterations += 1
        current: Location = frontier.get()

        if (goal_res := is_goal(current, goal)) == GOAL_RES_SKIP:
            continue
        elif goal_res:
            #ic("Reached goal", current, goal)
            break

        neighbors = list(graph.neighbors(current, came_from))
        current_cost = cost_so_far[current]

        if callback and not (iterations % callback_step):
            if callback(SearchCallBackInfo(cost_so_far, came_from, current, iterations, len(frontier.elements), neighbors, None)):
                break

        for next in  neighbors:
            new_cost = current_cost + graph.cost(current, next)

            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = priority_func(new_cost, current, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far, current

# =======================================================

# stops when every goal individually has been reached, not when a path that traverses all goals has been
def dijkstra_search_multi_goals(graph: WeightedGraph, start: Location, goals: set[Location], is_goal = operator.contains, callback_step: int=1, callback=None):
    goals = set(goals)

    def multi_goal(current, goal):
        if is_goal(goals, current):
            goals.remove(current)

            if not goals:
                return True
            # need to continue processing as this may be a node on the way to a different goal

        return False

    return dijkstra_search(graph, start, None, is_goal = multi_goal, callback_step=callback_step, callback=callback)

# =======================================================



# returns dict of dicts of lists: node -> node -> cost, minimum distance from every goal to every other goal
# unfortunately this includes ALL distances rather than only nodes directly reachable (without passing through other nodes)
# if nearest_neighbors_only, stop processing goal nodes once reached (don't progress past a goal, but going around it would work)
# assumes graph is bi-directional
def dijkstra_reduced_node_connections(graph: Graph, nodes: list[Location], nearest_neighbors_only=False):
    junction_nodes = defaultdict(dict)
    goals = set(nodes)

    def multi_goal(current, current_goals):
        if current in current_goals:
            current_goals.remove(current)
            neighbors.add(current)

            if not current_goals:
                return GOAL_RES_STOP

            #ic("found goal, skipping further processing on current", start, current)
            if nearest_neighbors_only:
                return GOAL_RES_SKIP # don't keep processing from this goal, we only want direct connections, not other goals through this goal
            # need to continue processing as this may be a node on the way to a different goal

        return GOAL_RES_CONTINUE

    for start in goals:
        use_goals = goals.difference([start])
        neighbors = set()
        came_from, cost_so_far, current = dijkstra_search(graph, start, use_goals, is_goal = multi_goal)
        #ic(start, neighbors, use_goals)

        for end in neighbors:
            #path = reconstruct_path(came_from, start, end)
            #cost = len(path) - 1
            cost = cost_so_far[end]
            junction_nodes[start][end] = cost
            junction_nodes[end][start] = cost

    return junction_nodes

# =======================================================

@dataclass
class ReducedGraph:
    junctions: dict # id -> dict(id) (id -> cost) (such as returned from dijkstra_reduced_node_connections)

    def neighbors(self, id: GridLocation, came_from: dict[Location, Optional[Location]]) -> Iterator[GridLocation]:
        return self.junctions[id].keys()

        # based on the assumption that to_id is a neighbor of from_id
    def cost(self, from_id: Location, to_id: Location) -> float:
        return self.junctions[from_id][to_id]


# =======================================================

if 0:
    def heuristic(a: GridLocation, b: GridLocation) -> float:
        (x1, y1, *_) = a
        (x2, y2, *_) = b
        return abs(x1 - x2) + abs(y1 - y2)

# =======================================================

# apparently astar can't be used for longest path (according to research), previously created a modified version but it didn't give correct result
def a_star_search(graph: WeightedGraph, start: Location, goal: Location, is_goal = None, cost_so_far = None, came_from = None, callback_step: int=1, callback=None):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    if came_from is None: came_from: dict[Location, Optional[Location]] = {}
    came_from[start]=None
    if cost_so_far is None: cost_so_far: dict[Location, float] = {}
    cost_so_far[start] = 0
    iterations = 0
    is_goal = is_goal or getattr(graph, "is_goal", operator.eq)

    while not frontier.empty():
        iterations += 1
        current: Location = frontier.get()
        #ic(iterations, current)

        if (goal_res := is_goal(current, goal)) == GOAL_RES_SKIP:
            continue
        elif goal_res:
            #ic("Reached goal", current, goal)
            break

        neighbors = list(graph.neighbors(current, came_from))
        current_cost = cost_so_far[current]

        if callback and not (iterations % callback_step):
            callback(SearchCallBackInfo(cost_so_far, came_from, current, iterations, len(frontier.elements), neighbors, None))

        for next in neighbors:
            new_cost = current_cost + graph.cost(current, next)

            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + graph.heuristic(next, goal)
#                ic("    ", next, new_cost, priority)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far, current


# =======================================================

def breadth_first_search(graph: Graph, start: Location, goal: Location, is_goal=None, frontier=None, callback_step: int=1, callback=None):
#    ic(start)
    if frontier is None: frontier = Queue()
    frontier.put(start)
    came_from: dict[Location, Optional[Location]] = {}
    came_from[start] = None
    iterations = 0
    is_goal = is_goal or getattr(graph, "is_goal", operator.eq)
    #ic(frontier)

    while not frontier.empty():
        iterations += 1
        current: Location = frontier.get()

        if (goal_res := is_goal(current, goal)) == GOAL_RES_SKIP:
            continue
        elif goal_res:
            #ic("Reached goal", current, goal)
            break

        #ic(current)
        neighbors = list(graph.neighbors(current, came_from))

        if callback and not (iterations % callback_step):
            if callback(SearchCallBackInfo(-1, came_from, current, iterations, len(frontier.elements), neighbors, None)):
                break

        for next in neighbors:
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current

    return came_from, current

# =======================================================
# the idea here is to serach from both directions, should be faster in many cases
# because search frontier is 2 small trees instead of one big tree
def breadth_first_search_bidirectional(graph: Graph, start: Location, goal: Location, callback_step: int=1, callback=None):
#    ic(start)
    frontier1 = Queue()
    frontier1.put(start)
    came_from1: dict[Location, Optional[Location]] = {}
    came_from1[start] = None
    org_came_from1 = came_from1
    frontier2 = Queue()
    frontier2.put(goal)
    came_from2: dict[Location, Optional[Location]] = {}
    came_from2[goal] = None
    org_came_from2 = came_from2
    iterations = 0

    while not frontier1.empty() and not frontier2.empty():
        iterations += 1

        if frontier1.len() > frontier2.len(): # expand the smaller queue first
#            ic("Swap")
            frontier1,frontier2 = frontier2,frontier1
            came_from1,came_from2 = came_from2,came_from1

        current: Location = frontier1.get()
        neighbors = list(graph.neighbors(current, came_from1))
#        ic(iterations, current, neighbors)

        if callback and not (iterations % callback_step):
            if callback(SearchCallBackInfo(-1, (came_from1, came_from2), current, iterations, len(frontier.elements), neighbors, None)):
                break

        for next in neighbors:
            if next in came_from2:
#                ic("Reached goal", current, next, goal)
                came_from1[next] = current
                return org_came_from1, org_came_from2, next

            if next not in came_from1:
                frontier1.put(next)
                came_from1[next] = current

    raise Exception("Path not found?")
    return org_came_from1, org_came_from2, next

# =======================================================
def reconstruct_path_bidirectional(came_from1: dict[Location, Location], came_from2: dict[Location, Location], start: Location, goal: Location, middle: Location) -> list[Location]:
    path1 = reconstruct_path(came_from1, start, middle)
    path2 = reconstruct_path(came_from2, goal, middle)
    path2.reverse()
    return path1 + path2[1:]


# =======================================================

# find node furthest distance from start
# to determine all distances from start, something like this can be used:
# @cache
#def calc_path_length(current):
#    return 0 if (next := came_from.get(current, 0)) is None else 1 + calc_path_length(next)

def breadth_first_count_longest(graph: Graph, start: Location):
    frontier = Queue()
    frontier.put((start, 0))
    came_from: dict[Location, Optional[Location]] = {}
    came_from[start] = None
    current: Location
    longest = 0
    end_node = None
    iterations = 0

    while not frontier.empty():
        iterations += 1
        current, cnt = frontier.get()
        neighbors = list(next for next in graph.neighbors(current, came_from) if next not in came_from)
        #ic(iterations, current, neighbors, cnt, longest)

        if not neighbors and cnt > longest:
            end_node, longest = current, cnt

        for next in neighbors:
            frontier.put((next, cnt+1))
            came_from[next] = current

    return came_from, end_node, longest


# =======================================================
# number of reachable nodes
def breadth_first_count(graph: Graph, start: Location):
    came_from, current = breadth_first_search(graph, start, None)
    return len(came_from)

# =======================================================
# if goal is provided, all paths returned end at goal
# otherwise all paths to anywhere are returned, ending when there are no more neighbors
# TODO: may be able to implement with just custom goal function
def breadth_first_search_all_paths(graph: Graph, start: Location, goal: Location, is_goal = None, check_visited = None, callback_step: int=1, callback=None):
    #ic("breadth_first_search_all_paths", start, goal)
    frontier = Queue()
    frontier.put((start, [start]))
    final_paths = []
    current: Location
    iterations = 0
    is_goal = is_goal or getattr(graph, "is_goal", lambda c, g: c == g)
    check_visited = check_visited or (lambda next, path_set: next in path_set)
#    ic(goal)

    while not frontier.empty():
        iterations += 1
        current, path = frontier.get()

        if (goal_res := is_goal(current, path, goal)) == GOAL_RES_SKIP:
            continue
        elif goal_res:
            #ic("Reached goal", current, goal)
            final_paths.append(tuple(path))
            # should break?

        #if is_goal(current, path, goal):
        #    final_paths.append(tuple(path))

        neighbors = list(graph.neighbors(current, None))

        if callback and not (iterations % callback_step):
            if callback(SearchCallBackInfo(None, None, current, iterations, len(frontier.elements), neighbors, path)):
                break

        if neighbors:
            path_set = set(path) if len(path) > 4 else path

        neighbors = list(next for next in neighbors if not check_visited(next, path_set))

        if not neighbors and not goal:
#            ic("appending")
            final_paths.append(tuple(path))

        for next in neighbors:
            frontier.put((next, path + [next]))

    return final_paths # start is included

# =======================================================


def breadth_first_search_multi_goals(graph: Graph, start: Location, goals: set[Location], first_reach_of_goals_only=False):
    frontier = Queue()
    frontier.put((start, [start]))
    final_paths = []
    current: Location
    goals = goals.copy()

    while not frontier.empty():
        current, path = frontier.get()

        if current in goals:
            final_paths.append(tuple(path))

            if first_reach_of_goals_only:
                goals.remove(current)

                if not goals:
                    break
            continue

        neighbors = list(graph.neighbors(current, None))

        if neighbors:
            path_set = set(path) if len(path) > 4 else path

        for next in neighbors:
            if next not in path_set:
                frontier.put((next, path + [next]))

    return final_paths # start is included

# =======================================================
# this does not do cost optimization, original use was for a loop where only one path from node-to node was possible
# returns list of tuples of from (from_id, to_id, cost)
def breadth_first_reduced_node_connections(graph: Graph, nodes: list[Location], callback_step: int=1):
    node_connections = []

    for start_node in nodes:
        goal_nodes = set(node for node in nodes if node != start_node)
        final_paths = breadth_first_search_multi_goals(graph, start_node, goal_nodes)
        #ic(final_paths)
        node_connections.extend((fp[0], fp[-1], len(fp)-1) for fp in final_paths)

    return set(tuple(sorted(s[:2])) + s[2:3] for s in node_connections) # start and goal are included

# =======================================================

class SquareGridNeighborOrder(SquareGrid):
    def neighbors(self, id, came_from: dict[Location, Optional[Location]]):
        x, y, *_ = id
        neighbors = [(x + dx, y + dy) for (dx, dy) in self.NEIGHBOR_ORDER]
        results = filter(self.in_bounds, neighbors)
        results = filter(functools.partial(self.passable, id), results)
#        results = filter(self.passable, results)
        return list(results)

def test_with_custom_order(neighbor_order):
    if neighbor_order:
        g = SquareGridNeighborOrder(30, 15)
        g.NEIGHBOR_ORDER = neighbor_order
    else:
        g = SquareGrid(30, 15)

    g.walls = DIAGRAM1_WALLS
    start, goal = (8, 7), (27, 2)
    came_from = breadth_first_search(g, start, goal)
    draw_grid(g, path=reconstruct_path(came_from, start=start, goal=goal),
              point_to=came_from, start=start, goal=goal)


class GridWithAdjustedWeights(GridWithWeights):
    def cost(self, from_node, to_node):
        prev_cost = super().cost(from_node, to_node)
        nudge = 0
        (x1, y1) = from_node
        (x2, y2) = to_node
        if (x1 + y1) % 2 == 0 and x2 != x1: nudge = 1
        if (x1 + y1) % 2 == 1 and y2 != y1: nudge = 1
        return prev_cost + 0.001 * nudge
