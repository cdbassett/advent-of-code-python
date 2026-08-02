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
from mini_lambda import s, _, x


# https://adventofcode.com/2015/day/17


@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().split('\n')
#        ics(lines)
        data = seq(lines).map(int).to_tuple()
#        ics(data)
        return data


    @cache
    def combos(remaining, containers):
        ics(containers, remaining)
        combinations = 0

        for index, container in enumerate(containers):
            if remaining == container:
                combinations += 1
                ics(containers, index, container, remaining)
            elif remaining > container:
#                combinations += combos(remaining - container, del_tuple(containers, index))
                combinations += combos(remaining - container, containers[index+1:]) # further solutions shouldn't use containers we've already checked

        return combinations

    def process1(parsed):
        return combos(150 if is_real else 25, parsed)



    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)
        result = process1(parsed)
        print_result(result)

    process2 = process1


    def process2(parsed):
        found = []

        def combos2(remaining, containers, used=()):
            combinations = 0

            for index, container in enumerate(containers):
                if remaining == container:
                    found.append(used + (container,))
                elif remaining > container:
                    combos2(remaining - container, containers[index+1:], used + (container,)) # further solutions shouldn't use containers we've already checked

        combos2(150 if is_real else 25, parsed)
        ics(found)
#        ics(type(seq(found).min_by(len)))
        found_seq = seq(found)
        min_len = found_seq.min_by(len).len()
        cnt = found_seq.count(lambda f: len(f) == min_len)
        return cnt


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


