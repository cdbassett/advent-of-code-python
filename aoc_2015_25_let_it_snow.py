from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
from timer_utils import timefunction

from colorama import Fore, Style
from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
import pyperclip
from icecream import ic
import aocd # https://github.com/wimglenn/advent-of-code-data
# aocd.lines  # like data.splitlines()
# aocd.numbers # uses regex pattern -?\d+ to extract integers from data


from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from quicklambda import _1, _2



@timefunction
def run(inp1, inp2, is_real):
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

    process2 = process1

    def process2(parsed):
        return 0


    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
        result = process2(parsed)
        print_result(result)

    part1(inp1)
#    part2(inp2)

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
        real_inp = aocd.data # supposed to work if filename is clear enough (year would need to be 4-digit)
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)




samp_inp1 = r"""
To continue, please consult the code grid in the manual.  Enter the code at row 3, column 5.
"""

samp_inp2 = samp_inp1


samp_inps = [
    ]


main()

