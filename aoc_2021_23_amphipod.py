from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
from timer_utils import timefunction

import pyperclip
from icecream import ic

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


@timefunction
def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip("\n").split('\n')

    # parsing
    """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
#############
#01.2.3.4.56#
###A#B#B#D###
  #1#1#C#A#
  #########
    """
    def is_slot(idx):
        return idx >= 7

    amphi_letters = "ABCD"

    amphi_energy = {
        "A": 1,
        "B": 10,
        "C": 100,
        "D": 1000,
        }

    empty_amphipod = "."

    def letters_from_positions(current_state, positions):
        return "".join(current_state[p] for p in positions)

    def slot_remainder_is_correct(slot_size, slot_positions, slot_pos_to_amphi, current_state, pos, disp=False):
        amphi = slot_pos_to_amphi[pos]
        cur_slot_positions = slot_positions[amphi]
            # everything below our stop must be correct amphi (not even empty)
        rem_slot_positions_count = cur_slot_positions[-1] - pos

        if not rem_slot_positions_count:
            return True

        rem_slot_positions = cur_slot_positions[slot_size-rem_slot_positions_count:]
        current_slot_values = current_state[rem_slot_positions[0]:rem_slot_positions[-1]+1]
        result = current_slot_values == amphi * len(rem_slot_positions)

#            if amphi == "A" and rem_slot_positions:
        if disp and rem_slot_positions:
            slot_letters = letters_from_positions(current_state, cur_slot_positions)
            ics(result, amphi, pos, slot_letters)
            rem_letters = letters_from_positions(current_state, rem_slot_positions)
            ics("    ", cur_slot_positions, rem_slot_positions, rem_letters)

        return result


    def build_structures(slot_size=2):
        final_state = empty_amphipod * 7 + "".join(amphi * slot_size for amphi in amphi_letters)
        a_slots, b_slots, c_slots, d_slots = all_slots = tuple(chunks_of_n(range(7, 7 + slot_size * 4), slot_size))
#        ics(a_slots, d_slots)


        base_moves_list = [
            (0, 1) + a_slots,
            (6, 5, 4, 3, 2) + a_slots,
            (0, 1, 2) + b_slots,
            (6, 5, 4, 3) + b_slots,
            (0, 1, 2, 3) + c_slots,
            (6, 5, 4) + c_slots,
            (0, 1, 2, 3, 4) + d_slots,
            (6, 5) + d_slots,
            ]


            # (start, end) - > list of positions
        move_steps = {}

        for base_moves in base_moves_list:
            for n, pos in enumerate(base_moves[:-slot_size]):
                for n_slot in range(slot_size):
                    slot1 = base_moves[-1 - n_slot]
                    move_steps[(pos, slot1)] = base_moves[n+1:(-n_slot if n_slot else None)]
                    move_steps[(slot1, pos)] = tuple(reversed(base_moves[n:-1-n_slot]))

            # (start, end) - > number of spots moved into
        move_count = {}
        add_positions = {1, 2, 3, 4, 5}

        for key, val in move_steps.items():
            move_count[key] = len(val) + sum(1 for pos in val+key[0:1] if pos in add_positions)

        slot_positions = {
            "A": a_slots, # sequential, lowest to highest
            "B": b_slots,
            "C": c_slots,
            "D": d_slots,
            }
#        ic(slot_positions)

        # a pos in a slot -> the amphi letter that belongs there
        slot_pos_to_amphi = [empty_amphipod] * len(final_state)

        for amphi, one_slot_moves in slot_positions.items():
            for slot_pos in one_slot_moves:
                slot_pos_to_amphi[slot_pos] = amphi

        # position in the state -> the amphi latter that belongs there
        slot_pos_to_amphi = "".join(slot_pos_to_amphi)

        def can_move(current_state, start, end):
            ind_steps = move_steps[start, end]
            return all(current_state[p] == empty_amphipod for p in ind_steps) # true if every step in current_state but first step is empty

        slot_remainder_is_correct_func = partial(slot_remainder_is_correct, slot_size, slot_positions, slot_pos_to_amphi)

        right_sides = {2, 3, 4, 5}
        left_sides = {1, 2, 3, 4}

            # we know we're moving from a slot
        def can_move_from_slot(current_state, start, end):
                # logic is flawed, just 'cause slot is blocked doesn't mean there's no further solution, depnds on whether one of the blocking amphis can move after
            def slot_is_blocked(left_side):
                    # remainder of slot better be correct
                slot_index = left_side - 1
                affected_slot_positions = all_slots[slot_index]
                check_slot_amphi = amphi_letters[slot_index]
                skip_letters = { empty_amphipod, check_slot_amphi}
                    # may or may not be slot we're moving from
                slot_values = list(current_state[p] for p in affected_slot_positions if p != start and current_state[p] not in skip_letters)
