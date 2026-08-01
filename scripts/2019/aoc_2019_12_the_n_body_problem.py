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
#        parsed = list(batched(string_to_integers(inp.strip()), 3))
        parsed = map_list(string_to_integers, lines)
        return parsed

    def adjust(a, b):
#        ics(a, b)
        return 0 if a == b else ((b - a) // abs(b - a))

#    assert(adjust(3, 5) == 4)
#    assert(adjust(5, 3) == 4)
#    assert(adjust(5, 5) == 5)

    def energy(moon):
        return sum(map(abs, moon))

    def process1(parsed):
        positions = parsed
        velocities = [[0] * 3 for _ in positions]
        steps = 10 if is_sample else 1000

        for step in range(steps):
            for n in range(4):
                cur_vel = velocities[n]
                cur_pos = positions[n]
                other_positions = del_index(positions, n)
#                ics(cur_vel, cur_pos, other_positions)

                for other_pos in other_positions:
#                    ics(n, cur_vel, cur_pos, other_pos)
                    cur_vel = add_tuple(cur_vel, starmap_tuple(adjust, zip(cur_pos, other_pos)))
#                    ics(n, cur_vel)

                velocities[n] = cur_vel

            positions = starmap_list(add_tuple, zip(positions, velocities))
#            ics(positions)
#            ics(velocities)
#            break

        energies = [energy(cur_pos) * energy(cur_vel) for cur_pos, cur_vel in zip(positions, velocities)]
        ics(energies)
        return sum(energies)

    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)
        result = process1(parsed)
        print_result(result)

    def get_cycles(all_positions):
        cycles = [None for dim in range(3)]
        ics(all_positions)

        for dim in range(3):
            ics(dim)
            positions = [one_position[dim] for one_position in all_positions]
            org_pos = tuple(positions)
            ics(positions)
            velocities = [0 for _ in positions]
            seen = dict()

            for step in count():
                new_velocities = velocities[:]

                for n in range(4):
                    cur_vel = velocities[n]
                    cur_pos = positions[n]
                    other_positions = del_index(positions, n)
#                ics(cur_vel, cur_pos, other_positions)

                    for other_pos in other_positions:
#                    ics(n, cur_vel, cur_pos, other_pos)
                        cur_vel = cur_vel + adjust(cur_pos, other_pos)
#                    ics(n, cur_vel)

                    new_velocities[n] = cur_vel

                velocities = new_velocities
                positions = add_tuple(positions, velocities)
                current = tuple(velocities), tuple(positions)
#                ics(current)

                last_step = seen.get(current)

                if last_step is not None:
                    cycles[dim] = step - last_step
                    ics(step, last_step, cycles[dim])
                    break

                seen[current] = step

                if not step % 100_000:
                    ics(dim, step)

        return cycles


    def process2(parsed):
        # determine cycles individually
        cycles = get_cycles(parsed)
        ics(cycles)
        return lcm(*cycles)


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

