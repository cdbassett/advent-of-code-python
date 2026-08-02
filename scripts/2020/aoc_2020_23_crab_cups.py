from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
from utils.timer_utils import timefunction

from colorama import Fore, Style
from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
from icecream import ic

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from utils.quicklambda import _1, _2
from mini_lambda import s, _, x


# https://adventofcode.com/2020/day/23


icf = ic.format

@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        cups = map_tuple(int, inp.strip())
        return cups

    def cup_seq(cur_cup, next_cups):
        cup = cur_cup
        yield cur_cup

        while (cup := next_cups[cup]) != cur_cup:
            yield cup

    def cup_repr(cur_cup, next_cups):
        return sjoin(str(cup) for cup in cup_seq(cur_cup, next_cups))


    def process(cups, moves, part1):
            # each entry points to next cup
        next_cups = dict(pairwise(cups))
        next_cups[cups[-1]] = cups[0]
        max_cup = max(cups)
        min_cup = min(cups)
        cur_cup = cups[0]
        ics(min_cup, max_cup)

        for step in range(moves):
            if is_sample and part1 and step <= 10:
                ics(step, cur_cup, cup_repr(cur_cup, next_cups))

            work_cups = [next_cups[cur_cup]]
            work_cups.append(next_cups[work_cups[-1]])
            work_cups.append(next_cups[work_cups[-1]])
            after_work_cup = next_cups[cur_cup] = next_cups[work_cups[-1]]
            dest_cup = cur_cup - 1

                # determine actual dest_cup
            while dest_cup in work_cups or dest_cup < min_cup:
                dest_cup -= 1

                if dest_cup < min_cup:
                    dest_cup = max_cup

            after_dest_cup = next_cups[dest_cup]

            if is_sample and step <= 10:
                ics(step, work_cups, after_work_cup, dest_cup, after_dest_cup)

            for work_cup in work_cups:
                next_cups[dest_cup] = work_cup
                dest_cup = work_cup

            next_cups[work_cups[-1]] = after_dest_cup
            cur_cup = after_work_cup


        return cur_cup, next_cups



    @timefunction
    def part1(inp):
        cups = data_parse(inp)
        cur_cup, next_cups = process(cups, 100, True)
        ics(next_cups)
        result = cup_repr(1, next_cups)[1:]
        # 149725386 is too high
        print_result(result)

    @timefunction
    def part2(inp):
        cups = data_parse(inp)
        cups = cups + tuple(range(max(cups)+1, 1_000_000+1))
        cur_cup, next_cups = process(cups, 10_000_000, False)
        first_cup = next_cups[1]
        second_cup = next_cups[first_cup]
        result = first_cup * second_cup
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