#                slot_values = set(current_state[p] for p in affected_slot_positions if p != start) - skip_letters
#                assert empty_amphipod not in slot_values
#                assert check_slot_amphi not in slot_values

#                fail_condition = len(slot_values) == 3 and slot_index == 0
                fail_condition = slot_values

                if fail_condition:
                    assert end == 2
                    assert left_side == 1
                    assert current_state[end] == empty_amphipod
                    assert current_state[left_side] != empty_amphipod
                    assert "A" not in slot_values
                    ic(start, end, left_side, slot_index)
                    ic(check_slot_amphi, affected_slot_positions, slot_values, get_repr(current_state, (start,end)))

                return fail_condition

            amphi = current_state[start]
            cur_slot_positions = slot_positions[amphi]

                # don't allow moving an amphi out of a slot when it's already in correct position
            if start in cur_slot_positions:
                if start == cur_slot_positions[-1] or slot_remainder_is_correct_func(current_state, start):
                    return False

            if not can_move(current_state, start, end):
                return False

            return True


            # we know we're moving into a slot
        def can_move_to_slot(current_state, start, end):
            if not slot_remainder_is_correct_func(current_state, end):
                return False

            return can_move(current_state, start, end)

            # (letter, start pos) -> list of allowed final positions
        possible_moves = defaultdict(list)

# TODO: break up into hall-to-slot, slot-to-slot, and slot-hall moves
# pass just the 3 functions, not include in moves
# if any slot-to-slot is possible, do all that immediately and skip other iterations

        for amphi in amphi_letters:
            use_slot = slot_positions[amphi]

            for (start, end), move in move_steps.items():
                key = (amphi, start)

#                if start in use_slot:
                if is_slot(start):
                    possible_moves[key].append((can_move_from_slot, end))
                elif end in use_slot:
                    possible_moves[key].append((can_move_to_slot, end))
#                else:
#                    ic(amphi, start, end)
#                    raise Exception("Logic error, shouldn't get here!")

        possible_moves = dict((key, tuple(val)) for key, val in possible_moves.items())
#        ics(list((key, list(t[1] for t in val)) for key, val in possible_moves.items()))
        return move_steps, possible_moves, final_state, move_count, slot_positions, slot_pos_to_amphi





    # build index (numeric index for each possible location) 15 possible positions
    # determine possible moves (in general and for each turn)
    # have array for each position
    # have entry for each starting position, has possible final positions, costs, elements it passes through?
    #   need to only go to one position for each move, determined by if already filled
    #   maybe start with more dirett visualization, then build abstract tree with movements from that
    #   could have set of functions used to determine if move is possible, default is if in-between locations are empty but could also check for correct ending slot
    # each amphipod can only move twice, once out, once in
    # can't move in unless empty or other occupant correct and correct slot
    # can't move through each other
    # recursively try one move at a time
    # track current positions and score
    # cacluate energy for each move
    # pass as pairs of amphipod, position, or as array of positions with amphipods in it


    def get_repr(current_state, emphasizes=[]):
        top = list(current_state)

        for emphasize in emphasizes:
            top[emphasize] = top[emphasize].lower().replace(".", "x")

        rest = top[7:]
        top = top[:7]

        top.insert(2, empty_amphipod)
        top.insert(4, empty_amphipod)
        top.insert(6, empty_amphipod)
        top.insert(8, empty_amphipod)
        top = "#" + "".join(top) + "#"
        next_parts = list(zip(*n_chunks(rest, 4)))
