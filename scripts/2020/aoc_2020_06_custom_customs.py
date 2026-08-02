from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
from utils.timer_utils import timefunction

from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
import pyperclip
from icecream import ic

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from utils.quicklambda import _1


# https://adventofcode.com/2020/day/6


@timefunction
def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    lines = inp.strip().split('\n')
#    lines = inp.strip("\n").split('\n')
    ic(len(lines))
#    ics(inp)
#    ic(1 in sets_union([]))

    @timefunction
    def part1():
        ics(seq(lines).split().map(lambda g: len(sets_union(g))))
        result = seq(lines).split().map(lambda g: len(sets_union(g))).sum()
        print_result(result)

    @timefunction
    def part2():
        result = seq(lines).split().map(lambda g: len(sets_intersection(g))).sum()
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
        # needs env var AOC_SESSION
        real_inp = get_aocd_data()
        run(real_inp, True)
#        aocd.submit(my_answer)


main()

