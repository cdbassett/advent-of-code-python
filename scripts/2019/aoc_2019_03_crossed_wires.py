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


from utils.timer_utils import timefunction
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from utils.quicklambda import _1, _2


# https://adventofcode.com/2019/day/3


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
    example = get_aocd_example()
    samp_inps = split_example(example)

    for n, samp_inp in enumerate(samp_inps, 1):
        print(f"{Fore.BLUE}{Style.BRIGHT}Sample {n}:{Style.RESET_ALL}")
        run(samp_inp, samp_inp, False)

    if 1:
        print(f"{Fore.BLUE}{Style.BRIGHT}Actual:{Style.RESET_ALL}")
        # needs env var AOC_SESSION
        real_inp = get_aocd_data()
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)


main()