#        ic(list(zip(*n_chunks(current_state[7:], 4))))
#        ic(next_parts)
        bottom = "  #" + "#  \n  #".join("#".join(s) for s in next_parts) + "#  "
        return f"{top}\n{bottom}"

        # As long as the heuristic does not overestimate distances , A* finds an optimal path, like Dijkstra’s Algorithm does.
        # A* uses the heuristic to reorder the nodes so that it’s more likely that the goal node will be encountered sooner.
        # Breadth First Search and Dijkstra’s Algorithm are guaranteed to find the shortest path given the input graph.
        # Greedy Best First Search is not. A* is guaranteed to find the shortest path if the heuristic is never larger than the true distance.
        # As the heuristic becomes smaller, A* turns into Dijkstra’s Algorithm.
        # As the heuristic becomes larger, A* turns into Greedy Best First Search.


    hall_pos_to_real_pos = {
        0: 0,
        1: 1,
        2: 3,
        3: 5,
        4: 7,
        5: 9,
        6: 10,
        }

    # amphi letter -> 0-based slot index
    slot_indices_by_letter = dict((amphi, ord(amphi) - ord("A")) for amphi in "ABCD")
    # first_avail_dest in slot, -1 means none, only available if all below are correct letter
    # first_avail_src in slot, -1 means none, only available if slot not done yet (empty laso mean not available)


    # could track blocked positions, where nothing can move in yet bc amphis aren't out
    # could track final positions, where nothing needs to move in bc correct amphis are in
    # could track top positions for each room, 0 or 1 available for each slot
    # would need to be part of state, immutable, and updated after each move
    # could also track positions of movable amphis, those in hall + those at top of slots but not correct slots
    # could cal blockable positions as well as move_steps, to check if clear rather than all move_steps

    def bfs(slot_size, initial_state):
            # here we want to do a rough estimate of what the minimal cost it would be to transform from current state to final
            # take energy per letter into account
            # for first run, just put minimal cost to move from slot to slot and hall to slot
        def heuristic(current_state):
            hall_letters, slot_letters = current_state[:7], current_state[7:]
            cost = 0
            hall_costs = 0
            slot_costs = 0

                # not taking into account depth into slot yet
                # "01 2 3 4 56"
                # "01234567890"
            for n, amphi in enumerate(hall_letters):
                if amphi != empty_amphipod:
                    dest_slot_index = slot_indices_by_letter[amphi]
                    move_squares = abs(hall_pos_to_real_pos[n] - (dest_slot_index * 2 + 2)) + 1
                    move_cost = move_squares * amphi_energy[amphi]
#                    ic("hall", amphi, move_cost, move_squares, dest_slot_index)
                    hall_costs += move_cost

            for n, amphi in enumerate(slot_letters):
                if amphi != empty_amphipod:
                    cur_slot_index  = n // slot_size
                    dest_slot_index = slot_indices_by_letter[amphi]

                    if cur_slot_index != dest_slot_index:
                        move_squares = abs(dest_slot_index - cur_slot_index) * 2 + 2
                        move_cost = move_squares * amphi_energy[amphi]
#                        ic("slot", amphi, move_cost)
#                        ic(" ", move_squares, cur_slot_index, dest_slot_index)
                        slot_costs += move_cost

            cost = hall_costs + slot_costs
#            ic(cost, hall_costs, slot_costs, current_energy, get_repr(current_state))
            return cost


#        print("initial_state:")
#        print(get_repr(initial_state))

        # move_steps: (start, end) - > list of positions
        # possible_moves: (letter, start pos) -> list of allowed final positions
        # final_state: string of desired result
        # move_count: (start, end) - > number of spots moved into
        # slot_positions: amphi letter -> array of room/slot positions, loewst to highest
        # slot_pos_to_amphi: position in the state -> the amphi letter that belongs there
        move_steps, possible_moves, final_state, move_count, slot_positions, slot_pos_to_amphi = build_structures(slot_size)
        slot_remainder_is_correct_func = partial(slot_remainder_is_correct, slot_size, slot_positions, slot_pos_to_amphi)



#        print(get_repr(final_state))
        positions_range = tuple(range(7 + slot_size * 4))
        hall_positions = tuple(range(7))

        queue = []
        put, get = get_queue_functions_smallest(queue)
        put((0, 0, 0, initial_state, (-1,)*4, tuple(slot_pos[0] for k, slot_pos in slot_positions.items()))) # assumes dict is in order
        iterations = 0
        disp_at = 100000
        best_steps = 0
        seen = {}
        cant_move = set()

        while queue:
            iterations += 1
            _, steps, current_energy, current_state, first_avail_dest, first_avail_src = get() # when using heap, always get smallest value.

            if current_state == final_state:
                ic(iterations, steps)
                return next_energy

            if not iterations % disp_at:
