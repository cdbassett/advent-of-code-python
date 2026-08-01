from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import operator
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
#        numbers = map(string_to_integers, lines)
        instructions = seq(lines).map(arrow_splitter).multimap(str.split, identity)
        return instructions


    def int_or_var(num):
        return int(num) if num.isdigit() else num

    circuit = {}

    def process1(parsed):
        circuit.clear()

        for inst, dest in parsed:
            match inst:
                case [num]:
                    circuit[dest] = identity, [int_or_var(num)]

                case "NOT", src:
                    circuit[dest] = operator.inv, [src]

                case a, "AND", b:
                    circuit[dest] = operator.and_, [int_or_var(a), b]

                case a, "OR", b:
                    circuit[dest] = operator.or_, [int_or_var(a), b]

                case a, "LSHIFT", cnt:
                    circuit[dest] = operator.lshift, [a, int(cnt)]

                case a, "RSHIFT", cnt:
                    circuit[dest] = operator.rshift, [a, int(cnt)]

        ics(circuit)
        ic(len(circuit))
        return circuit

    @cache
    def evaluate(key):
        next = circuit.get(key)

        if next is None:
            return key

        func, sources = next
        args = tuple(evaluate(src) for src in sources)

        try:
            res = func(*args)
        except:
            ic(func, sources, args)
            raise

        return res




    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)
        process1(parsed)
        evaluate.cache_clear()

        if is_real:
            result = evaluate("a")
        else:
            result = evaluate("f")

        print_result(result)

    process2 = process1

#    def process2(parsed):

    @timefunction
    def part2(inp):
        if is_real:
            parsed = data_parse(inp)
            ics(parsed)
            process1(parsed)
            a_val = evaluate("a")
            evaluate.cache_clear()
            circuit["b"] = identity, [a_val]
            result = evaluate("a")
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


