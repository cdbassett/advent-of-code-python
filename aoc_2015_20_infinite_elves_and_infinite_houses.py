from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
from timer_utils import timefunction
import sympy

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
#from fz import _1
from quicklambda import _1, _2
#from mini_lambda import s, _, x



@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        return int(inp.strip())

    def flatten(nested):
        return list(chain.from_iterable(nested))

    def factors(n):
        return set(flatten(
#                    ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))
                    ([i, n//i] for i in range(1, int(pow(n, 0.5)) + 1) if n % i == 0)))


    def process1(parsed):
        check = parsed // 10

        for n in count(5):
#            f = factors(n)
            f = sympy.divisors(n)

#            if n % 10000 == 0:
##                ic(check, n, f, sum(f))
#                ic(check, n, sum(f))

            if sum(f) >= check:
                return n

        return None

    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)
        result = process1(parsed)
        print_result(result)

    process2 = process1

    def process2(parsed):
        check = parsed
        track = defaultdict(int)
        ic(parsed, check)

        for n in count(1):
            value = 11 * (track[n] + n) # previous + self

            if n % 10000 == 0:
#                ic(check, n, f, sum(f))
                ic(n, value)

            if value >= check:
                ic(n, value)
                return n

            del track[n] # don't need this entry any more, free up its memory

                # prefill the other 49 houses
            for f in range(2, 51):
                track[n * f] += n

        return 0


    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
        result = process2(parsed)
        # 718200 is too high
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
        real_inp = aocd.data # supposed to work if filename is clear enough (year would need to be 4-digit)
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)




samp_inp1 = r"""
130
"""

samp_inp2 = samp_inp1


samp_inps = [
    ]


main()

