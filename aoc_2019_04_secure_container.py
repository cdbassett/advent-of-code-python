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


# accidentally overwrote solution - but it was simple
# this solves prevoius day's problem

@timefunction
def run(inp1, inp2, is_real):
    is_sample = not is_real
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    def data_parse(inp):
        lines = inp.strip().split('-')

        parsed = map_tuple(int, lines)
        return parsed

    def is_valid1(password):
        pairs = list(pairwise(str(password)))

        if any(a > b for a, b in pairs):
            return False

        if any(b == a for a, b in pairs):
            return True

        return False

    def process1(parsed, valid_func):
        return seq.range(parsed[0], parsed[1] + 1).count(valid_func)

    def is_valid2(password):
        password = str(password)
        pairs = list(pairwise(password))

        if any(a > b for a, b in pairs):
            return False

        if any(count_iter(g)==2 for k, g in groupby(password)):
            return True

        return False

    ics(is_valid1("111111"))
    ics(is_valid1("223450"))
    ics(is_valid1("123789"))
    ics(is_valid2("112233"))
    ics(is_valid2("123444"))
    ics(is_valid2("111122"))

    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ic(parsed)
        result = process1(parsed, is_valid1)
        print_result(result)


    process2 = process1


    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
        ic(parsed)
        result = process1(parsed, is_valid2)
        # 911 is too low
        print_result(result)

    part1(inp1)
    part2(inp2)

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
        real_inp = get_aocd_data()
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)




samp_inp1 = r"""
"""

samp_inp2 = samp_inp1

samp_inps = """
""".strip().split("\n")

samp_inps = [
    ]

main()

