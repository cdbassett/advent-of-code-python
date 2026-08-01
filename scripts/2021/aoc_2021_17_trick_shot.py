from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import pyperclip
from icecream import ic
from utils.timer_utils import timefunction
import matplotlib.pyplot as plt
from construct import *

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


"""
    quadratic sequence
    u(n)=an^2+bn+c
    first difference: how much each term increases over last one
    second difference: how much each first difference increases over last one
    a = second difference divided by 2
    b = u(2) - u(1) - 3a
    c = u(1) + 2a − (3a+b)
"""

"""
    y:
    y(1) = ivy
    y(2) = ivy + ivy - 1
    y(3) = ivy + ivy - 1 + ivy - 2
    2nd diff is -1

    a = -1/2
    b = ivy - 1 + 3/2 = ivy + 1/2
    c = ivy - 1 - (-3/2 + ivy -1 + 3/2) = 0
    y(n) = -n^2/2 + (ivy + 1/2)*n

    max:
        max_n=-b/2a = -(ivy + 1/2)/-1 = ivy + 1/2
        max_y = -(ivy+1/2)^2/2+(ivy + 1/2)*(ivy + 1/2)
        max_y(9) = -(9+1/2)^2/2 + (9+1/2)*(9 + 1/2)
                 = -(19/2)^2/2 + (19/2)*(19/2)

    n:  y: (ivy=2), y(n) = -n^2/2 + 5n/2
    0   0
    1   2
    2   3
    3   3
    4   2

    n:  x: (ivy=7), x(n) = -n^2/2 + 15n/2
    0   0
    1   7
    2   13
    3   18

    x(n) = -n^2/2 + (ivx - 1/2)*n for n < ivx, x(ivx) otherwise



position at step n:
	vx = max(0, ivx - n)
	x = vx(n) * n
	    = n*ivx - n^2 for n in (0, ivx), otherwise ivx^2
	vy(n) = ivy - n
	y = vy(n-1) * n = (ivy - (n - 1)) * n = n*(ivy+1) - n^2
	y = vy(n) + vy(n-1) ....
	n:  vy: y: (ivy=2)
	0   2   0
	1   1   ivy
	2   0   ivy + (ivy - 1) = 2ivy - 1
	3   -1  ivy + (ivy - 1) + (ivy - 2) = 3ivy - 3
	4   -2  ivy + (ivy - 1) + (ivy - 2) + (ivy - 3) = 4ivy - 6
	5   -3  ivy + (ivy - 1) + (ivy - 2) + (ivy - 3) + (ivy - 4) = 5ivy - 10 = n*ivy - n^2/2
	y = vy * n = (ivy - n) * n = n*ivy - (n-1)^2
"""

def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')
    line = inp[0]
    ics(line)
    parts = line.replace(",", " ").split()
    ics(parts)

    x_min, x_max = map(int, parts[2].split("=")[1].split(".."))
    y_min, y_max = map(int, parts[3].split("=")[1].split(".."))
#    x_point = Point(*map(int, parts[2].split("=")[1].split("..")))
#    y_point = Point(*map(int, parts[3].split("=")[1].split("..")))
    ics(x_min, x_max)
    ics(y_min, y_max)

    # -n**2/2 + (iv + 1/2)*n = m_min
#    ic(bits_used)
#    ics(packets)

    def calc_y(n, ivy):
        return -n**2/2 + (ivy + 1/2)*n

    def calc_x(n, ivx):
        if n > ivx:
            n = ivx

        return -n**2/2 + (ivx + 1/2)*n

    def in_y(y):
        return y >= y_min and y <= y_max

    def in_x(x):
        return x >= x_min and x <= x_max


    def get_max_y():
        a = -1/2
        c = 0

        for ivy in count(1):
            b = ivy + 1/2
            root = int(-b/a)
            hit_step = root + 1
            hit_y = calc_y(hit_step, ivy)
            ics(ivy, root, hit_step, hit_y)

            if hit_y < y_min:
                ivy -= 1
                vertex = -(ivy+1/2)**2/2+(ivy + 1/2)*(ivy + 1/2)
                result = round(vertex)
                return ivy, round(vertex)


        # for part 1 x is irrelevant
        # y(n) = -n^2/2 + (ivy - 1/2)*n
        # if y(n) < y_bot, stop processing
        # highest y point should be for highest initial value where value after y reaches 0 again isn't smaller than y_min
    @timefunction
    def part1():
        max_ivy, max_y = get_max_y()
        result = max_y

#        result = sum_versions(packets)
        print_result(result)

    def part2():
        max_ivy, max_y = get_max_y()
        max_ivx = x_max # first step hits last column
        min_ivy = y_min # first step hits last row
        ics(max_ivy, max_ivx, min_ivy)

#        possible_xs = [pos := calc_x(ivx)]
        hits = []

        if 0:
            ivxs = []
            ivys = []

            for ivx in range(1, max_ivx+1):
                for n in count(1):
                    x_pos = calc_x(n, ivx)
                    ics(n, x_pos)

                    if x_pos > x_max:
                        break

                    if x_pos >= x_min:
                        ivxs.append(ivx)
                        break # only need to establish one hit for these initial values

            for ivy in range(min_ivy, max_ivy+1):
                for n in count(1):
                    y_pos = calc_y(n, ivy)
                    ics(n, y_pos)

                    if y_pos < y_min:
                        break

                    if y_pos <= y_max:
                        ivys.append(ivy)
                        break # only need to establish one hit for these initial values

            hits = product(ivxs, ivys)

#        for ivx, ivy in [(6,5)]:
        for ivx, ivy in product(range(1, max_ivx+1), range(min_ivy, max_ivy+1)):
#            for ivx, ivy in [(6,3)]:
            for n in count(1):
                x_pos = calc_x(n, ivx)
                y_pos = calc_y(n, ivy)
#                    ics(n, x_pos, y_pos)

                if y_pos < y_min or x_pos > x_max:
                    break

                if y_pos <= y_max and x_pos >= x_min:
                    hits.append((ivx, ivy))
                    break # only need to establish one hit for these initial values

        ics(sorted(hits))
        result = len(hits)
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
