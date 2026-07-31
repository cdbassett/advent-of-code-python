from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import pyperclip
from icecream import ic
from timer_utils import timefunction
import networkx as nx
import matplotlib.pyplot as plt
from construct import *

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

Point = Point2D


def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')

#    h_map = [list(map(int, line)) for line in inp]
    h_map = inp

    def search(h_map, c):
        for y, line in enumerate(h_map):
            index = line.find(c)

            if index >= 0:
                return (index, y)

    def search_all(h_map, c):
        for y, line in enumerate(h_map):
            index = line.find(c)

            if index >= 0:
                yield (index, y)

    start = search(h_map, "S")
    end = search(h_map, "E")

    def set(x, y, c):
        line = h_map[y]
        line = "".join((line[:x], c, line[x+1:]))
        h_map[y] = line

    set(start[0], start[1], "a")
    set(end[0], end[1], "z")
    ics(start, end)
    ics(h_map)

    def build_graph(h_map):
        def pval(x, y):
            return ord(h_map[y][x])

        width = len(h_map[0])
        height = len(h_map)
        g = nx.DiGraph()

        for (xa, xb), y in product(pairwise(range(width)), range(height)):
            xa_val = pval(xa, y)
            xb_val = pval(xb, y)

            if xa_val >= xb_val - 1:
                g.add_edge((xa,y),(xb,y))

            if xb_val >= xa_val - 1:
                g.add_edge((xb,y),(xa,y))

        for (ya, yb), x in product(pairwise(range(height)), range(width)):
            ya_val = pval(x, ya)
            yb_val = pval(x, yb)

            if ya_val >= yb_val - 1:
                g.add_edge((x,ya),(x,yb))

            if yb_val >= ya_val - 1:
                g.add_edge((x,yb),(x,ya))

        return g


    @timefunction
    def part1():
        g = build_graph(h_map)

#        nx.draw_networkx(g, arrows=True)
#        plt.show()
        length, path = nx.bidirectional_dijkstra(g, source=start,target=end)

#        if not is_real:
#            nx.draw_networkx(g)
#            plt.show()

    #    path = nx.bellman_ford_path(g, source=start,target=end, weight='weight')
        dots = [Point(*p) for p in path]
        ics(get_vis_map(dots, False))


#        risks = [pval(*p) for p in path[1:]]
#        ics(risks)
#        result = sum(risks)
        result = length
        print_result(result)

    def part2():
        g = build_graph(h_map)
        start_points = list(search_all(h_map, "a"))
        ics(start_points)

#        nx.draw_networkx(g, arrows=True)
#        plt.show()


        results = [nx.bidirectional_dijkstra(g, source=start,target=end) for start in start_points]
        shortest = min(results)

#        if not is_real:
#            nx.draw_networkx(g)
#            plt.show()

#    path = nx.bellman_ford_path(g, source=start,target=end, weight='weight')
#        dots = [Point(*p) for p in path]
#        ics(get_vis_map(dots, False))

        result = shortest[0]
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
