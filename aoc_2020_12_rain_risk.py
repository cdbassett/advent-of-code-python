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
from iteration_utilities import return_identity as identity

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
#    w = width(lines)
#    h = height(lines)
#    ic(w, h)
#    ics(inp)
    instructions = seq(lines).map(head_tail).multimap(identity, int)
#    ics(instructions)

    directions = tuple(compass_movements.keys())
#    next_right = seq(compass_movements).pad_back("N").successive(2).to_dict()
#    next_left = seq(compass_movements).pad_back("N").reverse().successive(2).to_dict()


    @timefunction
    def part1():
        facing = "E"
        position = 0, 0
        facing_index = seq(directions).zip_with_index().to_dict()
        ics(facing_index)

        for code, val in instructions:
            if code == "R":
                code, val = "L", -val

            if code == "L":
                facing = directions[(facing_index[facing] - val // 90) % 4]
            else:
                if code == "F":
                    code = facing

                position = add_tuple(position, multiply_scalar_tuple(compass_movements[code], val))

        ic(position)
        result = manhattan((0,0), position)
        print_result(result)



    @timefunction
    def part2():
        position = 0, 0
        waypoint = 10, -1

        for code, val in instructions:
#            ics(position, waypoint, code, val)

            if code == "R":
                code, val = "L", -val

            if code == "F":
                position = add_tuple(position, multiply_scalar_tuple(waypoint, val))
            elif code == "L":
                    # will always result in 0-3
                index = (val // 90) % 4
                wx, wy = waypoint

                for nm in range(index):
                    wx, wy = wy, -wx # rotate 2D vector about origin CW

#                ics(waypoint, val, index, wx, wy)
                waypoint = wx, wy
            else:
                waypoint = add_tuple(waypoint, multiply_scalar_tuple(compass_movements[code], val))

        ic(position)
        result = manhattan((0,0), position)
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
F10
N3
F7
R90
F11
"""


short_samp = """
"""


samp_inps = [
#    short_samp,
    samp_inp,
    ]


main()

