from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import pyperclip
from icecream import ic
import iteration_utilities as it_ut
import copy
import shapely
import shapely.ops
from timer_utils import timefunction
import matplotlib.pyplot as plt

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


def run(inp, is_real):
    insert_sample_functions(is_real, globals())
    print_preface(is_real)
    inp = inp.strip().split('\n')
    inp ="".join(inp) # handle lines too long for editor
    ic(len(inp))

    rocks = [
        [
            [1, 1, 1, 1]
        ],
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ],
        [
            [1, 1, 1],
            [0, 0, 1],
            [0, 0, 1],
        ],
        [
            [1],
            [1],
            [1],
            [1],
        ],
        [
            [1, 1],
            [1, 1],
        ],
    ]

    rocks = tuple(tuple(rock) for rock in rocks)
#    ics(rocks)


    """
        as set of points
        as set of tuples
        as 2d array
            up on screen is increasing y axis
    """

    def build_rows(rock, left_add):
        rock_width = width(rock)
        right_add = 7 - rock_width - left_add
        return [[0] * left_add + r + [0] * right_add for r in rock]


#    ics(build_rows(rocks[0], 2))
#    ics(build_rows(rocks[1], 2))
#    ics(build_rows(rocks[2], 2))

    def blank_row():
        return [0] * 7

    def collision(tunnel, rock, left_add, top_rock_row):
        rock_width = width(rock)
        rock_height = height(rock)

        for index, rock_line in zip(count(), rock):
            tunnel_row = tunnel[top_rock_row + index - rock_height]

            for tr_n, rn in zip(range(left_add, 7), range(rock_width)):
                if tunnel_row[tr_n] + rock_line[rn] > 1:
                    return True

    def apply_rock(tunnel, rock, left_add, top_rock_row):
        rock_width = width(rock)
        rock_height = height(rock)

        for index, rock_line in zip(count(), rock):
            tunnel_row = tunnel[top_rock_row + index - rock_height]

            for tr_n, rn in zip(range(left_add, 7), range(rock_width)):
                tunnel_row[tr_n] |= rock_line[rn]


        # remove empty rows from top
    def clear_tunnel_top(tunnel):
        remove_rows = 0
        tunnel_height = height(tunnel)

        for check_index in range(tunnel_height - 1, 0, -1):
#            ics(check_index, tunnel[check_index])

            if sum(tunnel[check_index]):
                break

            remove_rows += 1

#        ics(remove_rows)

        if remove_rows:
            tunnel[tunnel_height-remove_rows:tunnel_height] = []


        # remove any rows from tower that are lower than the row that finishes blocking off tunnel
        # vertical piece can drop as long as there's space, so once every column has been blocked once we can stop
    def clear_tunnel_bottom(tunnel):
        keep_rows = 0
        tunnel_height = height(tunnel)
        filled = [0] * 7

        for check_index in range(tunnel_height - 1, 0, -1):
            tunnel_row = tunnel[check_index]

            for n in range(7):
                filled[n] |= tunnel_row[n]

#            ics(check_index, tunnel[check_index])

            keep_rows += 1

            if sum(filled) == 7:
                break
        else:
            return # never found bottom

        tunnel[:-keep_rows] = []
#        ics(keep_rows, tunnel_rep(tunnel))



    rep_chars = ".#"

    def tunnel_rep(tunnel):
        return list(reversed(list("".join(rep_chars[l] for l in line) for line in tunnel)))

    def process_jet(jet, left_add, right_add):
        if jet == "<":
            if left_add:
                left_add -= 1
                right_add += 1
        else:
            if right_add:
                left_add += 1
                right_add -= 1

        return left_add, right_add

    def rep_applied_rock(tunnel, rock, left_add, top_rock_row):
        tunnel = copy.deepcopy(tunnel)
        apply_rock(tunnel, rock, left_add, top_rock_row)
        return tunnel_rep(tunnel)


    def part1():
        jets_iter = iter(cycle(inp))
        tunnel = [[1] * 7]    # problem doesn't call for rock bottom but we'll add for simpler dectection and remvoe later

        for n, rock in zip(range(2022), cycle(rocks)):
#        for n, rock in zip(range(10), cycle(rocks)):
            rock_height = height(rock)
            rock_width = width(rock)
            tunnel = tunnel + [blank_row() for _ in range(3 + rock_height)]

