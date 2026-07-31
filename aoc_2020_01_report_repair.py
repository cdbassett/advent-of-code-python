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


@timefunction
def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')
#    inp = inp.strip("\n").split('\n')
    ic(len(inp))
    numbers = seq(inp).map(int)

    def solve(numbers, count):
        for t in numbers.combinations(count):
            if sum(t) == 2020:
                return products(t)


    @timefunction
    def part1():
        result = solve(numbers, 2)
        print_result(result)


    @timefunction
    def part2():
        result = solve(numbers, 3)
        print_result(result)

    part1()
    part2()

def main():
#    print(real_inp)

    if 1:
        for samp_inp in samp_inps:
            print("Sample:")
            run(samp_inp, False)

    if 1:
        print("Actual:")
            # needs env var AOC_SESSION
        real_inp = get_aocd_data()
        run(real_inp, True)
#        aocd.submit(my_answer)




samp_inp = r"""
1721
979
366
299
675
1456
"""

short_samp = """
"""


samp_inps = [
#    short_samp,
    samp_inp,
    ]


main()

