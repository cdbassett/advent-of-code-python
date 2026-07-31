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
#        lines = inp.strip().split('\n')
        dct = json.loads(inp)
        ics(dct)
        return dct


    def json_total(obj, should_process = lambda x: True):
        """Recursively fetch values from nested JSON."""

        if isinstance(obj, dict):
#            ics(obj, should_process(obj))
            total = sum(json_total(v, should_process) for k, v in obj.items()) if should_process(obj) else 0
        elif isinstance(obj, list):
            total = sum(json_total(item, should_process) for item in obj)
        elif isinstance(obj, int):
            total = obj
        else:
            total = 0

        return total


    def process1(parsed, should_process = lambda x: True):
        return json_total(parsed, should_process)



    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        result = process1(parsed)
        print_result(result)

    process2 = process1


    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
#        result = process2(parsed, should_process = lambda x: False)
        result = process2(parsed, should_process = lambda x: "red" not in x.values())
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
1
"""

samp_inp2 = samp_inp1
#samp_inp2 = r"""
#"""


samp_inps = \
"""
{"a":{"b":4},"d":{"r":4,"red":4},"c":-1}
""".strip().split("\n")
#{"a":{"b":4},"c":-1}
#[[[3]]]
#{"a":[-1,1]}
#[-1,{"a":2}]
#[]


main()


