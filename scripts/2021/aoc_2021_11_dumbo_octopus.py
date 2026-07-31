from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from dataclasses import dataclass, field
from builtins import pow
import pyperclip
from icecream import ic
import iteration_utilities as it_ut

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

PointVal = namedtuple("PointVal", "val,x,y")

@dataclass
class Point: # actually used
    x: int
    y: int
    val: int
    neighbors: list = field(default_factory=list)
    flashed: bool = False

    def increase(self):
#        print(f"({self.x},{self.y}) increase")

        if not self.flashed:
            self.val +=1

            if self.val == 10:
                self.val = 0
                self.flashed = True
#                print(f"({x},{y}) flashed")

                for p in self.neighbors:
                    p.increase()


def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')
    h_map = [list(map(int, line)) for line in inp]
    width = len(h_map[0])
    height = len(h_map)
    points = [[None] * width for _ in h_map]

    for x, y in product(range(width), range(height)):
        p = Point(x, y, h_map[y][x])
        points[y][x] = p

    all_points = list(it_ut.flatten(points))
    point_count = len(all_points)
    ics(point_count)
#    ics(points)
#    ics(all_points)

    def reset_point_values():
        for x, y in product(range(width), range(height)):
            get_point(x, y).val = h_map[y][x]

    def get_point(x, y):
        return points[y][x]

    def add_neighbor(p, x, y):
        if x < 0 or y < 0 or x >= width or y >= height:
            return

        p.neighbors.append(get_point(x, y))

    def add_neighbors(p):
        add_neighbor(p, x-1, y-1)
        add_neighbor(p, x-1, y)
        add_neighbor(p, x-1, y+1)

        add_neighbor(p, x+1, y-1)
        add_neighbor(p, x+1, y)
        add_neighbor(p, x+1, y+1)

        add_neighbor(p, x, y-1)
        add_neighbor(p, x, y+1)


    for x, y in product(range(width), range(height)):
        add_neighbors(get_point(x, y))

    def process_step():
        for p in all_points:
            p.flashed = False

        for p in all_points:
            p.increase()

    def count_flashed():
        return sum(1 for p in all_points if p.flashed)

    def simple_points():
#        return [[(p.x, p.y, p.val) for p in line_points] for line_points in points]
#        return [[p.val for p in line_points] for line_points in points]
        return ["".join(str(p.val) for p in line_points) for line_points in points]

    def part1():
        result = 0

        for step in range(100):
            process_step()
            flash_count = count_flashed()

#            if step < 5:
#                print(f"step {step}: flash_count={flash_count}")

            result += flash_count

        print_result(result)

    def part2():
        for step in count(1):
            process_step()
            flash_count = count_flashed()

#            if step <= 10 or step % 10 == 0:
#                ics(step, flash_count, simple_points())

            if point_count == flash_count:
                result = step
#                ics(step, simple_points())
                print_result(result)
                break

    part1()
    reset_point_values()
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
