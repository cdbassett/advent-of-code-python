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
    for samp_inp in samp_inps:
        print("Sample:")
        run(samp_inp, False)

    print("Actual:")
    run(real_inp, True)




samp_inp = r"""
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""

if 0:
    """
    [[[[4,3],4],4],[7,[[8,4],9]]]
    [1,1]
    """,
    """
    [1,1]
    [2,2]
    [3,3]
    [4,4]
    """,
    """
    [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
    [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
    [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
    [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
    [7,[5,[[3,8],[1,4]]]]
    [[2,[2,2]],[8,[8,1]]]
    [2,9]
    [1,[[[9,3],9],[[9,0],[0,7]]]]
    [[[5,[7,4]],7],1]
    [[[[4,2],2],6],[8,7]]
    """,
    """
    [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
    [[[5,[2,8]],4],[5,[[9,9],0]]]
    [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
    [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
    [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
    [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
    [[[[5,4],[7,7]],8],[[8,3],8]]
    [[9,3],[[9,9],[6,[4,9]]]]
    [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
    [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
    """,

samp_inps = [
    samp_inp
    ]



real_inp = r"""
[[5,[[8,5],8]],[[9,3],[0,3]]]
[[[8,[3,6]],[0,[1,2]]],[[[4,1],4],[7,[5,8]]]]
[[[[2,0],6],[4,8]],[8,[3,0]]]
[[[[8,2],[8,3]],[[0,9],5]],3]
[[[[4,4],[2,3]],8],[[1,[3,8]],[8,4]]]
[[[2,[1,0]],[[3,2],0]],[9,2]]
[[[0,4],[[9,8],[6,6]]],3]
[[[6,[6,2]],[[4,5],3]],[0,7]]
[[[[2,8],4],[[1,2],[3,8]]],9]
[[[3,[7,6]],[9,9]],[[8,9],[[6,2],[3,4]]]]
[0,[4,[[4,1],8]]]
[[[[3,3],[8,7]],[9,7]],[[7,6],4]]
[[1,[[0,6],4]],[[5,[3,3]],6]]
[[[0,4],7],4]
[[[2,[1,7]],8],[6,[2,[8,7]]]]
[[[9,7],[[2,5],[7,9]]],[1,[4,[8,6]]]]
[[[[3,7],6],[[1,6],[5,4]]],[0,[6,2]]]
[9,5]
[[[[6,1],[4,5]],[[4,2],8]],[[5,[5,1]],[[7,3],6]]]
[9,[9,[[7,4],[6,9]]]]
[3,[[9,2],9]]
[[[[1,7],6],[3,[9,7]]],[[6,[4,3]],[[5,6],5]]]
[[[[0,6],[7,9]],[[2,8],2]],[5,[3,[4,9]]]]
[0,[[[1,8],7],[9,4]]]
[5,[0,[[4,5],6]]]
[[[[7,9],[4,9]],[7,[7,5]]],[6,[[1,6],[8,7]]]]
[[[4,[0,1]],[[9,0],[8,1]]],[[0,7],[5,[0,4]]]]
[0,1]
[[[[7,7],[0,7]],8],[[3,[4,2]],[6,6]]]
[[[[7,8],[4,3]],[7,[7,0]]],[3,[2,3]]]
[[[[6,9],[3,2]],[[4,7],2]],[[3,[7,5]],[[3,3],3]]]
[7,[[[6,7],[1,3]],9]]
[[[[2,9],[2,1]],[3,[9,9]]],[1,[[0,7],[2,4]]]]
[[7,4],[[[0,0],5],[[2,4],5]]]
[[[[2,9],8],[3,4]],[6,[[8,7],[4,3]]]]
[[[8,3],0],[4,[[6,7],5]]]
[[[6,[4,1]],[[1,1],[0,4]]],[[[6,2],[8,6]],[5,2]]]
[9,[[[5,6],0],[[7,2],3]]]
[7,[[[6,6],[1,7]],8]]
[[1,[9,[6,2]]],[[4,0],[[7,7],[4,2]]]]
[[[5,[5,9]],[0,[7,2]]],[[3,3],6]]
[[5,[3,6]],[[0,[8,4]],[6,[5,5]]]]
[[[0,5],[[8,7],[0,3]]],[[[4,1],[6,2]],[[3,2],[2,7]]]]
[[[6,9],5],[[7,3],[[5,0],[2,2]]]]
[[3,5],[[1,[3,4]],[2,[5,3]]]]
[[9,9],[4,6]]
[[[[6,4],[3,7]],[3,8]],[3,[2,[3,7]]]]
[[4,[[1,1],6]],[7,[[1,1],6]]]
[[[[6,4],3],9],2]
[[[[8,1],3],7],[4,[9,1]]]
[4,[[[7,7],6],8]]
[[[7,5],[8,1]],[[6,[6,5]],[6,7]]]
[[8,[3,[1,3]]],[2,[[6,1],[0,5]]]]
[9,[[8,6],0]]
[[8,[1,5]],[[[6,4],6],1]]
[2,[[3,[4,6]],[[2,9],[6,4]]]]
[[[[0,9],[2,0]],[[2,4],7]],[[[7,1],3],[7,9]]]
[[[3,6],[[6,6],1]],[[[0,5],[6,8]],5]]
[[[4,5],[[5,1],0]],[3,[[3,1],[2,8]]]]
[[[[9,0],[7,6]],5],[6,[[0,3],1]]]
[[[1,4],[5,7]],[[9,[3,8]],3]]
[[[7,7],1],[[[5,0],[4,0]],8]]
[[[[0,9],[0,6]],[[5,8],[7,4]]],2]
[[[[0,2],1],[[4,8],0]],[4,[[8,7],[9,1]]]]
[[[1,[2,0]],[[8,4],[0,0]]],5]
[[[9,[8,1]],[[1,1],[4,2]]],[9,[7,[6,9]]]]
[[[[0,2],[1,5]],[[9,2],[8,7]]],[[6,8],[6,0]]]
[[[3,[6,7]],[[9,8],[6,9]]],[8,[[4,6],5]]]
[[[9,[1,5]],[[4,8],9]],2]
[[[0,[1,5]],0],0]
[[[[4,1],4],[4,[7,4]]],[[[3,9],9],3]]
[[[9,7],[[8,7],[0,0]]],[[[0,0],3],3]]
[[9,[[2,0],6]],[[8,6],[5,4]]]
[2,[6,1]]
[[7,[1,[9,5]]],[[[7,8],[1,0]],[6,3]]]
[[[[2,3],1],[7,3]],[[[1,5],[2,2]],[[6,3],7]]]
[4,6]
[[[[4,0],1],2],[[[0,5],8],[8,[0,4]]]]
[[5,[7,0]],[[[4,5],[0,2]],5]]
[[[5,[3,1]],[[8,4],[4,9]]],[2,[[4,8],9]]]
[[[0,7],2],[[[2,5],8],[0,[5,3]]]]
[[[[2,2],[8,1]],[8,[1,3]]],[6,7]]
[[[9,2],[[4,8],[7,1]]],[[[5,2],7],[5,8]]]
[[[2,8],[[3,6],[8,3]]],[[0,5],6]]
[[[3,[7,6]],[4,[5,2]]],6]
[[7,[[5,2],8]],[1,[8,[8,3]]]]
[[[[8,9],7],[[1,1],0]],[[3,6],[[7,8],9]]]
[[4,[[4,2],[7,9]]],[[8,9],[8,8]]]
[[[5,5],[9,[0,7]]],[[[5,8],8],4]]
[[8,[[4,4],[0,0]]],[[2,1],[[2,5],3]]]
[[6,[[4,3],[1,6]]],0]
[[[4,[1,6]],2],[[0,7],1]]
[[[6,[9,9]],[4,8]],[[[1,1],9],[4,[1,7]]]]
[[[[2,1],6],[[3,8],[2,2]]],[9,[7,6]]]
[[0,[[1,0],9]],[8,[0,6]]]
[[[8,[3,4]],[[6,7],[9,9]]],[[7,[6,8]],[[7,7],[6,8]]]]
[4,[[[4,5],[4,4]],[5,[9,0]]]]
[[[[8,2],7],[6,5]],2]
[[9,7],[4,[[5,3],7]]]
[[[[6,5],0],1],[[[5,8],[3,9]],[[9,4],[8,3]]]]
"""

main()

