from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow

from colorama import Fore, Style
from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
import pyperclip
from icecream import ic

#print(sys.path)
from aoc_utils import * # this includes adding c:\ut to sys.path
from timer_utils import timefunction
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it



@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        parsed = int(inp.strip())
        return parsed


    base_pattern = [0, 1, 0, -1]

    def transform(digits, cnt):
        use_pattern = list(islice(cycle(chain.from_iterable([d] * cnt for d in base_pattern)), 1, len(digits)+1))
#        ics(cnt, use_pattern)
        return abs(sum(multiply_tuple(use_pattern, digits))) % 10

    def process1(parsed, phases):
        digits = tuple(map_int(str(parsed)))
        digit_cnt = len(digits)
        transformed = digits

        for phase in range(phases):
            transformed = [transform(transformed, cnt+1) for cnt in range(digit_cnt)]
#            ics(transformed)

        return int("".join(map(str, transformed))[:8])

    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)
        result = process1(parsed, 100)
        print_result(result)

    def transform_single(digits, cnt):
        use_pattern = list(islice(cycle(chain.from_iterable([d] * cnt for d in base_pattern)), 1, len(digits)+1))
#        ics(cnt, use_pattern)
        return abs(sum(multiply_tuple(use_pattern, digits))) % 10

    def transform2(digits, start, end):
        pass

    def process2(parsed, phases):
        digits = tuple(map_int(str(parsed)))
        digit_cnt = len(digits)
        transformed = digits

        for phase in range(phases):
            transformed = [transform2(transformed, cnt+1) for cnt in range(digit_cnt)]
#            ics(transformed)

        return int("".join(map(str, transformed))[:8])


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
        real_inp = get_aocd_data()
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)




samp_inp1 = r"""
"""

samp_inp2 = samp_inp1

samp_inps = """
12345678
80871224585914546619083218645595
19617804207202209144916044189917
69317163492948606335995924319873
""".strip().split("\n")

#samp_inps = [
#    ]

main()

