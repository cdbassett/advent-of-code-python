from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *

from icecream import ic

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *


# https://adventofcode.com/2021/day/7


def run(inp, is_real):
    insert_sample_functions(is_real, globals())
    print_preface(is_real)
    inp = inp.strip().split('\n')
    crab_positions = list(map(int, inp[0].split(",")))
    min_pos = min(crab_positions)
    max_pos = max(crab_positions)
    pos_range = range(min_pos, max_pos + 1)

    def cost1(position):
        return sum(abs(e - position) for e in crab_positions)

    def cost2_ind(e):
        return (e**2 + e)//2

#    def cost2_ind(e):
#        return reduce(operator.add, range(1, e+1)) if e > 1 else e

    def cost2(position):
        pos_cost = [cost2_ind(abs(e - position)) for e in crab_positions]
        return sum(pos_cost)

#    def cost2(position):
#        pos_diff = [abs(e - position) for e in crab_positions]
#        pos_cost = [cost2_ind(e) for e in pos_diff]
#        return sum(pos_cost)

    def part1():
        optimal_position = round(median(crab_positions))
        result = sum(abs(e - optimal_position) for e in crab_positions)
        print_result(result)

    def part1():
        min_cost, min_pos = min((cost1(position), position) for position in pos_range)
        result = min_cost
        print_result(result)

    def part2():
        min_cost, min_pos = min((cost2(position), position) for position in pos_range)
        result = min_cost
        print_result(result)

    print_list("costs", list((n, cost2_ind(n)) for n in range(9)))
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