#            if n < 10:
#                ics("new", tunnel_rep(tunnel))

            left_add = 2
            right_add = 7 - rock_width - left_add
            top_rock_row = height(tunnel) - 1
#            ics(top_rock_row)

            jet = next(jets_iter)
#            ics(jet)
            left_add, right_add = process_jet(jet, left_add, right_add)

            for nj, jet in enumerate(jets_iter):
#                ics(nj, jet)

                    # gas push
                old_left, old_right = left_add, right_add
                left_add, right_add = process_jet(jet, left_add, right_add)

                if collision(tunnel, rock, left_add, top_rock_row):
                    left_add, right_add = old_left, old_right

                    # drop
                top_rock_row -= 1

#                ics(rep_applied_rock(tunnel, rock, left_add, top_rock_row))

                    # check
                if collision(tunnel, rock, left_add, top_rock_row):
                    top_rock_row += 1
#                    ics(tunnel_rep(tunnel))
                    apply_rock(tunnel, rock, left_add, top_rock_row)
#                    ics("apply", tunnel_rep(tunnel))
                    clear_tunnel_top(tunnel)
#                    ics("clear", tunnel_rep(tunnel))
                    break


        clear_tunnel_top(tunnel)
#        ics("done", tunnel_rep(tunnel))
        result = height(tunnel) - 1 # accouint for rock line at bottom
        print_result(result)



        # only tracking top n rows works but is much too slow, on actual data, didn't finish 1000th in one hour
    def part2():
        jets_iter = iter(cycle(inp))
        tunnel = [[1] * 7]    # problem doesn't call for rock bottom but we'll add for simpler dectection and remove later
        rocks_count = -1
        prog_step = 1000000000000 // 1000

#        for n, rock in zip(range(2022), cycle(rocks)):
        for n, rock in zip(range(1000000000000), cycle(rocks)):
#        for n, rock in zip(range(10), cycle(rocks)):
            rock_height = height(rock)
            rock_width = width(rock)
            tunnel = tunnel + [blank_row() for _ in range(3 + rock_height)]

            if not (n % prog_step):
                print(n)

#            if n < 10:
#                ics("new", tunnel_rep(tunnel))

            left_add = 2
            right_add = 7 - rock_width - left_add
            top_rock_row = height(tunnel) - 1
#            ics(top_rock_row)

            jet = next(jets_iter)
#            ics(jet)
            left_add, right_add = process_jet(jet, left_add, right_add)

            for nj, jet in enumerate(jets_iter):
#                ics(nj, jet)

                    # gas push
                old_left, old_right = left_add, right_add
                left_add, right_add = process_jet(jet, left_add, right_add)

                if collision(tunnel, rock, left_add, top_rock_row):
                    left_add, right_add = old_left, old_right

                    # drop
                top_rock_row -= 1

#                ics(rep_applied_rock(tunnel, rock, left_add, top_rock_row))

                    # check
                if collision(tunnel, rock, left_add, top_rock_row):
                    top_rock_row += 1
#                    ics(tunnel_rep(tunnel))
                    apply_rock(tunnel, rock, left_add, top_rock_row)
#                    ics("apply", tunnel_rep(tunnel))
                    clear_tunnel_top(tunnel)

                    if len(tunnel) > 15:
                        remove_count = len(tunnel) - 10
                        rocks_count += remove_count
                        tunnel = tunnel[-10:]

#                    ics("clear", tunnel_rep(tunnel))
                    break


        clear_tunnel_top(tunnel)
#        ics("done", tunnel_rep(tunnel))
        result = height(tunnel) + rocks_count
        print_result(result)


        # returns tunnel stage after rock is processed
    def next_stage(rock, jets_iter, tunnel):
        rock_height = height(rock)
        rock_width = width(rock)
        rocks_count = 0
        tunnel.extend(blank_row() for _ in range(3 + rock_height))
        left_add = 2
        right_add = 7 - rock_width - left_add
        top_rock_row = height(tunnel) - 1
#            ics(top_rock_row)

        jet = next(jets_iter)
#            ics(jet)
        left_add, right_add = process_jet(jet, left_add, right_add)

        for nj, jet in enumerate(jets_iter):
#                ics(nj, jet)

                # gas push
            old_left, old_right = left_add, right_add
            left_add, right_add = process_jet(jet, left_add, right_add)

            if collision(tunnel, rock, left_add, top_rock_row):
                left_add, right_add = old_left, old_right

                # drop
            top_rock_row -= 1

