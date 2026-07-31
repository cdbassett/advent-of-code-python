from operator import itemgetter
from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
from timer_utils import timefunction

from colorama import Fore, Style
from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
from icecream import ic

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from quicklambda import _1, _2


@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
#        parsed = inp.strip().split(inp.strip())
        parsed = seq(inp.strip().split(", ")).map(head_tail).multimap(identity, int)
        return parsed

    def positions(directions):
        movements = tuple(compass_movements.values())
        direction = 0 # north
        pos = 0, 0

        for turn, amount in directions:
            if turn == "R":
                direction += 1
            else:
                direction -= 1

            direction = direction % 4
            pos = add_tuple(pos, multiply_scalar_tuple(movements[direction], amount))
            ics(turn, amount, pos)
            yield pos


    def process1(parsed):
        start = 0, 0
        pos = last_element(positions(parsed))
        ic(pos)
        return manhattan(start, pos)

    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)
        result = process1(parsed)
        print_result(result)


    def positions2(directions):
        movements = tuple(compass_movements.values())
        direction = 0 # north
        pos = 0, 0

        for turn, amount in directions:
            if turn == "R":
                direction += 1
            else:
                direction -= 1

            direction = direction % 4

            for n in range(1, amount+1):
                yp = add_tuple(pos, multiply_scalar_tuple(movements[direction], n))
#                ics(yp)
                yield yp

            pos = add_tuple(pos, multiply_scalar_tuple(movements[direction], amount))


    def process2(parsed):
        visited = set()
        start = 0, 0

        for pos in positions2(parsed):
            if pos in visited:
                ic(pos)
                return manhattan(start, pos)

            visited.add(pos)


    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
        result = process2(parsed)
        # 269 is too high
        print_result(result)

    part1(inp1)
    part2(inp2)

def main():
    if 1:
        if samp_inps:
            for n, samp_inp in enumerate(samp_inps, 1):
                print_preface(False, n)
                run(samp_inp, samp_inp, False)
        elif samp_inp1.strip():
            print_preface(False)
            run(samp_inp1, samp_inp2, False)

    if 1:
        print_preface(True)
        real_inp = get_aocd_data()
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)


samp_inp1 = r"""
"""

samp_inp2 = ""


#R2, L3
#R2, R2, R2
samp_inps = """
R5, L5, R5, R3
R8, R4, R4, R8
""".strip().split("\n")
#samp_inps = []

main()

