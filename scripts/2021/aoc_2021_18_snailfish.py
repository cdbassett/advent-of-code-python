from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from dataclasses import dataclass
from builtins import pow
import pyperclip
from icecream import ic
import iteration_utilities as it_ut
import copy
from timer_utils import timefunction
import matplotlib.pyplot as plt

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


@dataclass
class RegNum: # actually used
    v: int


def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')

    def build_number_recurse(l):
        for n, e in enumerate(l):
            if isinstance(e, int):
                l[n] = RegNum(e)
            else:
                build_number_recurse(e)

        return l

    def build_number(line):
        l = eval(line)
        build_number_recurse(l)
        return l

    def simple_numbers_recurse(l):
#        if not isinstance(l, RegNum):
        for n, e in enumerate(l):
            if isinstance(e, RegNum):
                l[n] = e.v
            else:
                simple_numbers_recurse(e)

        return l

    def simple_numbers(number):
        num_copy = copy.deepcopy(number)
        simple_numbers_recurse(num_copy)
        return num_copy

    numbers = [build_number(line) for line in inp]

#    for line in inp:
#        number = eval(line)
#        numbers.append(number)
    """
        1) represent as tree with a node class with left and right (and parent?)
            explode: hold onto prev value while recursing, grab next value
        2) represent as nested lists with a number class
            explode: hold onto prev value while recursing, grab next value
    """


    ics(list(simple_numbers(n) for n in numbers))



    def explode_recurse(l, parent, level):
#        ics("explode_recurse", level, simple_numbers(l))
#        ics("explode_recurse", level, l)

        if level == 4:
            assert isinstance(l[0], RegNum) and isinstance(l[1], RegNum)
#            ics("exploding", level, simple_numbers(l))
            return l

        for n, e in enumerate(l):
            if not isinstance(e, RegNum):
                result = explode_recurse(e, l, level+1)

                if result:
                    if level == 3:
                        replacement = RegNum(0)
                        l[n] = replacement
                        return result, replacement

                    return result

    def explode(number):
        result = explode_recurse(number, None, 0)

        if result:
            old, replacement = result
            flattened = list(it_ut.deepflatten(number))
#            ics(simple_numbers(flattened))

            index = first(n for n, item in enumerate(flattened) if item is replacement)
#            index = flattened.index(replacement)
#            ics(index, len(flattened))
            assert flattened[index] is replacement

            if index > 0:
                flattened[index - 1].v += old[0].v

            if index < len(flattened) - 1:
                flattened[index + 1].v += old[1].v

#            ics("after explode", simple_numbers(flattened))
#            ics("after explode", simple_numbers(number))
            return True



    def split(l):
        for n, e in enumerate(l):
            if isinstance(e, RegNum):
                if e.v >= 10:
                    l[n] = [RegNum(e.v // 2), RegNum(ceil(e.v / 2))]
                    return True
            else:
                if split(e):
                    return True


    def reduce_snail(number):
        while True:
            if explode(number):
#                ics("exploded", simple_numbers(number))
                continue

            if split(number):
#                ics("split", simple_numbers(number))
                continue

            break

#        ics("reduced", simple_numbers(number))
        return number

    def add(number1, number2):
        added = [copy.deepcopy(number1), copy.deepcopy(number2)]
#        ics(simple_numbers(added))
        return reduce_snail(added)

    def magnitude(number):
#        ics(number)

        if isinstance(number, RegNum):
            return number.v

        return magnitude(number[0]) * 3 + magnitude(number[1]) * 2


#    ics(magnitude(build_number_recurse([9,1])))
#    ics(magnitude(build_number_recurse([[[[0,7],4],[[7,8],[6,0]]],[8,1]])))
#    ics(magnitude(build_number_recurse([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]])))

#    ics(reduce(build_number()))
#    ics(simple_numbers(add(numbers[0], numbers[1])))
#    ics(simple_numbers(add(numbers[0], numbers[1])))


    # -n**2/2 + (iv + 1/2)*n = m_min
#    ic(bits_used)
#    ics(packets)

#    @timefunction
    def part1():
        added = reduce(add, numbers)
        result = magnitude(added)
        print_result(result)

    def part2():
#        ics([(simple_numbers(num1), simple_numbers(num2)) for num1, num2 in permutations(numbers, 2)])
        adds = [(add(num1, num2), simple_numbers(num1), simple_numbers(num2)) for num1, num2 in permutations(numbers, 2)]
        magnitudes = [(magnitude(added), simple_numbers(added), num1, num2) for added, num1, num2 in adds]
#        ics(sorted(magnitudes))
        result = max(mag for mag, added, num1, num2 in magnitudes)
#        result = max(magnitude(add(num1, num2)) for num1, num2 in permutations(numbers, 2))
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
