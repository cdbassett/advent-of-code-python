from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import copy
from utils.timer_utils import timefunction

from colorama import Fore, Style
from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
from icecream import ic


from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


# https://adventofcode.com/2020/day/24


icf = ic.format





@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        subs = [("nw", "n0"), ("ne", "n1"), ("sw", "s0"), ("se", "s1"), ("e", "e "), ("w", "w "),]

        for sub in subs:
            inp = inp.replace(*sub)

        for f, t in subs[:4]:
            inp = inp.replace(t, f)

        lines = inp.strip().split('\n')
#        lines = inp.strip("\n").split('\n')
#        tile_dirs = map_list(compose(partial_right(chunks_of_n, 2), sjoin, list), lines)
        tile_dirs = [map_list(compose(sjoin, str.strip), chunks_of_n(line, 2)) for line in lines]
#        ics(tile_dirs)
        return tile_dirs

    # using axial coordinates (q, r):
    #   w increases q, e decreases.
    #   nw decrease r, se increases.
    #   ne decreases s, sw increases s, s = -q-r.
    # https://www.redblobgames.com/grids/hexagons/

    dir_map = {
        "ne": (1, -1),
        "sw": (-1, 1),
        "w": (-1, 0),
        "e": (1, 0),
        "nw": (0, -1),
        "se": (0, 1),
        }

    all_dirs = dir_map.values()

    def count_black(tiles):
        return sum(1 for t in tiles.values() if t)

    def process1(tile_dirs):
        tiles = defaultdict(bool) # True is black

        for line_dirs in tile_dirs:
            pos = 0, 0

            for d in line_dirs:
                pos = add_tuple(pos, dir_map[d])

            tiles[pos] = not tiles[pos]


        return tiles


    def touch_neighbors(coord, tiles):
        tiles[coord]

        for d in all_dirs:
            tiles[add_tuple(coord, d)]


    def count_black_neighbors(coord, tiles):
        cnt = 0

        for d in all_dirs:
#            if tiles[add(coord, d)]:
            if tiles.get(add_tuple(coord, d), False):
                cnt += 1

        return cnt


#    def get_max_ranges(tiles):



    def process2(tiles, steps):
        for step in range(1, steps+1):
            new_tiles = copy.copy(tiles)
#            ics(len(tiles))

            for coord, black in tiles.items():
                if black:
                    touch_neighbors(coord, new_tiles)

            tiles = new_tiles
            new_tiles = copy.copy(tiles)

#            ics(len(tiles))

            for coord, black in tiles.items():
                cnt = count_black_neighbors(coord, tiles)

                if cnt == 2:
                    new_tiles[coord] = True
                elif cnt == 0 or cnt > 2:
                    new_tiles[coord] = False

            tiles = new_tiles
            ics(step, count_black(tiles))
#            break

        return count_black(tiles)


    @timefunction
    def part1(inp):
        tile_dirs = data_parse(inp)
        tiles = process1(tile_dirs)
        result = count_black(tiles)
        print_result(result)


    @timefunction
    def part2(inp):
        tile_dirs = data_parse(inp)
        tiles = process1(tile_dirs)
        result = process2(tiles, 100)
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

