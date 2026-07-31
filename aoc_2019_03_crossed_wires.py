from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow

from colorama import Fore, Style
from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
from icecream import ic


from timer_utils import timefunction
from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from quicklambda import _1, _2



@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().split('\n')

        parsed = [seq(line.strip().split(",")).map(head_tail).multimap(identity, int) for line in lines]
        return parsed

    def process(directions, start=(0,0)):
        visited = dict()
        pos = start
        step_iter = iter(count(1))


        for dir, amount in directions:
            adjust = vertical_movements[dir]

            for n in range(amount):
                pos = add_tuple(pos, adjust)
                visited[pos] = next(step_iter)
#        ics(visited)
        return visited


    def process1(parsed):
        visted1 = process(parsed[0])
        visted2 = process(parsed[1])
        common = set(visted1.keys()).intersection(visted2.keys())
#        ics(common)
        return min(manhattan(pos) for pos in common)

    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)
        result = process1(parsed)
        print_result(result)

    process2 = process1

    def process2(parsed):
        visted1 = process(parsed[0])
        visted2 = process(parsed[1])
        common = set(visted1.keys()).intersection(visted2.keys())
#        ics(common)
        return min(visted1[c] + visted2[c] for c in common)


    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
        result = process2(parsed)
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
            # needs env var AOC_SESSION
        real_inp = get_aocd_data()
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)




samp_inp1 = r"""
"""

samp_inp2 = samp_inp1



samp_inps = ["""
R8,U5,L5,D3
U7,R6,D4,L4
""","""
R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83
""","""
R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7
"""]


main()

