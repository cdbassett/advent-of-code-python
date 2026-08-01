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

def run(inp, is_real):
    insert_sample_functions(is_real, globals())

    inp = inp.strip().split('\n')
    segments = [tuple(map(int, (v for p in line.split(" -> ") for v in p.split(",")))) for line in inp]
    print_list("segments", segments)

    def get_step(a1, a2):
        diff = a2 - a1
        return diff // abs(diff)


    def get_range(a1, a2):
        if a1 > a2:
            result = range(a1, a2 - 1, -1)
        elif a2 > a1:
            result = range(a1, a2 + 1)
        else:
            result = repeat(a1)
#        print_sample(f"    get_range({a1}, {a2}): {list(result)}")
        return result


    def get_line_range(segment):
        x1, y1, x2, y2 = segment
#        result = list(product(get_range(x1, x2), get_range(y1, y2)))
#        x_range = list(get_range(x1, x2))
#        y_range = list(get_range(y1, y2))
        result = list(zip(get_range(x1, x2), get_range(y1, y2)))
#        print_sample(f"    get_line_range({segment}): {result}")
        return result

    def count_hits(hits, segment, diags):
        def add_hit(*p):
            hits[p] += 1
#            print_sample(f"hit: ({p})")

        x1, y1, x2, y2 = segment

        if diags or x1 == x2 or y1 == y2:
            for x, y in get_line_range(segment):
                add_hit(x, y)

    def part1():
        hits = Counter()

        for segment in segments:
            count_hits(hits, segment, False)

#        print_sample_list("hits", hits)
        multi_hits = [hit for hit, count in hits.items() if count > 1]
#        print_sample_list("multi_hits", multi_hits)
        result = len(multi_hits)
        print_result(result)

    def part2():
        hits = Counter()

        for segment in segments:
            count_hits(hits, segment, True)

#        print_sample_list("hits", hits)
        multi_hits = [hit for hit, count in hits.items() if count > 1]
#        print_sample_list("multi_hits", multi_hits)
        result = len(multi_hits)
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
