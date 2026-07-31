from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
from utils.timer_utils import timefunction

from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
from icecream import ic

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from utils.quicklambda import _1


@timefunction
def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    lines = inp.strip().split('\n')
#    lines = inp.strip("\n").split('\n')
    ic(len(lines))
#    ics(inp)

    def parse_bag(s):
        return " ".join(line.split()[:2])

    bag_rules = {}

    for line in lines:
        key = parse_bag(line)

        remainder = line.split(" contain ")[1]
        rem_bag_parts = remainder.split(",")
        sub_dict = {}

        if not remainder.startswith("no"):
            for rem_bag_part in rem_bag_parts:
                count_parts = rem_bag_part.split()
                count = int(count_parts[0])
                bag_color = " ".join(count_parts[1:3])
                sub_dict[bag_color] = count

        bag_rules[key] = sub_dict

    ics(bag_rules)

        # colr -> containing color
    reverse_rules = defaultdict(list)

    for bag_color, sub_bags in bag_rules.items():
        for sub_bag_color, _ in sub_bags.items():
            reverse_rules[sub_bag_color].append(bag_color)

    ics(reverse_rules)


    def count_containing(bag_color, bag_set=None):
        if bag_set is None:
            bag_set = set()

        containing_colors = reverse_rules.get(bag_color, {})

        for containing_color in containing_colors:
            bag_set.add(containing_color)
            count_containing(containing_color, bag_set)

        return len(bag_set)

    def count_holding(bag_color):
        containing_colors = bag_rules.get(bag_color)

        if not containing_colors:
            return 0

        cnt = 0

        for sub_color, count in containing_colors.items():
            cnt += count * (1 + count_holding(sub_color))

        return cnt

    @timefunction
    def part1():
        result = count_containing("shiny gold")
        print_result(result)

    @timefunction
    def part2():
        result = count_holding("shiny gold")
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
        # needs env var AOC_SESSION
        real_inp = get_aocd_data()
        run(real_inp, True)
#        aocd.submit(my_answer)


main()

