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

icf = ic.format





@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().split('\n')
        card_pub_key, door_pub_key = map(int, lines)
        return card_pub_key, door_pub_key

    def determine_loop_size(pub_key):
        subject = 7
        value = subject

        for l in count(1):
            value = subject * value % 20201227

            if value == pub_key:
                return l

    def transform(subject, loop_size):
        value = subject

        for l in range(loop_size):
            value = subject * value % 20201227

        return value


    def process1(card_pub_key, door_pub_key):
        card_loop_size = determine_loop_size(card_pub_key)
        door_loop_size = determine_loop_size(door_pub_key)
        ic(card_loop_size, door_loop_size)
        enc1 = transform(card_pub_key, door_loop_size)
        enc2 = transform(door_pub_key, card_loop_size)
        ic(enc1, enc2)
        return enc2

    @timefunction
    def part1(inp):
        card_pub_key, door_pub_key = data_parse(inp)
        result = process1(card_pub_key, door_pub_key)
        print_result(result)


    @timefunction
    def part2(inp):
        pass

    part1(inp1)
#    part2(inp2)

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

