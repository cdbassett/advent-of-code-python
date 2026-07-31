from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
from timer_utils import timefunction

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
        return inp.strip()

    def inc_pass(pw):
        work = list(pw)

        for i, c in reversed(list(enumerate(work))):
            if c == "z":
                work[i] = "a"
                continue

            work[i] = chr(ord(c)+1)
            return sjoin(work)

        return pw

    fails = set("iol")

    def pass_valid(pw):
        if not fails.isdisjoint(pw):
            return False

        clumps = [l for k, v in groupby(pw) if (l := len(list(v))) > 1]

#        if len(clumps) < 2 and (not clumps or clumps[0] < 4):
        if not clumps or len(clumps) < 2 and clumps[0] < 4:
            return False

        for triplet in triplewise(pw):
            ords = map_tuple(ord, triplet)

            if ords[0] + 1 == ords[1] == ords[2] - 1:
                break
        else:
            return False


        return True

    def process1(parsed):
#        assert pass_valid(parsed)
        pw = parsed

        while (pw := inc_pass(pw)):
            if pass_valid(pw):
                return pw


    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)
        result = process1(parsed)
        print_result(result)

    process2 = process1


    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
        result = process2(parsed)
        ic(result)
        result = process2(result)
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
abcdefgh
"""

samp_inp2 = samp_inp1


samp_inps = """
abcdefgh
ghijklmn
""".strip().split("\n")
samp_inps = []


main()