#                ics(rep_applied_rock(tunnel, rock, left_add, top_rock_row))

                # check
            if collision(tunnel, rock, left_add, top_rock_row):
                top_rock_row += 1
#                ics("collision", tunnel_rep(tunnel))
                apply_rock(tunnel, rock, left_add, top_rock_row)
#                ics("apply", tunnel_rep(tunnel))
                clear_tunnel_top(tunnel)
#                ics("clear_top", tunnel_rep(tunnel))
                prev_rocks = height(tunnel)
                clear_tunnel_bottom(tunnel)
#                ics("clear_bottom", tunnel_rep(tunnel))
                new_rocks = height(tunnel)
                rocks_count += (prev_rocks - new_rocks)
                break
        else:
            clear_tunnel_top(tunnel)

        return rocks_count


        # implementation of part 1 keeping only relevant bottom part
    def part1():
        jets_iter = iter(cycle(inp))
        tunnel = [[1] * 7]    # problem doesn't call for rock bottom but we'll add for simpler dectection and remvoe later
        rocks_count = -1

        for n, rock in zip(range(2022), cycle(rocks)):
            rocks_count += next_stage(rock, jets_iter, tunnel)
#            ics(n, tunnel_rep(tunnel))

        ics("done", n, tunnel_rep(tunnel))
        result = height(tunnel) + rocks_count
        print_result(result)

    def get_compact_tunnel_rep(tunnel):
        return tuple(it_ut.flatten(tunnel))

    def part2():
        jets_iter = iter(cycle(inp))
        rocks_iter = iter(cycle(rocks))
        tunnel = [[1] * 7]    # problem doesn't call for rock bottom but we'll add for simpler dectection and remvoe later
        rocks_count = -1 # -1 accounts for added line of rocks at the bottom
        all_rocks_count = 1000000000000 if is_real else 2022
        jets_count = len(inp)
        prog_step = all_rocks_count // 1000
        cycle_size = jets_count * len(rocks)
        ic(cycle_size)
        track_tunnel_states = [None] * cycle_size

        for n_rock, rock in zip(range(cycle_size), rocks_iter):
            added = next_stage(rock, jets_iter, tunnel)
            rocks_count += added

            if added:
#                ics(n_rock) # first rock where able to remove chunk
                break
#            ics(n, tunnel_rep(tunnel))

        n_cycle_begin = n_rock
        ics(n_cycle_begin)

        for n_rock, rock in zip(range(n_cycle_begin, n_cycle_begin + cycle_size), rocks_iter):
            added = next_stage(rock, jets_iter, tunnel)
            rocks_count += added
            track_tunnel_states[n_rock - n_cycle_begin] = get_compact_tunnel_rep(tunnel)

        next_cycle_begin = n_cycle_begin + cycle_size
        ics(next_cycle_begin)

        for n_rock, rock in zip(range(next_cycle_begin, next_cycle_begin + cycle_size), rocks_iter):
            added = next_stage(rock, jets_iter, tunnel)
            rocks_count += added

            if track_tunnel_states[n_rock - next_cycle_begin] == get_compact_tunnel_rep(tunnel):
                repeating_rock = n_rock
                ics(repeating_rock)
                break


        ics("done", n_rock, tunnel_rep(tunnel))
        result = height(tunnel) + rocks_count
        print_result(result)

        # maybe only need state at begining of new cycle
    def part2_no():
        jets_iter = iter(cycle(inp))
        rocks_iter = iter(cycle(rocks))
        tunnel = [[1] * 7]    # problem doesn't call for rock bottom but we'll add for simpler dectection and remvoe later
        rocks_count = -1 # -1 accounts for added line of rocks at the bottom
        all_rocks_count = 1000000000000 if is_real else 2022
        jets_count = len(inp)
        prog_step = all_rocks_count // 1000
        cycle_size = jets_count * len(rocks)
        ic(cycle_size)
        track_tunnel_states = [None] * cycle_size

        for n_rock, rock in zip(range(cycle_size), rocks_iter):
            added = next_stage(rock, jets_iter, tunnel)
            rocks_count += added

        start_cycle_state = get_compact_tunnel_rep(tunnel)
        repeating_rock = 0

