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


# https://adventofcode.com/2021/day/3


def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)
    print_list = partial(print_list_aoc, is_real)

    inp = inp.strip().split('\n')
    position_count = len(inp[0])

    def get_most_common(values):
        transposed = list("".join(e) for e in zip(*values))
        #    print_list("transposed", transposed)
        counts = [Counter(line) for line in transposed]
        #    print_list("counts", counts)
        most_common = [count.most_common() for count in counts]
        print_list("most_common", most_common)
        return most_common


    def part1():
        most_common = get_most_common(inp)
        gamma = "".join(mc[0][0] for mc in most_common)
#        ic(gamma)
        gamma = int(gamma, 2)
        ic(gamma)
        epsilon  = "".join(mc[1][0] for mc in most_common)
#        ic(epsilon)
        epsilon = int(epsilon, 2)
        ic(epsilon)

        result = gamma * epsilon
        print_result(result)

    def find_rating(idx):
        matches = inp[:]

        for n_pos in range(position_count):
            if not is_real:
                ic(matches)

            most_common = get_most_common(matches)
            mce = most_common[n_pos]
            ic(mce)
            mc = mce[idx][0] if len(mce) > 1 and mce[0][1] > mce[1][1] else "10"[idx]
            ic(n_pos, mc)
            matches = [match for match in matches if match[n_pos] == mc]

            if len(matches) == 1:
                ic(matches[0])
                return int(matches[0], 2)


    def part2():
        oxygen = find_rating(0)
        ic(oxygen)
        co2 = find_rating(1)
        ic(co2)
        result = oxygen * co2
        print_result(result)

    part1()
    part2()

def main():
    if 0: # samples from aocd don't work yet, replaced from hardcoded to put on github
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
