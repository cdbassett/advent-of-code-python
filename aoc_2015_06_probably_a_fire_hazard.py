from functools import *
from collections import *
#from sympy import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
#import shapely
#import shapely.ops
from timer_utils import timefunction
#import networkx as nx
#import matplotlib.pyplot as plt
#from construct import *

#from sympy import *

import numpy as np
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
        lines = inp.strip().split('\n')
#        numbers = map(string_to_integers, lines)
        numbers = seq(lines).map(compose(string_to_integers, chunks_of_2, transpose, flatten, list))
        slices = [seq(line).grouped(2).multimap(identity, increment).starmap(slice).to_tuple() for line in numbers]
#        ics(slices)
        inst = [1 if line.startswith("turn on") else 0 if line.startswith("turn off") else 2 for line in lines]
        return list(zip(inst, slices))


    def process1(parsed):
        array = np.zeros((1000,1000), dtype=bool)

        for inst, (sx, sy) in parsed:
            if inst == 2:
                array[sx, sy] ^= True
            else:
                array[sx, sy] = bool(inst)

        return np.count_nonzero(array)


    inst_to_brightness = dict(enumerate((-1, 1, 2)))

    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)
        result = process1(parsed)
        print_result(result)

    process2 = process1

    def process2(parsed):
        array = np.zeros((1000,1000), dtype=int)

        for inst, (sx, sy) in parsed:
            array[sx, sy] += inst_to_brightness[inst]
            array = np.clip(array, 0, None)
#            ics(inst, inst_to_brightness[inst], sx, sy, np.sum(np.clip(array, 0, None)))
#            ics(np.sum(array), np.sum(array[sx, sy]))

        return int(np.sum(array))

    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
        result = process2(parsed)
        print_result(result)

    part1(inp1)
    part2(inp2)

def main():
    if 1:
        if samp_inps and samp_inps[0]:
            for n, samp_inp in enumerate(samp_inps, 1):
                print_preface(False, n)
                run(samp_inp, samp_inp, False)
        else:
            print_preface(False)
            run(samp_inp1, samp_inp2, False)

    if 1:
        print_preface(True)
            # needs env var AOC_SESSION
        real_inp = aocd.data # supposed to work if filename is clear enough (year would need to be 4-digit)
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)




samp_inp1 = r"""
turn on 0,0 through 999,999
toggle 0,0 through 999,0
turn off 499,499 through 500,500
"""

samp_inp2 = samp_inp1
samp_inp2 = r"""
turn off 0,0 through 999,999
toggle 0,0 through 999,0
turn on 499,499 through 500,500
"""


samp_inps = \
"""
""".strip().split("\n")


main()

