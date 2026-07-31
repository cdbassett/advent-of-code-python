from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
from timer_utils import timefunction


from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
import pyperclip
from icecream import ic

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
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

