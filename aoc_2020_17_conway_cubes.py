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
from mini_lambda import s, _


@timefunction
def run(inp1, inp2, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    def data_parse(inp, build_point):
#        lines = inp.strip().split('\n')
        lines = inp.strip("\n").split('\n')
        w, h = width(lines), height(lines)
        ic(w, h)
        space = set()

        for y, line in enumerate(lines, -(h // 2)):
            for x, c in enumerate(line, -(w // 2)):
                if c == "#":
                    space.add(build_point(x, y))

        ic(len(space))
        ics(space)
        return lines, space


    def process(lines, space, stages, dimensions):
            # allows iterating through all dimensions without needing recursing or nested loop
        all_directions = list(product((-1, 0, 1), repeat=dimensions))
        all_directions.remove((0,) * dimensions)
#        ics(all_directions)

        ranges = [3] * dimensions
        ranges[0:2] = [width(lines) + 2, height(lines) + 2] # x and y have multiple, z and w have one (initially), then +1 in each direction
        ranges = tuple(ranges)
        ics(ranges)
        range_increase = (2,) * dimensions # each pass extends blocks we have to check by one in each direction


        if 1:
            for step in range(1, stages+1):
                new_space = set(space)
#                ics(step, len(new_space))
                cur_ranges = list(product(*[range(-(r//2), r//2+1) for r in ranges]))
#                ics(cur_ranges)

                for coord in cur_ranges:
                    was_active = coord in space
                    check_coords = seq(all_directions).map(partial(add_tuple, coord)).to_set()
#                    ics(coord, check_coords)
                    active_neighbors = len(check_coords.intersection(space))
                    is_active = was_active

                    if was_active:
                        if active_neighbors not in (2,3):
                            new_space.remove(coord)
                    else:
                        if active_neighbors == 3:
                            new_space.add(coord)

#                    is_active = coord in new_space
#                    wa, ia, an = was_active, is_active, active_neighbors
#                    ics(coord, wa, ia, an)

                ranges = add_tuple(ranges, range_increase)
                space = new_space
                ics(step, len(space))

#            ics(space)

        return len(space)



    @timefunction
    def part1(inp):
        lines, space = data_parse(inp, lambda x, y: (x, y, 0))
        result = process(lines, space, 6, 3)
        print_result(result)


    @timefunction
    def part2(inp):
        lines, space = data_parse(inp, lambda x, y: (x, y, 0, 0))
        result = process(lines, space, 6, 4)
        print_result(result)

    part1(inp1)
    part2(inp2)

def main():
    if 1:
        if samp_inps:
            for samp_inp in samp_inps:
                print(f"{Fore.GREEN}{Style.BRIGHT}Sample:{Style.RESET_ALL}")
                run(samp_inp1, samp_inp2, False)
        else:
            print(f"{Fore.BLUE}{Style.BRIGHT}Sample:{Style.RESET_ALL}")
#            print("Sample:")
            run(samp_inp1, samp_inp2, False)

    if 1:
        print(f"{Fore.YELLOW}{Style.BRIGHT}Actual:{Style.RESET_ALL}")
#        print("Actual:")
            # needs env var AOC_SESSION
        real_inp = aocd.data # supposed to work if filename is clear enough (year would need to be 4-digit)
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)




samp_inp1 = r"""
.#.
..#
###
"""

samp_inp2 = samp_inp1


short_samp = """
"""


samp_inps = [
#    short_samp,
#    samp_inp,
    ]


main()

