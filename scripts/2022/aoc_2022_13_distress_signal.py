from functools import *
from collections import *
from collections.abc import Iterable
from itertools import *
from math import *
from statistics import *
from builtins import pow
import pyperclip
from icecream import ic
import iteration_utilities as it_ut
from utils.timer_utils import timefunction
import matplotlib.pyplot as plt

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


# https://adventofcode.com/2022/day/13


def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')

    pairs = [tuple(eval(line) for line in lines) for lines in split_iterable(inp, "")]
    ics(pairs)

    def packets_are_in_order_recurse(l1, l2):
#        ics("packets_are_in_order_recurse", l1, l2)
        l1_is_list = isinstance(l1, Iterable)
        l2_is_list = isinstance(l2, Iterable)

        if l1_is_list and l2_is_list:
#            if len(l1) > len(l2):
#                ics(len(l1), len(l2))
#                return False

            for e1, e2 in zip_longest(l1, l2):
                if e2 is None:
#                    ics(e2)
                    return 1

                if e1 is None:
#                    ics(e1)
                    return -1

                res = packets_are_in_order_recurse(e1, e2)
#                ics(res)

                if res > 0:
#                    ics(e1, e2)
                    return res

                if res < 0:
                    return res

#            ics("equal")
            return 0

        elif l1_is_list and not l2_is_list:
            return packets_are_in_order_recurse(l1, [l2])
        elif l2_is_list and not l1_is_list:
            return packets_are_in_order_recurse([l1], l2)
        else:
#            ics(l1, l2, l1 - l2)
            return l1 - l2

        assert False
        return True

    def packets_are_in_order(l1, l2):
        return packets_are_in_order_recurse(l1, l2) <= 0

#    ics(magnitude(build_number_recurse([9,1])))
    def part1():
        packets_and_order = [(p, packets_are_in_order(p[0], p[1])) for p in pairs]
        ics(packets_and_order)
        in_order_indices = [n for n, (p, o) in enumerate(packets_and_order, 1) if o]
        ics(in_order_indices)
        result = sum(in_order_indices)
        print_result(result)

    def part2():
        sort_key = cmp_to_key(packets_are_in_order_recurse)
        sorted_packets = sorted(list(it_ut.flatten(pairs)) + [[[2]], [[6]]], key = sort_key)
        ics(sorted_packets)
        packet_strings = [str(p) for p in sorted_packets]
        packets_by_string = dict((s, n) for n, s in enumerate(packet_strings, 1))
        div1_index = packets_by_string[str([[2]])]
        div2_index = packets_by_string[str([[6]])]
        result = div1_index * div2_index
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
