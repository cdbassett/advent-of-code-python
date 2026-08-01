from functools import *
from collections import *
from itertools import *
from math import *
from builtins import pow
import pyperclip
from icecream import ic
import numpy as np

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

def run(inp, is_real):
    insert_sample_functions(is_real, globals())

    inp = inp.strip().split('\n')
    directions = inp

    def part1():
        position = np.array([0, 0]) # horiz, depth
        adjust = {
            "forward": np.array((1, 0)),
            "down": np.array((0, 1)),
            "up": np.array((0, -1)),
            }

        for line in directions:
            d, val = line.split(" ")
            val = int(val)
#            position = list(a + b * val for a, b in zip(position, adjust[d]))
            position += adjust[d] * val
#            print_sample_list("position", position)

        result = int(position[0] * position[1])
        print_result(result)

    def part2():
        position = np.array([0, 0, 0]) # horiz, depth, aim
        adjust = {
            "forward": np.array((1, 1, 0)),
            "down": np.array((0, 0, 1)),
            "up": np.array((0, 0, -1)),
            }

        depth = np.array([0, 1, 0]) # horiz, depth, aim
        aim = np.array([0, 0, 1]) # horiz, depth, aim
        pos_only = np.array([1, 1, 0]) # horiz, depth, aim
        horiz_and_aim = np.array([1, 0, 1]) # horiz, depth, aim

        for line in directions:
            d, val = line.split(" ")
            val = int(val)
            adjustment = adjust[d]
            position += adjustment * horiz_and_aim * val + depth * adjustment * val * position[2]
            ics(position)

        result = int(position[0] * position[1])
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
