from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow

#import numpy as np
#import sympy
#from sympy import *
from colorama import Fore, Style
from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
import pyperclip
from icecream import ic

from timer_utils import timefunction
from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
#from fz import _1
from quicklambda import _1, _2
#from mini_lambda import s, _, x



@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    if is_real:
        width = 25
        height = 6
    else:
        width = 3
        height = 2


    def data_parse(inp, width, height):
        lines = inp.strip().split('\n')
        parsed = list(batched(inp.strip(), width * height))
        return parsed


    def process1(parsed):
        layer_counters = list(enumerate(Counter(layer) for layer in parsed))
        ics(layer_counters)
        s = seq(layer_counters)
        fewest_zero_layer_index = s.min_by(lambda layer: layer[1]["0"])[0]
        ic(fewest_zero_layer_index)
        fewest_zero_layer = layer_counters[fewest_zero_layer_index][1]
        return fewest_zero_layer["1"] * fewest_zero_layer["2"]

    @timefunction
    def part1(inp):
        parsed = data_parse(inp, width, height)
        ics(parsed)
        result = process1(parsed)
        print_result(result)

    process2 = process1

    def process2(parsed):
        pixels = dict()
        ics(parsed)

        for layer in reversed(parsed):
            pixels.update((n, p) for n, p in enumerate(layer) if p != "2")

#        chars = ["."] * len(parsed)
#
#        for n, p in pixels.items():
#            chars[n] = p
#
#        array = rebuild_2D_string_array(chars, width)
#        print(get_vis_map_multiline_str(array))

        xs_and_ys = [(n % width, n // width) for n, p in pixels.items() if p == "1"]
        print(get_vis_map_multiline_str(*zip(*xs_and_ys)))

        ics(pixels)

        if not is_sample:
            xs, ys = zip(*xs_and_ys)
            s = get_vis_map_multiline_str(xs, ys, show_axis=False)
            return ocr_aoc_letters(s)


    @timefunction
    def part2(inp):
        nonlocal width

        if not is_real:
            width = 2

        parsed = data_parse(inp, width, height)
        result = process2(parsed)
        print_result(result)

    part1(inp1)
    part2(inp2)

def main():
    if 1:
        if samp_inps:
            for n, samp_inp in enumerate(samp_inps, 1):
                print_preface(False, n)
                run(samp_inp, samp_inp, False)
        elif samp_inp1.strip():
            print_preface(False)
            run(samp_inp1, samp_inp2, False)

    if 1:
        print_preface(True)
            # needs env var AOC_SESSION
        real_inp = get_aocd_data()
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)




samp_inp1 = r"""
123456789012
"""

samp_inp2 = "0222112222120000"

samp_inps = """
""".strip().split("\n")

samp_inps = [
    ]

main()

