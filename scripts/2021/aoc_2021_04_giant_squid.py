from functools import *
from collections import *
from itertools import *
from math import *
from builtins import pow
import pyperclip
from icecream import ic
import iteration_utilities as it_ut

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)
    print_list = partial(print_list_aoc, is_real)

    inp = inp.strip().split('\n')
    call_nums = list(map(int, inp[0].split(",")))
    print_list("call_nums", call_nums)
    boards = list(split_iterable(inp[2:], ""))
#    print_list("boards", boards)
    boards = [[tuple(map(int, board_line.strip().split())) for board_line in board] for board in boards]
    print_list("boards", boards)

    matches = list()

    def add_board_matches(n_board, board):
        for board_line in board:
            matches.append((n_board, set(board_line)))

    for n_board, board in enumerate(boards):
        add_board_matches(n_board, board)
        add_board_matches(n_board, zip(*board))

    print_list("matches", matches)

    def find_board_match(called_set, matches):
        for n_board, board_line_set in matches:
            if not (board_line_set - called_set):
                return n_board

    def find_winning_board(matches):
        called_set = set()
        winning_board = None

        for call_num in call_nums:
            called_set.add(call_num)

            while (n_board_match := find_board_match(called_set, matches)) is not None:
                winning_board = boards[n_board_match]
#                    print_list("winning_board", winning_board)
                yield call_num, called_set, n_board_match, winning_board
                    # take winning this boards matches out
                if not (matches := [(n_board, board_line_set) for n_board, board_line_set in matches if n_board != n_board_match]):
                    return

    def get_board_score(call_num, called_set, winning_board):
        uncalled = [n for n in flatten(winning_board) if n not in called_set]
        print_list("uncalled", uncalled)
        return call_num * sum(uncalled)

    def part1():
        call_num, called_set, n_board, winning_board = first(find_winning_board(matches))
        score = get_board_score(call_num, called_set, winning_board)

        print_result(score)

    def part2():
#        winning_boards = list(find_winning_board(matches))
#        call_num, called_set, n_board, winning_board = winning_boards[-1]
        call_num, called_set, n_board, winning_board = it_ut.last(find_winning_board(matches))
        score = get_board_score(call_num, called_set, winning_board)
        print_result(score)


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
