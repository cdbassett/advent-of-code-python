from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
from timer_utils import timefunction

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
        return lines

    check_positions = [
        (-1,-1), (0, -1), (1, -1),
        (-1,0),  (1, 0),
        (-1,1), (0, 1), (1, 1),]


    def simulate(arry, steps, skip=set()):
        w, h = width(arry), height(arry)

        def determine_neighbors(arry, x, y):
            xy = x, y
            cur_check_positions = (add_tuple(check_position, xy) for check_position in check_positions)
            l = tuple(yn * w + xn for xn, yn in cur_check_positions if 0 <= xn < w and 0 <= yn < h)
            return l

        def build_neighbor_map(arry):
            seat_map = [[determine_neighbors(arry, x, y) for x in range(w)] for y in range(h)]
            return flatten_2D_array(seat_map)

        neighbors_map = build_neighbor_map(arry)
#        print_sample("arry\n" + "\n".join(arry))

        for step in range(1, steps+1):
            working = flatten_2D_array(arry)
            reference = list(working)

#            if step == 1:
#                print_sample(rebuild_2D_string_array(working, w))

            for seat, c, neighbors in zip(count(), reference, neighbors_map):
                if seat not in skip:
                    occupied_count = sum(1 for neighbor in neighbors if reference[neighbor] == "#")

#                if step == 2:
#                    ics(seat, c, neighbors, occupied_count)

                    if c == "#":
                        if occupied_count not in (2,3):
                            working[seat] = "."
                    else:
                        if occupied_count == 3:
                            working[seat] = "#"

            if step < 6:
                ics(step)
                print_sample("reference\n" +  "\n".join(rebuild_2D_string_array(reference, w)))
                print_sample("working\n" +  "\n".join(rebuild_2D_string_array(working, w)))

            arry = rebuild_2D_string_array(working, w)

        return seq(working).count(_1 == "#")

    def process1(parsed):
        return simulate(parsed, 100 if is_real else 4)

    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)
        result = process1(parsed)
        print_result(result)

    process2 = process1

    def process2(parsed):
        w, h = width(parsed), height(parsed)
        skip = set([0, w-1, w * (h-1), w * h - 1])
        working = flatten_2D_array(parsed)

        for p in skip:
            working[p] = "#"

        arry = rebuild_2D_string_array(working, w)
        return simulate(arry, 100 if is_real else 5, skip)


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
        # needs env var AOC_SESSION
        real_inp = get_aocd_data()
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)


main()

