from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from dataclasses import dataclass
from builtins import pow
import pyperclip
import operator
from icecream import ic
from utils.timer_utils import timefunction
from typing import Callable
from sympy import *

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


# https://adventofcode.com/2022/day/21


def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')

    operations = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
    }

    @dataclass
    class MonkeyOp:
        name: str
        operation: Callable[int, int]
        left: str
        right: str

        def get_val(self):
#            ics(self.operation, self.left, self.right)
            return self.operation(monkeys_by_name[self.left].get_val(), monkeys_by_name[self.right].get_val())


    @dataclass
    class MonkeyNum:
        name: str
        val: int

        def get_val(self):
            return self.val



    all_monkey_parts = [line.split() for line in inp]
    monkeys_by_name = dict()

    for monkey_parts in all_monkey_parts:
        name = monkey_parts[0][:-1]

        match monkey_parts[1:]:
            case [val]:
                monkey = MonkeyNum(name, int(val))

            case [str(left), str(op), str(right)]:
                monkey = MonkeyOp(name, operations[op], left, right)

            case _:
                raise Exception(repr(monkey_parts))

        monkeys_by_name[name] = monkey

    root_monkey = monkeys_by_name["root"]

    @timefunction
    def part1():
        result = int(root_monkey.get_val())
        print_result(result)



    @timefunction
    def part2():
        x = symbols("x")
        human = monkeys_by_name["humn"]
        human.val = x
#        root_monkey.operation = lambda a, b: a == b
        root_monkey.operation = lambda a, b: a - b
#        left = monkeys_by_name[root_monkey.left]
#        right = monkeys_by_name[root_monkey.right]
#        ics(left.get_val())
#        ics(right.get_val())
        equation = root_monkey.get_val()
        ics(equation)

        result = int(solve(equation, x)[0])

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
