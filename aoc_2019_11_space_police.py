from functools import *
from collections import *
#from sympy import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
#import numpy as np
from timer_utils import timefunction

from sympy import *

from colorama import Fore, Style
from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
import pyperclip
from icecream import ic

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

from aoc_2019_intcode import process_intcodes, parse_intcodes


@timefunction
def run(inp1, inp2, is_real):
    icsd = nothing if is_real else ic
    icsd = nothing
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        return parse_intcodes(inp)

    def process1(parsed, start_color = 0):
        painted = defaultdict(int) # point -> 0 or 1
        generator = process_intcodes(parsed, ics=ics)
        generator.send(None) # start it
        cur_pos = 0, 0
        direction = 0
        adjustments = list(vertical_movements.values())
#        ic(adjustments)
        painted[cur_pos] = start_color

        try:
            for step in count():
                color = generator.send(painted[cur_pos])
                painted[cur_pos] = color
                turn = next(generator)


                if turn == 1:
                    direction += 1
                else:
                    direction -= 1

                direction = direction % 4

#                if step < 10:
#                    ic(cur_pos, color, turn, direction, adjustments[direction], len(painted))
#                    print(get_vis_map_multiline_str(map_list(first_elem, painted), map_list(second_elem, painted), special_chars=[("@", cur_pos[0], cur_pos[1])]))
#                ic(cur_pos, adjustments[direction])
                cur_pos = add_tuple(cur_pos, adjustments[direction])

        except StopIteration:
            ic("stopped", step)
        except GeneratorExit:
            ic("exited", step)

        return painted

    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
#        ics(parsed)
        painted = process1(parsed)
        result = len(painted)
        print_result(result)

    process2 = process1

    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
#        ics(parsed)
        painted = process2(parsed, 1)
        white_points = [p for p, color in painted.items() if color == 1]
        xs, ys = xs_and_ys(white_points)
        print(get_vis_map_multiline_str(xs, ys))

        if not is_sample:
            s = get_vis_map_multiline_str(xs, ys, show_axis=False)
            print_result(ocr_aoc_letters(s))


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
        real_inp = get_aocd_data()
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)




samp_inp1 = r"""
"""

samp_inp2 = """
"""



samp_inps = """
""".strip().split("\n")
samp_inps=[]



main()


