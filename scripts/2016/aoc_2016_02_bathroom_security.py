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
import pyperclip
from icecream import ic
import aocd # https://github.com/wimglenn/advent-of-code-data
# aocd.lines  # like data.splitlines()
# aocd.numbers # uses regex pattern -?\d+ to extract integers from data


from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from utils.quicklambda import _1, _2



@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().split('\n')
        return lines


    def process(directions, keypad, start):
        pos = start
        keys = []

        for line in directions:
            for dir in line:
                adjust = vertical_movements[dir]
                new_pos = add_tuple(pos, adjust)

                if new_pos in keypad:
                    pos = new_pos

            keys.append(keypad[pos])

        return sjoin(keys)

    def process1(parsed):
        keypad = seq.range(1,10).map(str).grouped(3).to_list()
        keypad = dict(((x,y), keypad[y][x]) for x, y in product(range(3), range(3)))
        ics(keypad)
        start = 1, 1

        return process(parsed, keypad, start)


    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)
        result = process1(parsed)
        print_result(result)

    process2 = process1

    def process2(parsed):
        keypad = {
            (2, 0): "1",
            (2, 4): "D",
            }
        keypad.update(((n+1, 1), str(n+2)) for n in range(3))
        keypad.update(((n, 2), str(n+5)) for n in range(5))
        keypad.update(((n+1, 3), c) for n, c in zip(range(3), "ABC"))
        ics(keypad)
        start = 0, 2

        return process(parsed, keypad, start)


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

