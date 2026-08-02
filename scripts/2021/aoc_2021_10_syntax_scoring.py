from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import pyperclip
from icecream import ic
import iteration_utilities as it_ut

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


# https://adventofcode.com/2021/day/10


open_chars = "([{<"
open_chars_set = set(open_chars)
close_chars = ")]}>"

open_for_close = dict(zip(close_chars, open_chars))
close_for_open = dict(zip(open_chars, close_chars))
invalid_scores = dict(zip(close_chars, (3, 57, 1197, 25137)))
completion_scores = dict(zip(close_chars, (1, 2, 3, 4)))

def is_corrupted(line, track = None):
    if track is None:
        track = []

    for c in line:
        if c in open_chars_set:
            track.append(c)
        else:
            p = track.pop()

            if p != open_for_close[c]:
                return c

def get_close(line, track = None):
    cnt = Counter()
    if track is None:
        track = []

    for c in line:
        if c in open_chars_set:
            track.append(c)
        else:
            p = track.pop()

            if p != open_for_close[c]:
                return cnt


def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')
    lines = inp
#    corrupted = [line for line in lines if is_corrupted(line)]
    incomplete, corrupted = it_ut.partition(lines, lambda line: is_corrupted(line))
    ics(corrupted)

#    for line in lines:


    def part1():
        scores = [invalid_scores[is_corrupted(line)] for line in corrupted]
        result = sum(scores)
        print_result(result)

    def part2():
        closings = []
        scores = []

        for line in incomplete:
            track = []
            is_corrupted(line, track)
            ics(track)
            closing = "".join(reversed(list(close_for_open[c] for c in track)))
            ics(closing)
#            closings.append(closing)
            score = 0

            for c in closing:
                score = score * 5 + completion_scores[c]

            ics(score)
            scores.append(score)

        scores = sorted(scores)
        ics(scores)
        result = scores[len(scores)//2]
        print_result(result)

    part1()
    part2()

def main():
    example = get_aocd_example()
    samp_inps = split_example(example)

    for n, samp_inp in enumerate(samp_inps, 1):
        print(f"{Fore.BLUE}{Style.BRIGHT}Sample {n}:{Style.RESET_ALL}")
        run(samp_inp, False)

    if 1:
        print(f"{Fore.BLUE}{Style.BRIGHT}Actual:{Style.RESET_ALL}")
        real_inp = get_aocd_data()
        run(real_inp, True)

main()
