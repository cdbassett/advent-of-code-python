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
import aocd # https://github.com/wimglenn/advent-of-code-data
# aocd.lines  # like data.splitlines()
# aocd.numbers # uses regex pattern -?\d+ to extract integers from data


from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from utils.quicklambda import _1


# https://adventofcode.com/2020/day/9


@timefunction
def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    lines = inp.strip().split('\n')
#    lines = inp.strip("\n").split('\n')
    ic(len(lines))
#    ics(inp)
    numbers = seq(lines).map(int)
    ics(numbers)
    preamble = 25 if is_real else 5

    def validate(numbers, preamble):
        n = preamble

        for *window, check in numbers.sliding(preamble+1):
            if check not in seq(window).combinations(2).map(sum):
                return check, n

            n += 1


    def search(numbers, key):
        count = numbers.len()

        for start, first in numbers.enumerate():
            for end in range(start+2, count):
                check_range = numbers[start:end]
                s = check_range.sum()

                if s == key:
#                    ic(check_range)
                    return check_range.min() + check_range.max()

                if s > key:
                    break


    @timefunction
    def part1():
        result, _ = validate(numbers, preamble)
        print_result(result)

    @timefunction
    def part2():
        key, index = validate(numbers, preamble)
        result = search(numbers[:index], key)
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