#            if iterations == 1:
#            if iterations < 20:
                ic(iterations, len(queue), current_energy)
                print(get_repr(current_state))

            for pos in hall_positions + first_avail_src: # prune possible moves from room/slot to 1 or 0
                if pos < 0:
                    continue

                amphi = current_state[pos]

                if amphi != empty_amphipod:
                    pos_is_slot = is_slot(pos)
                    p_moves = possible_moves[(amphi, pos)]
                    amphi_slot_index = slot_indices_by_letter[amphi if not pos_is_slot else slot_pos_to_amphi[pos]]
                    cur_slot_positions = slot_positions[amphi]

                        # prune possible moves to room/slot to 1 or 0
                    if not pos_is_slot: # moving to slot
                        end_pos = first_avail_dest[amphi_slot_index]
                        p_moves = [] if end_pos < 0 else [(p_moves[0][0], end_pos)]

                    for can_move_func, end_pos in p_moves:
                        if can_move_func(current_state, pos, end_pos):
                            temp_state = list(current_state)
                            temp_state[pos] = empty_amphipod
                            temp_state[end_pos] = amphi
                            next_state = "".join(temp_state)
                            next_energy = current_energy + move_count[pos, end_pos] * amphi_energy[amphi] # take into account step where they won't stop
                            previous = seen.get(next_state)

                                # if we've already processed this state, and its energy was at least as good, don't do any more with it, it would be just a duplication
                            if previous and previous <= next_energy:
                                continue

                            seen[next_state] = next_energy
                            priority = next_energy + heuristic(next_state)

                            next_first_avail_dest, next_first_avail_src = list(first_avail_dest), list(first_avail_src)
                            next_dest = first_avail_dest[amphi_slot_index]
                            next_src = first_avail_src[amphi_slot_index]

                            if pos_is_slot: # moving to hall
                                if pos == cur_slot_positions[-1]: # last one out
                                    next_src = -1
                                    next_dest = cur_slot_positions[-1]
                                else:
#                                        if slot_remainder_is_correct_func(next_state, pos, amphi=="B" and amphi_slot_index == 2):
                                    if slot_remainder_is_correct_func(next_state, pos):
                                        next_src = -1
                                        next_dest = pos
                                    else:
                                        next_src += 1
                                        next_dest = pos

                            else: # must be moving to slot
                                assert is_slot(end_pos)

                                if next_src != -1:
                                    print(get_repr(current_state))
                                    print(get_repr(next_state))
                                    ic(iterations, amphi, pos, end_pos, first_avail_dest, first_avail_src, amphi_slot_index, next_src, cur_slot_positions)

                                assert next_src == -1 # if moving in can't still be expecting to move out

                                if end_pos == cur_slot_positions[0]: # last one in
                                    next_dest = -1
                                else:
                                    next_dest -= 1

                            next_first_avail_dest[amphi_slot_index] = next_dest
                            next_first_avail_src[amphi_slot_index] = next_src
                            put((priority, steps+1, next_energy, next_state, tuple(next_first_avail_dest), tuple(next_first_avail_src)))


    @timefunction
    def part1():
        amphis = "CCAABDDB" if is_real else "BACDBCDA"
        initial_state = empty_amphipod * 7 + amphis
        print("initial_state:")
        print(get_repr(initial_state))
        result = bfs(2, initial_state)
        print_result(result)

#      Part 1 result: 12521
#      Part 2 result: 44169


    @timefunction
    def part2():
  #D#C#B#A#
  #D#B#A#C#
        amphis = "CDDCACBABBADDACB" if is_real else "BDDACCBDBBACDACA"
        initial_state = empty_amphipod * 7 + amphis
        result = bfs(4, initial_state)
        print("initial_state:")
        print(get_repr(initial_state))
        print_result(result)

    #      Part 1 result: 11536
    #      Part 2 result: 55136

    part1()
    part2()

def main():
#    print(real_inp)

    if 0:
        for samp_inp in samp_inps:
            print("Sample:")
            run(samp_inp, False)

    if 1:
        print("Actual:")
        real_inp = get_aocd_data()
        run(real_inp, True)




samp_inp = r"""
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
  """

short_samp = """
"""


samp_inps = [
#    short_samp,
    samp_inp,
    ]


main()

