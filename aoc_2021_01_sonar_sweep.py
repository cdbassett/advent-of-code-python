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
    print("Sample:")
    run(samp_inp, False)

    print("Actual:")
    real_inp = aocd.data # supposed to work if filename is clear enough (year would need to be 4-digit)
    run(real_inp, True)




samp_inp = r"""
199
200
208
210
200
207
240
269
260
263
"""

main()

