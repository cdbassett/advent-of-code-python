from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import pyperclip
from icecream import ic
from utils.utilities import *
import iteration_utilities as it_ut
from utils.timer_utils import timefunction
import networkx as nx
import matplotlib.pyplot as plt

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

Point = Point2D

def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')
    h_map = [list(map(int, line)) for line in inp]
    start = (0, 0)
    ics(h_map)



    def build_graph(h_map):
        def pval(x, y):
            return h_map[y][x]

        width = len(h_map[0])
        height = len(h_map)
        end = (width-1, height-1)
        g = nx.DiGraph()

        for (xa, xb), y in product(pairwise(range(width)), range(height)):
            g.add_edge((xa,y),(xb,y),weight=pval(xb, y))
            g.add_edge((xb,y),(xa,y),weight=pval(xa, y))

        for (ya, yb), x in product(pairwise(range(height)), range(width)):
            g.add_edge((x,ya),(x,yb),weight=pval(x, yb))
            g.add_edge((x,yb),(x,ya),weight=pval(x, ya))

        return end, g


#    path = nx.shortest_path(g, source=start,target=end, weight='weight')

    @timefunction
    def part1():
        end, g = build_graph(h_map)
        length, path = nx.bidirectional_dijkstra(g, source=start,target=end, weight='weight')

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

        # works but too slow
    def part2():
        def new_risk(r, dist):
            r += dist
#            return (r % 9 + 1) if r > 9 else r
            return ((r-1) % 9 + 1) if r > 9 else r

        def build_map_chunk(h_map, x, y):
            dist = x + y
            chunk = [[new_risk(r, dist) for r in line] for line in h_map]
#            ics(x, y, chunk)
            return chunk

        def build_line(line, y):
#            dist = x + y
            return list(it_ut.flatten([new_risk(r, x + y) for r in line] for x in range(5)))

        def build_5x_map(h_map):
            new_map = list(it_ut.flatten([build_line(line, y) for line in h_map] for y in range(5)))
#            ics(x, y, chunk)
            return new_map

#        h5_map = list(it_ut.flatten(list(it_ut.flatten(build_map_chunk(h_map, x, y) for x in range(5))) for y in range(5)))
        h5_map = build_5x_map(h_map)
#        ics(build_map_chunk(h_map, 2, 1))
        vis_map = ["".join(str(r) for r in line) for line in h5_map]
        ics(vis_map)

        end, g = build_graph(h5_map)
        length, path = nx.bidirectional_dijkstra(g, source=start,target=end, weight='weight')
        dots = [Point(*p) for p in path]
        ics(get_vis_map(dots, False))
        result = length
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
