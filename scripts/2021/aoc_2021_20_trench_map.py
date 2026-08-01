from functools import *
from collections import *
from sympy import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import pyperclip
from icecream import ic
from utils.timer_utils import timefunction

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


def xs_and_ys(points):
    return zip(*points)


def or_and_shift(a, b):
    return a << 1 | b

def disp_image(title, image, max_val):
    if not max_val:
        print_lines(*[title] + image)

def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip("\n").split('\n')
#    ic(inp[:5])
#    ic(list(line[:60] for line in inp[:5]))
    ic(len(inp))
    enhancement, image = split_iterable(inp, "")
    enhancement = enhancement[0]
    ic(len(enhancement))

    full_width = width(image)
    ic(full_width)
    full_height = height(image)
    ic(full_height)

    max_val = 5 if is_real else None
    disp_image("image", image, max_val)


    def enhance_image(image, step):
        height = len(image)
        width = len(image[0])
        new_height = height + 2
        new_width = width + 2

        from_height = new_height + 2
        from_width = new_width + 2

        # if index of 0 is light pixel, make outer boundary light
        # really this means every other enhancement has all outer pixels light
        # for odd steps, everything outside border by 1 has become light
        filler = "#" if enhancement[0] == "#" and step % 2 else "."
        filler_lines= [filler * from_width] * 2
        filler_side = filler * 2
        from_image = filler_lines + [filler_side + l + filler_side for l in image] + filler_lines

        new_image = [["."] * new_width] + [["."] * new_width for l in image] + [["."] * new_width]
#        disp_image("from_image", from_image, max_val)
#        disp_image("new_image", new_image, max_val)

        for x, y in product(range(0, new_width), range(0, new_height)):
            index = 0

            for ly, lx in product(range(y-1, y+2), range(x-1, x+2)):
                index = (index << 1) | int(from_image[ly+1][lx+1] == "#")

#            if x == 0 and y < 5:
#                ics(x, y, index)

            if enhancement[index] == "#":
                new_image[y][x] = "#"

        new_image = ["".join(l) for l in new_image]
        return new_image





#    ics(left_arrows)

    @timefunction
    def part1():
        first_pass = enhance_image(image, 0)
        disp_image("first_pass", first_pass, max_val)
#        ic(get_xy_bounds(*xs_and_ys(first_pass)))

        second_pass = enhance_image(first_pass, 1)
        disp_image("second_pass", second_pass, max_val)
#        ic(get_xy_bounds(*xs_and_ys(second_pass)))

        result = sum(c=="#" for l in second_pass for c in l)
        print_result(result)


    @timefunction
    def part2():
        working_image = image

        for step in range(50):
            working_image = enhance_image(working_image, step)

#        disp_image("working_image", working_image, max_val)
        result = sum(c=="#" for l in working_image for c in l)
        print_result(result)

    part1()
    part2()

def main():
    if 0: # samples from aocd don't work yet, replaced from hardcoded to put on github
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
