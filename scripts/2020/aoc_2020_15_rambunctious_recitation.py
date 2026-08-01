from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
from utils.timer_utils import timefunction


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
from mini_lambda import s, _


@timefunction
def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    lines = inp.strip().split('\n')
#    lines = inp.strip("\n").split('\n')
    numbers = string_to_integers(inp)

    def determine_turn_number(initial_numbers, end_turn):
#        tracker = defaultdict(int)
        tracker = {}

        for n, num in enumerate(initial_numbers[:-1], 1):
            tracker[num] = n

        last = initial_numbers[-1]

#        ics(tracker, last)

        for turn in count(n+2):
#            new_num = turn - tracker[last]
            new_num = turn - 1 - tracker.get(last, turn - 1)
#            ics(turn, new_num, last, tracker)
            tracker[last] = turn - 1

            if turn == end_turn:
                return new_num

            last = new_num




    @timefunction
    def part1():
#        result = determine_turn_number(numbers, 10)
        result = determine_turn_number(numbers, 2020)
        print_result(result)


    @timefunction
    def part2():
        result = determine_turn_number(numbers, 30000000)
        print_result( result)

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

