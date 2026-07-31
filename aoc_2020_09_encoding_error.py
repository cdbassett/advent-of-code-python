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
import aocd # https://github.com/wimglenn/advent-of-code-data
# aocd.lines  # like data.splitlines()
# aocd.numbers # uses regex pattern -?\d+ to extract integers from data


from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from quicklambda import _1


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
    if 1:
        for samp_inp in samp_inps:
            print("Sample:")
            run(samp_inp, False)

    if 1:
        print("Actual:")
            # needs env var AOC_SESSION
        real_inp = get_aocd_data() # supposed to work if filename is clear enough (year would need to be 4-digit)
        run(real_inp, True)
#        aocd.submit(my_answer)




samp_inp = r"""
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
"""


short_samp = """
"""


samp_inps = [
#    short_samp,
    samp_inp,
    ]


main()