#        for n_rock, rock in zip(range(cycle_size, all_rocks_count), rocks_iter):
        for n_rock, rock in zip(range(cycle_size, cycle_size * 100), rocks_iter):
            if not (n_rock % cycle_size):
                ic(n_rock)

                if n_rock > cycle_size and get_compact_tunnel_rep(tunnel) == start_cycle_state:
                    repeating_rock = n_rock
                    ic(repeating_rock)
                    break

            added = next_stage(rock, jets_iter, tunnel)
            rocks_count += added

        ics("done", n_rock, tunnel_rep(tunnel))
        result = height(tunnel) + rocks_count
        print_result(result)

        # returns tunnel stage after rock is processed
    def next_stage2(rock, jets_iter, tunnel):
        rock_height = height(rock)
        rock_width = width(rock)
        rocks_count = 0
        tunnel.extend(blank_row() for _ in range(3 + rock_height))
        left_add = 2
        right_add = 7 - rock_width - left_add
        top_rock_row = height(tunnel) - 1
#            ics(top_rock_row)

        jet_index, jet  = next(jets_iter)
#            ics(jet)
        left_add, right_add = process_jet(jet, left_add, right_add)

        for nj, (jet_index, jet) in enumerate(jets_iter):
#                ics(nj, jet)

                # gas push
            old_left, old_right = left_add, right_add
            left_add, right_add = process_jet(jet, left_add, right_add)

            if collision(tunnel, rock, left_add, top_rock_row):
                left_add, right_add = old_left, old_right

                # drop
            top_rock_row -= 1

#                ics(rep_applied_rock(tunnel, rock, left_add, top_rock_row))

                # check
            if collision(tunnel, rock, left_add, top_rock_row):
                top_rock_row += 1
#                ics("collision", tunnel_rep(tunnel))
                apply_rock(tunnel, rock, left_add, top_rock_row)
#                ics("apply", tunnel_rep(tunnel))
                clear_tunnel_top(tunnel)
#                ics("clear_top", tunnel_rep(tunnel))
                prev_rocks = height(tunnel)
                clear_tunnel_bottom(tunnel)
#                ics("clear_bottom", tunnel_rep(tunnel))
                new_rocks = height(tunnel)
                rocks_count += (prev_rocks - new_rocks)
                break
        else:
            clear_tunnel_top(tunnel)

        return jet_index, rocks_count

    def part2():
        jets_iter = iter(cycle(enumerate(inp)))
        rocks_iter = iter(cycle(enumerate(rocks)))
        tunnel = [[1] * 7]    # problem doesn't call for rock bottom but we'll add for simpler dectection and remvoe later
        rocks_count = -1 # -1 accounts for added line of rocks at the bottom
        all_rocks_count = 1000000000000 if is_real else 2022
        jets_count = len(inp)
        prog_step = all_rocks_count // 1000
        cycle_size = jets_count * len(rocks)
        ic(cycle_size)

        for n_rock, (rock_index, rock) in zip(range(cycle_size), rocks_iter):
            jet_index, added = next_stage2(rock, jets_iter, tunnel)
            rocks_count += added

            if added:
#                ics(n_rock) # first rock where able to remove chunk
                break
#            ics(n, tunnel_rep(tunnel))

        n_cycle_begin = n_rock
        ic(n_cycle_begin)

        tracked = dict()

        for n_rock, (rock_index, rock) in zip(range(n_cycle_begin, all_rocks_count), rocks_iter):
            key = (jet_index, rock_index)
            found = tracked.get(key)

            if found:
                prev_rock_num, elevation = tracked[key]
                period = n_rock - prev_rock_num

                if n_rock % period == all_rocks_count % period:
                    ic(period)
                    ic(prev_rock_num, n_rock)
                    cycle_height = rocks_count + height(tunnel) - elevation
                    ic(cycle_height)
                    rocks_remaining = all_rocks_count - n_rock
                    cycles_remaining = (rocks_remaining // period) + 1
                    ics(cycles_remaining)
                    result = elevation + (cycle_height * cycles_remaining) - 1
                    break
            else:
                tracked[key] = (n_rock, rocks_count + height(tunnel))

            jet_index, added = next_stage2(rock, jets_iter, tunnel)
            rocks_count += added


#        ics("done", n_rock, tunnel_rep(tunnel))
#        result = height(tunnel) + rocks_count
        print_result(result)

    part1()
    part2()

def main():
    for samp_inp in samp_inps:
        run(samp_inp, False)

    real_inp = get_aocd_data()
    run(real_inp, True)


samp_inp = r"""
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
"""


samp_inps = [
    samp_inp
    ]

main()

