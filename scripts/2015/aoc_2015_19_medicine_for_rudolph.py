from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
from utils.timer_utils import timefunction

from colorama import Fore, Style
from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
from icecream import ic

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from utils.quicklambda import _1, _2


# https://adventofcode.com/2015/day/19


@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().split('\n')
        pair_lines, [medicine] = split_iterable(lines, "")
        pairs = seq(pair_lines).map(double_arrow_splitter).to_list()
        return medicine, pairs

    def replacements(inp, before, after):
        index = 0

        for step in count():
            pos = inp.find(before, index)

            if pos < 0:
                return

            index = pos + 1
            out = out = inp[:pos] + after + inp[pos+len(before):]

            yield out
            ics(inp, step, out, before, after, index)


    def process1(parsed):
        medicine, pairs = parsed
        found = set()

        for a, b in pairs:
            for derived in replacements(medicine, a, b):
                found.add(derived)

        return len(found)

    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)
        result = process1(parsed)
        print_result(result)

    process2 = process1

    # worked for sample but runs out of memory for real
    def process2_old(parsed):
        medicine, pairs = parsed

        def get_derivations(current):
            for a, b in pairs:
                yield from replacements(current, b, a)

        queue = []
        put, get = get_queue_functions_smallest(queue)
        put((0, medicine, (medicine,)))
        found = 0

        while queue and not found:
#            iterations += 1
            steps, current, path = get()

            for derived in get_derivations(current):
                if derived == "e":
                    found = steps + 1
                    ics(path + (derived,))
                    break

                put((steps + 1, derived, path + (derived,)))



        return found
# TODO: takes too long
    def process2(parsed):
        medicine, pairs = parsed
        pairs_by_length = sorted(((len(b), b, a) for a, b in pairs), reverse=True)
        working = medicine
        steps = 0

        while working != "e":
            for l, b, a in pairs_by_length:
                before = working
                working = working.replace(b, a, 1)

                if working != before:
                    steps += 1
                    continue # start back over once we've changed to allow longer chains another chance

        return steps


    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
        result = process2(parsed)
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
        real_inp = get_aocd_data()
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)


main()

