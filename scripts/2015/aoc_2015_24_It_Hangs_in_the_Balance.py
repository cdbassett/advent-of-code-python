from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
from timer_utils import timefunction
from bisect import bisect_right


import sympy

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
from quicklambda import _1, _2


@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().split('\n')
        parsed = map_list(int, lines)
        return parsed

#    @cache
#    def get_worst_factors(missing, remainder, max_count):
#        all_divisors = sympy.divisors(missing)
#        divisors = [n for n in all_divisors if n in remainder]
#        rem = [n for n in remainder if n in divisors]
#        ics(remainder)
#        ics(missing, divisors, rem, max_count, all_divisors)
#        ics(list(reversed(range(2, len(divisors)))))
#        p = prod(divisors)
#
#            # seems very unlikely that all possible divisors are factors of missing, but just in case
#        if p == missing and p in remainder:
#            ic("result", p)
#            return p
#
#        for n in reversed(range(2, min(max_count, len(divisors)))):
#            possible =[prod(v) for v in combinations(divisors, n) if sum(v) == missing]
#
#            if possible:
#                ic("result", possible)
#                return max(possible)
#
#        if missing in remainder:
#            ic("result", missing)
#            return missing
    @cache
    def predict_qe(missing, remainder, max_count):
        all_divisors = sympy.divisors(missing)
        divisors = [n for n in all_divisors if n in remainder]
        rem = [n for n in remainder if n in divisors]
        ics(remainder)
        ics(missing, divisors, rem, max_count, all_divisors)
#        ics(list(reversed(range(2, len(divisors)))))
        p = prod(divisors)

            # seems very unlikely that all possible divisors are factors of missing, but just in case
        if p == missing and p in remainder:
            ic("result", p)
            return p

        for n in reversed(range(2, min(max_count, len(divisors)))):
            possible =[prod(v) for v in combinations(divisors, n) if sum(v) == missing]

            if possible:
                ic("result", possible)
                return max(possible)

        if missing in remainder:
            ic("result", missing)
            return missing



        # all groups must weigh the same
        # first group must have fewest packages
        # first group must have lowest QE (product) of choices

        # theoretically best first group will always contain highest value:
        #   has to be possible, because some group has to have it
        #   the higher the number, the lower the remainder can be, the more lopsided, thus a smaller product than more even numbers

        # don't need to calculate all groups, other than possibly making sure that some configuration is possible
        # was barking up the wrong tree here, running out of memory, and predict_qe was finding factors instead of addends
    def process1(parsed, group_count = 3):
        assert sum(parsed) % group_count == 0
        ic(len(parsed))
        max_pkg = len(parsed) // group_count # the most packages first group should have
        group_weight = sum(parsed) // group_count
        ic(max_pkg, group_weight)
        first, *remainder = sorted(parsed, reverse=True)

        queue = []
        put, get = get_queue_functions_smallest(queue) # len, product, groups, remaining packages
#        put((1, first, (first,), tuple(sorted(remainder))))
        put((0, 0, (), tuple(sorted(parsed))))

        while queue:
            l, qe, first_group, remainder = get()
            fgl = len(first_group)
            sum_group = sum(first_group)

                # do it here rather than before putting in queue to allow other possibilities to precede
            if sum_group == group_weight:
                ic(first_group)
                return prod(first_group)

            if fgl >= max_pkg:
                continue

            balance = group_weight - sum_group

                # if we have one package that perfectly fills remainder, we want to use it as aanything welse would mean a higher number of packages
            idx = binary_search(remainder, balance)

            if idx >= 0:
                p = remainder[idx]
                new_first_group = first_group + (p,)
                qe = prod(new_first_group)
                new_remainder = del_index(remainder, idx)
                put((max_pkg, qe, new_first_group, new_remainder))
            elif fgl == max_pkg - 1:
                    # if only one slot remaining, only the exact amount will work
                continue


#            if is_sample:
#                idx = bisect_right(remainder, balance)
#                ics(balance, idx, len(remainder), remainder, remainder[:idx])

            fgl = len(first_group) + 1

            for idx in range(bisect_right(remainder, balance)):
                if 1:
                    p = remainder[idx]
                    assert p <= balance

