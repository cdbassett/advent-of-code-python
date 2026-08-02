from functools import *
from collections import *
from sympy import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import pyperclip
from icecream import ic
from utils.utilities import *
from utils.timer_utils import timefunction

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


# https://adventofcode.com/2022/day/25


def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')
#    inp = inp.strip("\n").split('\n')

    snafu_values = dict((str(n), n) for n in range(3))
    snafu_values["-"] = -1
    snafu_values["="] = -2

    num_values = dict((v, k) for k, v in snafu_values.items())
#    num_values = dict((str(n), n) for n in range(3))
#    num_values["-"] = -1
#    num_values[] = "="


    def to_snafu(num):
        if not num:
            return "0"

        val = ""

        while num:
            num, rem = divmod(num, 5)

            if rem > 2:
                num += 1
                rem -= 5

            val = num_values[rem] + val

        return val


    def from_snafu(s):
        val = 0
        mult = 1

        for c in reversed(s):
            val += mult * snafu_values[c]
            mult *= 5

        return val

    ics(from_snafu("1121-1110-1=0")) # 314159265
    ics(to_snafu(314159265)) # 314159265



    @timefunction
    def part1():
        result = to_snafu(sum(from_snafu(line) for line in inp))

        print_result(result)



    @timefunction
    def part2():
        last_config = None

        for round in count(1):
            ic(round)
            process(elves, checks_moves)

            if elves == last_config:
                break

            last_config = set(elves)

        ics(round, get_vis_map(elves))
        result = round
        print_result(result)

    part1()
#    part2()

def main():
    example = get_aocd_example()
    samp_inps = split_example(example)

    for n, samp_inp in enumerate(samp_inps, 1):
        print(f"{Fore.BLUE}{Style.BRIGHT}Sample {n}:{Style.RESET_ALL}")
        run(samp_inp, False)

    if 1:
        print(f"{Fore.BLUE}{Style.BRIGHT}Actual:{Style.RESET_ALL}")
        real_inp = get_aocd_data()
        run(real_inp, True)

main()
