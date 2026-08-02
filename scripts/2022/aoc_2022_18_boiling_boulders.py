from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import pyperclip
from icecream import ic
import shapely
import shapely.ops
from utils.timer_utils import timefunction
import networkx as nx
import matplotlib.pyplot as plt

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


# https://adventofcode.com/2022/day/18


def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')

    cubes = [tuple(map(int, line.split(","))) for line in inp]
    ics(len(cubes), cubes)
    points = set(cubes)

    max_x = max(p[0] for p in cubes)
    max_y = max(p[1] for p in cubes)
    max_z = max(p[2] for p in cubes)
    ic(max_x, max_y, max_z)

    min_x = min(p[0] for p in cubes)
    min_y = min(p[1] for p in cubes)
    min_z = min(p[2] for p in cubes)
    ic(min_x, min_y, min_z)

#    inp ="".join(inp) # handle lines too long for editor
#    ic(len(inp))
#    ics(rocks)

    def adjusted(p, adjust):
        return tuple(a + b for a, b in zip(p, adjust))

    def is_in(p, adjust):
        check = adjusted(p, adjust)
        return check in points



    """
        1) group cubes together
        2) count faces
    """

    adjustments = [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (-1, 0, 0),
        (0, -1, 0),
        (0, 0, -1),
    ]


    half_adjustments = adjustments[:3]

    def reg_range(min_v, max_v):
        return list(range(min_v-1, max_v+2))

    def pair_range(min_v, max_v):
        return list(pairwise(range(min_v-1, max_v+2)))

    x_range = reg_range(min_x, max_x)
    y_range = reg_range(min_y, max_y)
    z_range = reg_range(min_z, max_z)
    ic(len(x_range), len(y_range), len(z_range))

    def get_points_pairs():
        for (xa, xb), y, z in product(pair_range(min_x, max_x), y_range, z_range):
            yield (xa, y, z), (xb, y, z)

        for x, (ya, yb), z in product(x_range, pair_range(min_y, max_y), z_range):
            yield (x, ya, z), (x, yb, z)

        for x, y, (za, zb) in product(x_range, y_range, pair_range(min_z, max_z)):
            yield (x, y, za), (x, y, zb)


    def part1():
        faces = 0
#        ics(list(pairwise(range(min_x-1, max_x+2))))
#        ics(list(pairwise(range(min_y-1, max_y+2))))
#        ics(list(pairwise(range(min_z-1, max_z+2))))
#        ics(list(product(pairwise(range(min_x-1, max_x+2)), pairwise(range(min_y-1, max_y+2)))))
#        ics(list(product(pairwise(range(min_x-1, max_x+2)), pairwise(range(min_y-1, max_y+2)), pairwise(range(min_z-1, max_z+2)))))

        if 1:
            for pa, pb in get_points_pairs():
                pa_in = pa in points
                pb_in = pb in points
#                ics(pa, pb, pa_in != pb_in)

                if pa_in != pb_in:
                    faces += 1
        else:
            for p in product(x_range, y_range, z_range):
                p_in = p in points

                for adj in half_adjustments:
                    po_in = is_in(p, adj)

                    if p_in != po_in:
                        faces += 1

        result = faces
        print_result(result)



    def part2():

        def reg_range(min_v, max_v):
            return list(range(min_v-1, max_v+1))

        all_faces = 0
        gs = nx.Graph()
        ge = nx.Graph()
#        ics(it_ut.count_items(product(x_range, y_range, z_range)))
        empty_points = set(p for p in product(x_range, y_range, z_range) if p not in points)

#        ics(it_ut.count_items(get_points_pairs()))

        for pa, pb in get_points_pairs():
            pa_in = pa in points
            pb_in = pb in points

            if pa_in == pb_in:
                if pa_in:
                    ics(pa, pb)
                    gs.add_edge(pa, pb)
                else:
                    ge.add_edge(pa, pb)
            else:
                all_faces += 1


        ics(all_faces)
        ics(len(empty_points))

            # don't use connect solids because it deoesn;t take individual cubes into account
#        solids = list(nx.connected_components(gs))
#        ics(solids)
#        all_solids = sets_union(solids)
#        ics(len(all_solids))
        connected_empties = list(nx.connected_components(ge))
#        ics(empty_points)
#        ics(connected_empties)
        empty_corner = (min_x-1, min_y-1, min_z-1)
        outer_empty = first(n for n in connected_empties if empty_corner in n)
        inner_empties = list(n for n in connected_empties if empty_corner not in n)
#        all_inner_empties = sets_union(inner_empties)
        faces = 0
        ics(len(outer_empty))

        for p in cubes:
            for adj in adjustments:
                p_adj = adjusted(p, adj)

                if p_adj in outer_empty:
                    faces += 1


        result = faces
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