#            for idx, p in enumerate(remainder):
#                if p <= balance:
                    new_first_group = first_group + (p,)
                    qe = prod(new_first_group)
                    new_remainder = del_index(remainder, idx)
                    missing = balance - p
#                    put((len(new_first_group), qe, new_first_group, new_remainder))
#                    put((max_pkg if missing else len(new_first_group), qe * missing if missing else qe, new_first_group, new_remainder))

                    predicted_qe = qe

                    if missing:
                        #                        ics(remainder)
                        if fgl == max_pkg - 1:
                            predicted_qe = qe * missing
                        else:
                            worst_remaining = predict_qe(missing, remainder, max_pkg - fgl)

                            if worst_remaining is None:
                                continue

                            predicted_qe = qe * worst_remaining



                    put((max_pkg if missing else fgl, predicted_qe, new_first_group, new_remainder))





#        for p in permutations(parsed):
#            groups = list(batched(p), group_count)

        return 0

#    ics(binary_search_reverse([5, 4, 2, 0], 4))
#    ics(binary_search_reverse([5, 4, 2, 0], 3))
#    ics(binary_search_reverse([5, 4, 2, 0], 0))
#    ics(binary_search_reverse([5, 4, 2, 0], 6))

    @cache
    def find_fit(remainder, need):
            # only iterate through packages that are at or below our reamining needed weight
            # start with biggest first
        for idx in reversed(range(bisect_right(remainder, need))):
            p = remainder[idx]

            if p == need:
                return (p,)

            use_group = find_fit(del_index(remainder, idx), need - p)

            if use_group is not None:
                return (p,) + use_group



        # all groups must weigh the same
        # first group must have fewest packages
        # first group must have lowest QE (product) of equal length choices

        # theoretically best first group will always contain highest value:
        #   has to be possible, because some group has to have it
        #   the higher the number, the lower the remainder can be, the more lopsided, thus a smaller product than more even numbers

        # don't need to calculate all groups, other than possibly making sure that some configuration is possible
        # this worked for part 1 but not part2
    def process1(parsed, group_count = 3):
        assert sum(parsed) % group_count == 0
        ic(len(parsed))
        max_pkg = len(parsed) // group_count # the most packages first group should have
        group_weight = sum(parsed) // group_count
        ic(max_pkg, group_weight)

        first_group = find_fit(tuple(sorted(parsed)), group_weight)
        ic(first_group)
        ic(sum(first_group))
        return prod(first_group)

        # all groups must weigh the same
        # first group must have fewest packages
        # first group must have lowest QE (product) of equal length choices

        # theoretically best first group will always contain highest value:
        #   has to be possible, because some group has to have it
        #   the higher the number, the lower the remainder can be, the more lopsided, thus a smaller product than more even numbers

        # don't need to calculate all groups, other than possibly making sure that some configuration is possible
    def process1(parsed, group_count = 3):
        assert sum(parsed) % group_count == 0
        ic(len(parsed))
        max_pkg = len(parsed) // group_count # the most packages first group should have
        group_weight = sum(parsed) // group_count
        ic(max_pkg, group_weight)

        for n in range(1, max_pkg):
            qes = [prod(x) for x in combinations(parsed, n) if sum(x) == group_weight]

            if qes:
                return min(qes)





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
        result = process2(parsed, 4)
        # 139699414 is too high
        print_result(result)

    part1(inp1)
    part2(inp2)

def main():
    example = get_aocd_example()
    samp_inps = split_example(example)

    for n, samp_inp in enumerate(samp_inps, 1):
        print(f"{Fore.BLUE}{Style.BRIGHT}Sample {n}:{Style.RESET_ALL}")
        run(samp_inp, samp_inp, False)

    if 1:
        print(f"{Fore.BLUE}{Style.BRIGHT}Actual:{Style.RESET_ALL}")
        # needs env var AOC_SESSION
        real_inp = get_aocd_data()
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)


main()

