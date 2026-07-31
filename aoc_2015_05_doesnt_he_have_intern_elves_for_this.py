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

@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().split('\n')
        return lines


    def process_report(is_valid, line):
        res = is_valid(line)
        ics(line, res)
        return res

    def process1(parsed, is_valid):
#        return seq(parsed).count(is_valid)
        return seq(parsed).count(partial(process_report, is_valid))

    vowel_set = set("aeiou")
    bad_pairs = "ab,cd,pq,xy".split(",")

    @timefunction
    def part1(inp):
        def is_valid(line):
            for part in bad_pairs:
                if part in line:
                    ics(line, "bad_pairs")
                    return False

            if len(list(c for c in line if c in vowel_set)) < 3:
                ics(line, "insufficent vowels", list(c for c in line if c in vowel_set))
                return False

            for c1, c2 in pairwise(line):
                if c1 == c2:
                    return True


            ics(line, "no doubles")
            return False

        parsed = data_parse(inp)
        result = process1(parsed, is_valid)
        print_result(result)

    process2 = process1

    @timefunction
    def part2(inp):
        def is_valid(line):
            pair_counts = Counter(pairwise(line))

            for pair, cnt in pair_counts.items():
                if cnt > 1:
                    pair = sjoin(pair)
                    index = line.index(pair)
                    rindex = line.rindex(pair)

                    if rindex > index+1:
                        break
            else:
                ics(line, "no double pairs with something in between")
                return False

            for c1, c2, c3 in seq(list(line)).sliding(3):
                if c1 == c3:
                    return True


            ics(line, "no doubles with something in between")
            return False

        parsed = data_parse(inp)
        result = process1(parsed, is_valid)
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
ugknbfddgicrmopn
aaa
jchzalrnumimnmhp
haegwjzuvuyypxyu
dvszwmarrgswjxmb
"""

samp_inp2 = samp_inp1
samp_inp2 = r"""
qjhvhtzxzqqjkmpb
xxyxx
uurcxstgmygtbstg
ieodomkazucvgmuy
"""


samp_inps = \
"""
""".strip().split("\n")


main()

