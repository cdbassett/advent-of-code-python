from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from dataclasses import dataclass, field
from builtins import pow
import pyperclip
from icecream import ic

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


# https://adventofcode.com/2021/day/12


#Connection = namedtuple("Connection", "start,")

@dataclass
class Node:
    name: str
    neighbors: list = field(default_factory=list)

    def add_neighbor(self, node):
        self.neighbors.append(node)
        node.neighbors.append(self)

    def remove_neighbor(self, node):
        if node in self.neighbors:
            self.neighbors.remove(node)



    # we subclass this for __missing__ functionality, which is called when key not in dict upon
    # __getitem__() call (called by  dict[key] reference)
    # normal defaultdict behavior is to return default value and add to dict
    # we want to create a node and initialize it with key
class DefaultDictNode(collections.defaultdict):
    def __missing__(self, key):
        node = Node(key)
        self[key] = node
        return node


def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')
    connections = [line.split("-") for line in inp]
    nodes = DefaultDictNode() # name -> node

    for source, target in connections:
        nodes[source].add_neighbor(nodes[target])

    all_nodes = list(nodes.values())
    start_node = nodes["start"]
    end_node = nodes["end"]

        # don't bother with connections back to start
    for node in all_nodes:
        node.remove_neighbor(start_node)

    def simple_nodes(nodes=all_nodes):
#        return [[(p.x, p.y, p.val) for p in line_points] for line_points in points]
#        return [[p.val for p in line_points] for line_points in points]
        return [f"{node.name}: {','.join(n.name for n in node.neighbors)}" for node in nodes]

    def get_path_desc(path):
#        return "->".join(node.name for node in path)
        return ",".join(node.name for node in path)

    ics(simple_nodes())

    def traverse_path1(node, paths, path, visited):
#        ics(node.name)

        if node == end_node:
            path.append(node)
#            ics(get_path_desc(path))
            paths.append(path)
            return

        if node.name.islower():
            if node.name in visited:
                return
            else:
                visited.add(node.name)

        path.append(node)

        for n, neighbor in enumerate(node.neighbors):
#            ics(node.name, n)
            traverse_path1(neighbor, paths, path[:], set(visited))


    def traverse_path2(node, paths, path, visited, small_cave=None):
#        ics(node.name)

        if node == end_node:
            path.append(node)
#            ics(get_path_desc(path))
            paths.append(path)
            return

        if node.name.islower():
            if node.name in visited:
                if small_cave:
                    return
                else:
                    small_cave = node
            else:
                visited.add(node.name)

        path.append(node)

        for n, neighbor in enumerate(node.neighbors):
#            ics(node.name, n)
            traverse_path2(neighbor, paths, path[:], set(visited), small_cave)

    def part1():
        paths = []
        traverse_path1(start_node, paths, [], set())
        path_desc = [get_path_desc(path) for path in paths]
#        ics(path_desc)

#        ics(simple_nodes(paths[0]))
        result = len(paths)
        print_result(result)

    def part2():
        paths = []
#        traverse_path2(start_node, paths, [], Counter())
        traverse_path2(start_node, paths, [], set())
        path_desc = [get_path_desc(path) for path in paths]
#        ics(path_desc)

#        ics(simple_nodes(paths[0]))
        result = len(paths)
        print_result(result)

    part1()
    part2()

def main():
    example = get_aocd_example()
    samp_inps = split_example(example)

    for n, samp_inp in enumerate(samp_inps, 1):
        print(f"{Fore.BLUE}{Style.BRIGHT}Sample {n}:{Style.RESET_ALL}")
        run(samp_inp, False)

    if 1:
        print(f"{Fore.BLUE}{Style.BRIGHT}Actual:{Style.RESET_ALL}")
        real_inp = get_aocd_data()
        run(real_inp, True)

main()
