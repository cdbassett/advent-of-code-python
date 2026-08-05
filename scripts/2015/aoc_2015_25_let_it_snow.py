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
import pyperclip
from icecream import ic
import aocd # https://github.com/wimglenn/advent-of-code-data


from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from utils.quicklambda import _1, _2


# https://adventofcode.com/2015/day/25


@timefunction
def run(inp1, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        return string_to_integers(inp)

    def diagonal():
        for row in count(1):
            for x, y in zip(range(row+1), range(row, -1, -1)):
                yield x+1, y+1

    def process1(parsed):
        targy, targx = parsed
        ic(targx, targy)
        val = 20151125

        for col, row in diagonal():
            val = (val * 252533) % 33554393

            if col == targx and row == targy:
                return val

        return 0

    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)
        result = process1(parsed)
        print_result(result)

    part1(inp1)

def main():
    # aocd example retrieval doesn't work for this puzzle.

    print(f"{Fore.BLUE}{Style.BRIGHT}Actual:{Style.RESET_ALL}")
    real_inp = get_aocd_data()
    run(real_inp, True)
#        aocd.submit(my_answer)


main()

