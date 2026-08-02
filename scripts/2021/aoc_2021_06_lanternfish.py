from functools import *
from collections import *
from itertools import *
from math import *
from builtins import pow
from icecream import ic
import iteration_utilities as it_ut

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


# https://adventofcode.com/2021/day/6


def run(inp, is_real):
    insert_sample_functions(is_real, globals())
    inp = inp.strip().split('\n')
    initial_fish = list(map(int, inp[0].split(",")))
    fish_counts = [0] * 9 # one element per possible day age value, element value is how many fish are that age

    for day, cnt in Counter(initial_fish).items():
        fish_counts[day] = cnt

    def simulate(days):
        current_counts = fish_counts

        for day in range(days):
            producing_fish = current_counts[0]
            current_counts = current_counts[1:] + [producing_fish]
            current_counts[6] += producing_fish

        result = sum(current_counts)
        return result

    def simulate_old(days):
        current_fish = initial_fish

        for day in range(days):
            new_fish = [8] * it_ut.count_items(current_fish, lambda x: x == 0)
            current_fish = [6 if f == 0 else f - 1 for f in current_fish] + new_fish
#            print_sample_list("current_fish", current_fish)

        result = len(current_fish)
        return result

    def part1():
        result = simulate(80)
        print_result(result)

    def part2():
        result = simulate(256)
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
