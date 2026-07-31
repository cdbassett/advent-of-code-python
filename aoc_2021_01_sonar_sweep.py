from functools import *
from collections import *
from itertools import *
from math import *
from builtins import pow

from functional import seq # https://github.com/EntilZha/PyFunctional
import pyperclip
from icecream import ic
import aocd # https://github.com/wimglenn/advent-of-code-data

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


def run(inp, is_real):
    insert_sample_functions(is_real, globals())

    lines = inp.strip().split('\n')
    measurements = seq(lines).map(int)
    gt = lambda x: x[1] > x[0]

    def part1():
        result = measurements.sliding(2).count(gt)
        print_result(result)

    def part2():
        result = measurements.sliding(3).map(sum).sliding(2).count(gt)
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
        real_inp = get_aocd_data()
        run(real_inp, True)
#        aocd.submit(my_answer)

main()

