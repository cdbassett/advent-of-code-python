from operator import itemgetter
from functools import *
from collections import *
from itertools import *
from utils.timer_utils import timefunction

from colorama import Fore, Style
from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
from icecream import ic

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


# https://adventofcode.com/2016/day/1


@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
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
            pos = add_tuple2(pos, multiply_scalar_tuple(movements[direction], amount))
            ics(turn, amount, pos)
            yield pos


    def process1(parsed):
        start = 0, 0
        pos = last_element(positions(parsed))
        ic(pos)
        return manhattan2(start, pos)

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
                yp = add_tuple2(pos, multiply_scalar_tuple(movements[direction], n))
                yield yp

            pos = add_tuple2(pos, multiply_scalar_tuple(movements[direction], amount))


    def process2(parsed):
        visited = set()
        start = 0, 0

        for pos in positions2(parsed):
            if pos in visited:
                ic(pos)
                return manhattan2(start, pos)

            visited.add(pos)


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
        real_inp = get_aocd_data()
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)


main()

