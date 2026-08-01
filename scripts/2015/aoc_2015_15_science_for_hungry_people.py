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
from icecream import ic

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from mini_lambda import s, _, x


@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().split('\n')
#        ics(lines)
        data = string_to_integers(inp)
#        ics(data)
        return data

    def process1(parsed):
#        names, *values = zip(*parsed)
        names = None
        values = list(zip(*parsed))
        all_values = values[:-1]
        ic(names, all_values)
        best_total = 0
        p = PrintMaxTimes(10)

        for a in range(101):
            for b in range(101 - a):
                for c in range(101 - a - b):
                    d = 100 - a - b - c # last ingredient gets whatever is left over
                    assert d >= 0
                    amounts = a, b, c, d
#                    assert sum(amounts) == 100
                    total = prod(max(0, sumprod(amounts, values)) for values in all_values)

#                    if p.should_print_and_inc():
#                        ic([sumprod(amounts, values) for values in all_values])
#                        ic(amounts, total, best_total)

                    best_total = max(best_total, total)

        return best_total


    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)
        result = process1(parsed)
        print_result(result)

    process2 = process1

    def process2(parsed):
#        names, *values = zip(*parsed)
        names = None
        values = list(zip(*parsed))
        all_values = values[:-1]
        calories = values[-1]
        ic(names, all_values)
        best_total = 0
        p = PrintMaxTimes(10)

        for a in range(101):
            for b in range(101 - a):
                for c in range(101 - a - b):
                    d = 100 - a - b - c # last ingredient gets whatever is left over
                    assert d >= 0
                    amounts = a, b, c, d
#                    assert sum(amounts) == 100

                    if sumprod(amounts, calories) != 500:
                        continue

                    total = prod(max(0, sumprod(amounts, values)) for values in all_values)

#                    if p.should_print_and_inc():
#                        ic([sumprod(amounts, values) for values in all_values])
#                        ic(amounts, total, best_total)

                    best_total = max(best_total, total)

        return best_total


    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
        result = process2(parsed)
        print_result(result)

    part1(inp1)
    part2(inp2)

def main():
    if 0: # samples fro maocd don't work yet, replaced from hardcoded to put on github
        example = get_aocd_example()
        samp_inps = split_example(example)

        for n, samp_inp in enumerate(samp_inps, 1):
            print(f"{Fore.BLUE}{Style.BRIGHT}Sample {n}:{Style.RESET_ALL}")
            run(samp_inp, samp_inp, False)

    if 1:
        print(f"{Fore.BLUE}{Style.BRIGHT}Actual:{Style.RESET_ALL}")
        # needs env var AOC_SESSION
        real_inp = get_aocd_data()
        run(real_inp, real_inp, True)

main()


