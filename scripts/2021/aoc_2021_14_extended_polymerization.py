from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import pyperclip
from icecream import ic
from utils.timer_utils import timefunction

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

#Connection = namedtuple("Connection", "start,")
Point = namedtuple("Point", "x,y")


def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')
    template = inp[0]
    rules = dict(line.split(" -> ") for line in inp[2:])
#    ics(rules)
    test_steps = 10

    @timefunction
    def part1():
        working = template
#        ics(pairwise(working))

        for step in range(test_steps):
            working = working[0] + "".join(rules.get(a+b, "") + b for a, b in pairwise(working))
#            ics(step, working)

        count = Counter(working)
        mc = count.most_common()
        result = mc[0][1] - mc[-1][1]
        print_result(result)

        # works but too slow
    def part2():
        working = template
        ics(working)

        for step in range(40):
            print(".", end="", flush=True)
            working = working[0] + "".join(rules.get(a+b, "") + b for a, b in pairwise(working))
#            ics(step, working)

        count = Counter(working)
        mc = count.most_common()
        result = mc[0][1] - mc[-1][1]
        print_result(result)

    def build_polymer(a, b, step):
        next_step = step - 1
        ab = a + b

        if next_step < 0:
            return b

        insert = rules.get(ab)

        if insert:
            return build_polymer(a, insert, next_step) + build_polymer(insert, b, next_step)

        return b

    @cache
    def build_polymer_cached(a, b, step):
        next_step = step - 1
        ab = a + b

        if next_step < 0:
            return b

        insert = rules.get(ab)

        if insert:
            return build_polymer(a, insert, next_step) + build_polymer(insert, b, next_step)

        return b

    # works but still too slow
    @timefunction
    def part2():
        parts = [template[0]]

        for a, b in pairwise(template):
            parts.append(build_polymer_cached(a, b, test_steps))

        working = "".join(parts)
#        ics(working)
        ics(len(working))

        count = Counter(working)
        mc = count.most_common()
        result = mc[0][1] - mc[-1][1]
        print_result(result)

    def count_polymer(a, b, step, counter):
        next_step = step - 1

        if next_step < 0:
            return

        insert = rules.get(a + b)

        if insert:
            counter[insert] += 1
            count_polymer(a, insert, next_step, counter)
            count_polymer(insert, b, next_step, counter)

    # works but even this is still too slow
    @timefunction
    def part2():
        counter = Counter(template)

        for a, b in pairwise(template):
            count_polymer(a, b, 40, counter)

#        ics(working)

        mc = counter.most_common()
        result = mc[0][1] - mc[-1][1]
        print_result(result)

    @timefunction
    def part2():
        counter = Counter(a+b for a, b in pairwise(template))
        next_counter = counter
        ics(template, counter)

        for step in range(40):
#            ics(step)
            next_counter = Counter()

            for key, cnt in counter.items():
#                ics(key)
                a, b = key
#                ics(a,b)
                insert = rules[key]
                next_counter[a+insert] += cnt
                next_counter[insert+b] += cnt

#            if step < 5:
#            ics(next_counter)

            counter = next_counter

        single_counts = Counter((template[0], template[-1]))

        for key, cnt in counter.items():
#            half_count = cnt/2
            a, b = key
            single_counts[a] += cnt
            single_counts[b] += cnt

        mc = single_counts.most_common()
        result = (mc[0][1] - mc[-1][1]) // 2
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
