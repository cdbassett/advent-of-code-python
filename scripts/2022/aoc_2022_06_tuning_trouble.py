from functools import *
from collections import *
from itertools import *
from math import *
from builtins import pow
import pyperclip
from icecream import ic
import iteration_utilities as it_ut

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip('\n').split('\n')
    signal = inp[0]

    def part1():
        l = 4
#        chunks = list(it_ut.successive(signal, times = l))

        for n, chunk in enumerate(it_ut.successive(signal, times = l)):
            if len(set(chunk)) == l:
                print_result(n + l)
                break


#        for n in range(l - 1, len(signal) - l + 1):
#            if len(set(signal[n-l:n])) == l:
#                print_result(n)
#                break


    def part2():
        l = 14
        for n, chunk in enumerate(it_ut.successive(signal, times = l)):
            if len(set(chunk)) == l:
                print_result(n + l)
                break


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
