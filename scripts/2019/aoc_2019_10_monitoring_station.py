from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow

from colorama import Fore, Style
from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
import pyperclip
from icecream import ic

from utils.timer_utils import timefunction
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from utils.quicklambda import _1, _2



@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().split('\n')
        return lines

    def calc_polar(parsed):
        coords = list(get_hash_coords(parsed))
#        by_angle = defaultdict(list)
        all_coords = dict()


        for coord1 in coords:
            by_angle = all_coords[coord1] = defaultdict(list)

            for coord2 in coords:
                if coord1 != coord2:
                    coord_diff = subtract_tuple(coord2, coord1)
                    r, phi = xy_to_polar(*coord_diff)
#                    ics(coord1, coord2, r, phi)
                    by_angle[phi].append((r, coord2))

#        ic(len(all_coords))
        return all_coords

        # we want asteroid that can see the most
        # an asteroid can see another one if there is not another one in the same line of sight
        # so we can effectively check by slope
    def process1(parsed):
        all_coords = calc_polar(parsed)



#        ics(map_list(len, all_coords))
#        ics(all_coords[(8, 9)])
#        ics(len(all_coords[(8, 9)]))
#        ics(list(len(by_angle) for by_angle in all_coords))
#        ics(map_list(len, all_coords))
        return max(map(len, all_coords.values()))

#        slopes = [Counter(get_slope(coord1, coord2) for coord2 in coords if coord1 != coord2) for coord1 in coords]
#        return max(map(len, slopes))

    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)
        result = process1(parsed)
        print_result(result)

    process2 = process1

    def process2(parsed):
        all_coords = calc_polar(parsed)
        use_coords = seq(all_coords.items()).max_by(lambda by_angle: len(by_angle[1].items()))
#        ics(use_coords)
        base, by_angle = use_coords
        ic(base)
#        max_length = max(map(len, by_angle.values()))
#        process_asteroids_list = sorted(((-phi + pi/2) % (2 * pi), sorted(coord_list)) for phi, coord_list in by_angle.items())
        # unit circle has y increase in upwards direction, but in our map y increases in the downward direction
        process_asteroids_list = sorted(((phi + pi/2) % (2 * pi), sorted(coord_list)) for phi, coord_list in by_angle.items())
#        ics(list((angle, coord_list[0]) for  angle, coord_list in process_asteroids_list))

        if is_sample:
            for n, target in enumerate(roundrobin(*(coord_list for angle, coord_list in process_asteroids_list)), 1):
                if n in (1,2,3,10,20,50,100,199,200,201):
                    ics(n, target)

#        for n in range(199,202):
#            target = nth(roundrobin(*(coord_list for angle, coord_list in process_asteroids_list)), n)
#            ic(n, target)

        target = nth(roundrobin(*(coord_list for angle, coord_list in process_asteroids_list)), 199)
        ic(target)
        r, coord = target
        return coord[0] * 100 + coord[1]


    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
        result = process2(parsed)
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

