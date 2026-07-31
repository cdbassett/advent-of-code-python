from functools import *
from collections import *
#from sympy import *
from itertools import *
from math import *
from statistics import *
import re
from builtins import pow
#import shapely
#import shapely.ops
from timer_utils import timefunction
#import networkx as nx
#import matplotlib.pyplot as plt
#from construct import *

#from sympy import *

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
        ics(lines)
        return lines


    re_hex = re.compile(r"\\x[0-9a-f]{2}")

    def process1(parsed):
        total = 0

        for line in parsed:
#            decoded = line[1:-1].replace('"', r'\"').replace(r"\\", "\\")
            decoded = line[1:-1].replace(r'\"', '"').replace(r"\\", "\\")
            decoded = re_hex.sub(lambda s: chr(int(s.group(0)[2:], base=16)), decoded)
            diff = len(line) - len(decoded)

            ics(line, decoded, diff)
            total += diff

        return total




    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        result = process1(parsed)
        # 1131 is too low
        print_result(result)

    process2 = process1

    def process2(parsed):
        total = 0

        for line in parsed:
            encoded = line.replace("\\", r"\\").replace('"', r'\"')
            diff = len(encoded) - len(line) + 2

            ics(line, encoded, diff)
            total += diff

        return total

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
""
"abc"
"aaa\"aaa"
"\x27"
"""

samp_inp2 = samp_inp1
#samp_inp2 = r"""
#"""


samp_inps = \
"""
""".strip().split("\n")


main()


