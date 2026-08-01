from functools import *
from collections import *
from itertools import *
from math import *
from builtins import pow
import pyperclip
from icecream import ic

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


def overlaps_ex(range1, range2):
    return range1[0] <= range2[0] and range1[1] >= range2[1]

def overlaps(range1, range2):
    return overlaps_ex(range1, range2) or overlaps_ex(range2, range1)

def overlaps_any_ex(range1, range2):
    return range1[0] <= range2[0] and range1[1] >= range2[1]

def between(a, l, h):
    return a >= l and a <= h

def overlaps_any(range1, range2):
    return max(range1[0], range2[0]) <= min(range1[1],range2[1])

def main(inp, is_real):
    insert_sample_functions(is_real, globals())
    print_preface(is_real)
    inp = inp.strip().split('\n')
    section_pairs = [line.split(",") for line in inp]
#    print_sample("num_pairs" + repr(num_pairs))

    def part1(inp, is_real):
        have_overlap_count = 0

        for s_pairs in section_pairs:
            num_pairs = [list(map(int, s_pair.split("-"))) for s_pair in s_pairs]

            if overlaps(num_pairs[0], num_pairs[1]):
                have_overlap_count += 1
#                print_sample("overlaps")

        print_result(have_overlap_count)

    def part2(inp, is_real):
        section_pairs = [line.split(",") for line in inp]
        have_overlap_count = 0

        for s_pairs in section_pairs:
            num_pairs = [list(map(int, s_pair.split("-"))) for s_pair in s_pairs]

            if overlaps_any(num_pairs[0], num_pairs[1]):
                have_overlap_count += 1
#                print_sample("overlaps")

        print_result(have_overlap_count)

    part1(inp, is_real)
    part2(inp, is_real)

def run_samples():
    examples = get_aocd_example()
    samples = split_example(examples)
    for s in samples:
        main(s, False)

run_samples()

real_inp = get_aocd_data()
main(real_inp, True)

