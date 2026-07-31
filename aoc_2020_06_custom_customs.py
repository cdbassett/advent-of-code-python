from functools import *
from collections import *
#from sympy import *
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
#from fz import _1
from quicklambda import _1


@timefunction
def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    lines = inp.strip().split('\n')
#    lines = inp.strip("\n").split('\n')
    ic(len(lines))
#    ics(inp)
#    ic(1 in sets_union([]))

    @timefunction
    def part1():
        ics(seq(lines).split().map(lambda g: len(sets_union(g))))
        result = seq(lines).split().map(lambda g: len(sets_union(g))).sum()
        print_result(result)

    @timefunction
    def part2():
        result = seq(lines).split().map(lambda g: len(sets_intersection(g))).sum()
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
        real_inp = get_aocd_data()
        run(real_inp, True)
#        aocd.submit(my_answer)




samp_inp = r"""
abc

a
b
c

ab
ac

a
a
a
a

b
"""


short_samp = """
"""


samp_inps = [
#    short_samp,
    samp_inp,
    ]


main()

