from functools import *
from collections import *
from itertools import *
from math import *
from dataclasses import dataclass
from builtins import pow
import pyperclip
from icecream import ic
import numpy as np

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


MonkeyData = namedtuple("MonkeyData", "x,y")


@dataclass
class MonkeyData:
    index: int
    items: list[int]
    operation: str
    by: int
    modulo: int
    true_throw: int
    false_throw: int
#    name: str
#    items: list = field(default_factory=list)


def square(old, val, modulo):
#    if old % modulo:
#        return old

    res  =  old ** 2
#    ic("square", old, val, res)
    return res

def add(old, val, modulo):
    res = old + val
#    ic("add", old, val, res)
    return res

def mult(old, val, modulo):
#    if old % modulo and val % modulo:
#        return old

    res =  old * val
#    ic("mult", old, val, res)
    return res


operations = {
    "add": add,
    "square": square,
    "mult": mult,
    }

def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip('\n').split('\n')

    monkey_chunks = list(split_iterable(inp, ""))
#    ics(monkey_chunks)

    def build_monkeys():
        monkeys = []

        for n, monkey_chunk in enumerate(monkey_chunks):
#        items = list(Item(int(w)) for w in monkey_chunk[1].split(":")[1].strip().split(", "))
            items = list(int(w) for w in monkey_chunk[1].split(":")[1].strip().split(", "))
            parts = monkey_chunk[2].split()[-2:]
            by = None
#        ics(parts)

            if parts[0] == "*":
                if parts[1] == "old":
                    operation = "square"
                else:
                    operation = "mult"
                    by = int(parts[1])
            else:
                operation = "add"
                by = int(parts[1])

            modulo = int(monkey_chunk[3].split()[-1])
            true_throw = int(monkey_chunk[4].split()[-1])
            false_throw = int(monkey_chunk[5].split()[-1])
            monkeys.append(MonkeyData(n, items, operation, by, modulo, true_throw, false_throw))

        return monkeys


#    ics(monkeys)

    def monkey_items(monkey):
#        return f"{list(item.worry for item in monkey.items)}"
        return f"{monkey.items}"

    def report_monkeys_items():
        for n, monkey in enumerate(monkeys):
            print(f"Monkey {n}: {monkey_items(monkey)}" )


    def process_monkey1(n, monkey, round):
        activity = len(monkey.items)
        operation = operations[monkey.operation]
#        print(f"Monkey {n}: {monkey_items(monkey)}" )

        for item in monkey.items:
            new_worry = operation(item, monkey.by, monkey.modulo)
            new_worry = new_worry // 3
            throw_to = monkey.true_throw if not new_worry % monkey.modulo else monkey.false_throw
            monkeys[throw_to].items.append(new_worry)

#            if round == 1:
#                ics(item, monkey.operation, monkey.by, new_worry, monkey.modulo, throw_to)
#                print(f"Monkey {n}: {monkey_items(monkey)}" )

        monkey.items = []
        return activity




    def part1():
        monkey_activity = [0] * len(monkeys)
#        report_monkeys_items()

        for round in range(1, 21):
            for n, monkey in enumerate(monkeys):
                monkey_activity[n] += process_monkey1(n, monkey, round)

            ics(round, monkey_activity)
#            report_monkeys_items()

        most_active = sorted(monkey_activity)[-2:]
        result = most_active[0] * most_active[1]
        print_result(result)

    def process_monkey2(n, monkey, round, lcm):
        activity = len(monkey.items)
        operation = operations[monkey.operation]

#        print(f"Monkey {n}: {monkey_items(monkey)}" )

        for item in monkey.items:
            new_worry = operation(item, monkey.by, monkey.modulo)
            new_worry = int(new_worry % lcm)

#            assert new_worry % monkey.modulo == (new_worry % lcm) % monkey.modulo
#            if new_worry % monkey.modulo != (new_worry % lcm) % monkey.modulo:
#                ics(round, n, new_worry, monkey.modulo, new_worry % monkey.modulo, new_worry % lcm, (new_worry % lcm) % monkey.modulo)

            true_throw = not new_worry % monkey.modulo
            throw_to = monkey.true_throw if true_throw else monkey.false_throw
            monkeys[throw_to].items.append(new_worry)

#            if round == 1:
#                ics(item, monkey.operation, monkey.by, new_worry, monkey.modulo, throw_to)
#                print(f"Monkey {n}: {monkey_items(monkey)}" )

        monkey.items = []
        return activity

    def part2():
        lcm_parts = [monkey.modulo for monkey in monkeys]
        ics(lcm_parts)
        lcm = np.lcm.reduce(lcm_parts)
        ics(lcm)
        monkey_activity = [0] * len(monkeys)
#        report_rounds = set([1,20,50] + list(range(100, 1000, 100)) + list(range(1000, 11000, 1000)))
        report_rounds = set([1,20]  + list(range(1000, 11000, 1000)))
        ics(sorted(report_rounds))

        for round in range(1, 10001):
#        for round in range(1, 21):
#        for round in range(1, 1001):

            for n, monkey in enumerate(monkeys):
                monkey_activity[n] += process_monkey2(n, monkey, round, lcm)

            if round in report_rounds:
                ics(round, monkey_activity)

#            report_monkeys_items()

        most_active = sorted(monkey_activity)[-2:]
        result = most_active[0] * most_active[1]
        print_result(result)


#        print_result("Part 2", result)

#
    monkeys = build_monkeys()
    part1()
    monkeys = build_monkeys()
    part2()

def main():
    print("Sample:")
    run(samp_inp, False)

    print("Actual:")
    run(real_inp, True)




samp_inp = r"""
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""

real_inp = r"""
Monkey 0:
  Starting items: 57
  Operation: new = old * 13
  Test: divisible by 11
    If true: throw to monkey 3
    If false: throw to monkey 2

Monkey 1:
  Starting items: 58, 93, 88, 81, 72, 73, 65
  Operation: new = old + 2
  Test: divisible by 7
    If true: throw to monkey 6
    If false: throw to monkey 7

Monkey 2:
  Starting items: 65, 95
  Operation: new = old + 6
  Test: divisible by 13
    If true: throw to monkey 3
    If false: throw to monkey 5

Monkey 3:
  Starting items: 58, 80, 81, 83
  Operation: new = old * old
  Test: divisible by 5
    If true: throw to monkey 4
    If false: throw to monkey 5

Monkey 4:
  Starting items: 58, 89, 90, 96, 55
  Operation: new = old + 3
  Test: divisible by 3
    If true: throw to monkey 1
    If false: throw to monkey 7

Monkey 5:
  Starting items: 66, 73, 87, 58, 62, 67
  Operation: new = old * 7
  Test: divisible by 17
    If true: throw to monkey 4
    If false: throw to monkey 1

Monkey 6:
  Starting items: 85, 55, 89
  Operation: new = old + 4
  Test: divisible by 2
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 7:
  Starting items: 73, 80, 54, 94, 90, 52, 69, 58
  Operation: new = old + 7
  Test: divisible by 19
    If true: throw to monkey 6
    If false: throw to monkey 0
"""

main()


