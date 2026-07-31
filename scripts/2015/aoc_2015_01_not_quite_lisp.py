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


from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from utils.quicklambda import _1, _2


@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().replace("(", "1,").replace(")", "-1,").strip(",").split(",")
        parsed = map_list(int, lines)
        return parsed


    def process1(parsed):
        return sum(parsed)

    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        result = process1(parsed)
        print_result(result)

    process2 = process1

    def process2(parsed):
        res = seq(parsed).accumulate().enumerate().find(lambda x: x[1] == -1)
        if res is None:
            return None
        return res[0] + 1

    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
        result = process2(parsed)
#            1796 is too low
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


