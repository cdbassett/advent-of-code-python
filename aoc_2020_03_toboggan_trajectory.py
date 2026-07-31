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

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
#from fz import _1
from quicklambda import _1


@timefunction
def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')
#    inp = inp.strip("\n").split('\n')
    ic(len(inp))
#    ics(inp)


    def count_trees(lines, x_delta, y_delta):
        x = 0
        cnt = 0
        w = width(lines)

        for y in range(0, height(lines), y_delta):
            if lines[y][x] == "#":
                cnt += 1

            x = (x + x_delta) % w

        return cnt



    @timefunction
    def part1():
        result = count_trees(inp, 3, 1)
        print_result(result)


    @timefunction
    def part2():
        slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2), ]
        result = products(count_trees(inp, x_delta, y_delta) for x_delta, y_delta in slopes)
        print_result(result)

    part1()
    part2()

def main():
#    print(real_inp)

    if 1:
        for samp_inp in samp_inps:
            print("Sample:")
            run(samp_inp, False)

    if 1:
        print("Actual:")
#        real_inp = aocd.get_data(day=25, year=2021)
            # needs env var AOC_SESSION
        real_inp = get_aocd_data()
        run(real_inp, True)
#        aocd.submit(my_answer)




samp_inp = r"""
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
"""

short_samp = """
"""


samp_inps = [
#    short_samp,
    samp_inp,
    ]


main()

