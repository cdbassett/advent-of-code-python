from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
from timer_utils import timefunction


from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
from iteration_utilities import return_identity as identity

import pyperclip
from icecream import ic
import aocd # https://github.com/wimglenn/advent-of-code-data
# aocd.lines  # like data.splitlines()
# aocd.numbers # uses regex pattern -?\d+ to extract integers from data


from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from quicklambda import _1


@timefunction
def run(inp, is_real):
    insert_sample_functions(is_real, globals())

    lines = inp.strip().split('\n')
#    lines = inp.strip("\n").split('\n')
    ic(len(lines))
#    w = width(lines)
#    h = height(lines)
#    ic(w, h)
#    ics(inp)
    instructions = seq(lines).map(head_tail).multimap(identity, int)
#    ics(instructions)

    directions = tuple(compass_movements.keys())
#    next_right = seq(compass_movements).pad_back("N").successive(2).to_dict()
#    next_left = seq(compass_movements).pad_back("N").reverse().successive(2).to_dict()


    @timefunction
    def part1():
        facing = "E"
        position = 0, 0
        facing_index = seq(directions).zip_with_index().to_dict()
        ics(facing_index)

        for code, val in instructions:
            if code == "R":
                code, val = "L", -val

            if code == "L":
                facing = directions[(facing_index[facing] - val // 90) % 4]
            else:
                if code == "F":
                    code = facing

                position = add_tuple(position, multiply_scalar_tuple(compass_movements[code], val))

        ic(position)
        result = manhattan((0,0), position)
        print_result(result)



    @timefunction
    def part2():
        position = 0, 0
        waypoint = 10, -1

        for code, val in instructions:
#            ics(position, waypoint, code, val)

            if code == "R":
                code, val = "L", -val

            if code == "F":
                position = add_tuple(position, multiply_scalar_tuple(waypoint, val))
            elif code == "L":
                    # will always result in 0-3
                index = (val // 90) % 4
                wx, wy = waypoint

                for nm in range(index):
                    wx, wy = wy, -wx # rotate 2D vector about origin CW

#                ics(waypoint, val, index, wx, wy)
                waypoint = wx, wy
            else:
                waypoint = add_tuple(waypoint, multiply_scalar_tuple(compass_movements[code], val))

        ic(position)
        result = manhattan((0,0), position)
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

