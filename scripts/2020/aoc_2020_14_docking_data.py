from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
from timer_utils import timefunction

from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
import pyperclip
from icecream import ic

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from mini_lambda import s, _


def and_mask(mask):
    return int(mask.replace("X", "1"), base=2)

def or_mask(mask):
    return int(mask.replace("X", "0"), base=2)

def build_and_and_or_masks(mask):
    return and_mask(mask), or_mask(mask)

def count_xs(mask):
    return len(mask.replace("1", "").replace("0", ""))

def mem_parse(mems):
    return tuple(tuple(map(string_to_integers, mem)) for mem in mems)

def build_floating_masks(mask):
    x_indexes = [n for n, c in enumerate(mask) if c == "X"]
    return tuple(reversed(x_indexes)), or_mask(mask)



@timefunction
def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    lines = inp.strip().split('\n')
#    lines = inp.strip("\n").split('\n')
    splitter = partial(str.split, sep=" = ")
    ic(len(lines))
    instructions = seq(lines).map(splitter).groupby_no_key(_(s[0] =="mask")).grouped(2)
    ics(list(instructions.slice(0, 4)))

    @timefunction
    def part1():
        parsed = []

        for masks, mems in instructions:
            parsed.append((build_and_and_or_masks(masks[0][1]), mem_parse(mems)))

        ics(parsed[:4])
        memory = defaultdict(int)

        for (and_mask, or_mask), mems in parsed:
            ics(bin(and_mask), bin(or_mask), len(bin(and_mask)))

            for addr, val in mems:
                new_val = (val & and_mask) | or_mask
                ics(addr, val, new_val)
                memory[addr] = new_val

        ics(memory)
        result = sum(memory.values())
        print_result( result)


    def possible_addresses(mask, floating_mask, addr):
        x_indexes, or_mask_val = floating_mask
        addr = addr | or_mask_val
        addr_str = list(f'{addr:036b}') # base address as list of chars of binary value
#        ics(x_indexes)
#        ics(bin(or_mask_val), sjoin(addr_str))

        for floating_addr in range(1 << count_xs(mask)):
            binstr = f'{floating_addr:036b}'
#            ics(floating_addr, binstr)
    #        sjoin(binstr[x_index] for x_index in x_indexes)
            for n, x_index in enumerate(x_indexes):
#                ics("", x_index, -n-1, binstr[-n-1])
                addr_str[x_index] = binstr[-n-1]

#            ics(sjoin(addr_str))
            single_addr = int(sjoin(addr_str), base=2)
#            ics(single_addr)
            yield single_addr

    @timefunction
    def part2():
        parsed = []

        for masks, mems in instructions:
            parsed.append((masks[0][1], mem_parse(mems)))

#        ic(sum(1 << count_xs(m[0]) for m in parsed))
#        ics(parsed[:4])
        memory = defaultdict(int)

        for mask, mems in parsed:
            floating_mask = build_floating_masks(mask)

            for addr, val in mems:
                for possible_address in possible_addresses(mask, floating_mask, addr):
                    memory[possible_address] = val

#        ics(memory)
        result = sum(memory.values())
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

