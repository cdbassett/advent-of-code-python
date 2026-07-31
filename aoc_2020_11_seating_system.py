from functools import *
from collections import *
#from sympy import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
#import numpy as np
#import shapely
#import shapely.ops
from timer_utils import timefunction
#import networkx as nx
#import matplotlib.pyplot as plt
#from construct import *

#from Levenshtein import distance as levenshtein_distance
#from sympy import *

from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
import pyperclip
from icecream import ic
import aocd # https://github.com/wimglenn/advent-of-code-data
# aocd.lines  # like data.splitlines()
# aocd.numbers # uses regex pattern -?\d+ to extract integers from data


from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
#from fz import _1
from quicklambda import _1


@timefunction
def run(inp, is_real):
    insert_sample_functions(is_real, globals())

    lines = inp.strip().split('\n')
#    lines = inp.strip("\n").split('\n')
    ic(len(lines))
    w = width(lines)
    h = height(lines)
    ic(w, h)
#    ics(inp)

    def flatten_seats(seats):
        return seq(seats).map(list).flatten().to_list()

    def rebuild_seats(flattened):
        return [sjoin(line) for line in chunks_of_n(flattened, w)]

    ferry = lines
    org_flattened = flatten_seats(ferry)

#    ics(lines)
#    ics(flatten_seats(lines))
#    ics(rebuild_seats(flatten_seats(lines)))

    def simulate(ferry, neighbor_seat_map, vis_limit):
        for step in count(1):
            working = flatten_seats(ferry)
            reference = list(working)

#            if step == 1:
#                ics(rebuild_seats(working))

            for seat, c, neighbors in zip(count(), reference, neighbor_seat_map):
                if c != ".":
                    occupied_count = sum(1 for neighbor in neighbors if reference[neighbor] == "#")

#                    if step == 1:
#                        ics(seat, c, neighbors, occupied_count)

                    if c == "#":
                        if occupied_count >= vis_limit:
                            working[seat] = "L"

                    if c == "L":
                        if occupied_count == 0:
                            working[seat] = "#"
#            if step < 5:
#                ics(rebuild_seats(reference))
#                ics(rebuild_seats(working))


            if working == reference:
                return seq(working).count(_1 == "#")

            ferry = rebuild_seats(working)

#            if step < 5:
#                ics(ferry)


    def build_seat_map(ferry, determine_neighbors):
        seat_map = [[determine_neighbors(x, y) for x in range(w)] for y in range(h)]
        return flatten_seats(seat_map)


    check_positions = [
        (-1,-1), (0, -1), (1, -1),
        (-1,0),  (1, 0),
        (-1,1), (0, 1), (1, 1),]


    @timefunction
    def part1():
#        check_positions = arithtuple([
#        check_positions = ([
#            -w-1, -w, -w+1,
#            -1,       +1,
#            w-1, w, w+1])


        def determine_neighbors(x, y):
            if ferry[y][x] == ".":
                return tuple()

            xy = x, y
            cur_check_positions = (add_tuple(check_position, xy) for check_position in check_positions)
            l = tuple(yn * w + xn for xn, yn in cur_check_positions if 0 <= xn < w and 0 <= yn < h and lines[yn][xn] != ".")
            return l


        ics(ferry)
        neighbor_seat_map = build_seat_map(ferry, determine_neighbors)
#        ics(neighbor_seat_map)
        result = simulate(ferry, neighbor_seat_map, 4)
        print_result(result)



    @timefunction
    def part2():
        def determine_neighbors(x, y):
            if ferry[y][x] == ".":
                return tuple()

            xy = x, y
            cur_check_positions = (add_tuple(check_position, xy) for check_position in check_positions)
            found_neighbors = []

            for check_position in check_positions:
                cur_check_position = add_tuple(check_position, xy)

                while True:
                    xn, yn = cur_check_position

                    if not (0 <= xn < w and 0 <= yn < h):
                        break

                    if lines[yn][xn] == "L":
                        found_neighbors.append(yn * w + xn)
                        break

                    cur_check_position = add_tuple(check_position, cur_check_position)

            return tuple(found_neighbors)

        neighbor_seat_map = build_seat_map(ferry, determine_neighbors)
#        ics(neighbor_seat_map)
        result = simulate(ferry, neighbor_seat_map, 5)
        print_result(result)

    part1()
    part2()

def main():
    if 1:
        for samp_inp in samp_inps:
            print("Sample:")
            run(samp_inp, False)

    if 1:
        print("Actual:")
#        real_inp = aocd.get_data(day=25, year=2021)
            # needs env var AOC_SESSION
        real_inp = aocd.data # supposed to work if filename is clear enough (year would need to be 4-digit)
        run(real_inp, True)
#        aocd.submit(my_answer)




samp_inp = r"""
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""


short_samp = """
"""


samp_inps = [
#    short_samp,
    samp_inp,
    ]


main()

