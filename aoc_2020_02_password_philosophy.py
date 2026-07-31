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


# accidentally overwrote solution - but it was simple
# this solves prevoius day's problem

@timefunction
def run(inp, is_real):
    insert_sample_functions(is_real, globals())
    ics(inp)
#    inp = inp.strip("\n").split('\n')

    Rule = namedtuple("Rule","num1,num2,letter,password")

    def parse_line(line):
        parts = line.split()
        nums = string_to_integers(line.replace("-", " "))
        return Rule(nums[0], nums[1], parts[1].strip(":"), parts[2])

    def parse_data(inp):
        return seq(inp.strip().split("\n")).map(parse_line).list()

    def process(parsed, valid_func):
        return seq(parsed).count(valid_func)

    def is_valid1(rule):
        cnt = rule.password.count(rule.letter)
        ics(rule, cnt)
        return rule.num1 <= cnt <= rule.num2


    @timefunction
    def part1():
        parsed = parse_data(inp)
        result = process(parsed, is_valid1)
        print_result(result)

    def is_valid2(rule):
        s = rule.password[rule.num1-1] + rule.password[rule.num2-1]

        return rule.letter in s and s != rule.letter * 2

    @timefunction
    def part2():
        parsed = parse_data(inp)
        result = process(parsed, is_valid2)
        print_result(result)

    part1()
    part2()

def main():
#    print(real_inp)

    if 1:
        if "example" not in dir() or not example:
            example = get_aocd_example()

        sample_data1s = split_example(example)

        for samp_inp in sample_data1s:
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

