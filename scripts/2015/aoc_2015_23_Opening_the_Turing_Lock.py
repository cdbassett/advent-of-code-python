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
from quicklambda import _1, _2



@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().replace(",", "").split('\n')
        parsed = map_list(str.split, lines)
        return parsed


    idx = {
        "a": 0,
        "b": 1,
        "ip": 2,
        }

    a = 0
    b = 1
    ip = 2

    def jmp(state, *args):
        state[ip] += int(args[0]) - 1

    def jie(state, *args):
        if not state[idx[args[0]]] & 1:
            jmp(state, args[1])

    def jio(state, *args):
        if state[idx[args[0]]] == 1:
            jmp(state, args[1])

    def tpl(state, *args):
        state[idx[args[0]]] *= 3

    def inc(state, *args):
        state[idx[args[0]]] += 1

    def hlf(state, *args):
        state[idx[args[0]]] //= 2

    d = locals()
    functions = dict((s, d[s]) for s in "jmp,jio,jie,hlf,tpl,inc".split(","))


    def process_instructions(instructions, start_a=0):
        state = [0] * 3
        state[a] = start_a
        inst_len = len(instructions)
        ic(inst_len)

        while state[ip] < inst_len:
            op, *args = instructions[state[ip]]
            ics(state, op, args)
            state[ip] += 1
            functions[op](state, *args)

        ics(state)
        return state[b]

    def process1(parsed, start_a=0):
        return process_instructions(parsed, start_a)

    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)
        result = process1(parsed)
        print_result(result)

    process2 = process1


    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
        result = process2(parsed, 1)
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

