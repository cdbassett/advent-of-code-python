from functools import *
from collections import *
#from sympy import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
from timer_utils import timefunction

from colorama import Fore, Style
from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
import pyperclip
from icecream import ic

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from quicklambda import _1, _2
from mini_lambda import s, _, x

icf = ic.format

@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().split('\n')
#        lines = inp.strip("\n").split('\n')
        player_parts = list(split_iterable(lines, ""))
        players_cards = tuple(map_tuple(int, player_part[1:]) for player_part in player_parts)
        return players_cards

    def calc_score(win_deque):
        multipliers = tuple(range(len(win_deque), 0, -1))
        score = sum(c * m for c, m in zip(win_deque, multipliers))
        return score

    def process1(player1_cards, player2_cards):
        deque1 = deque(player1_cards)
        deque2 = deque(player2_cards)
        deques = deque1, deque2

        while deque1 and deque2:
#            card1, card2 = deque1.popleft(), deque2.popleft()
            cards = deque1.popleft(), deque2.popleft()
            windex = it_ut.argmax(cards)
#            ics(deque1, deque2, windex)
            win_deque = deques[windex]

            if windex == 1:
                cards = tuple(reversed(cards))

            win_deque.extend(cards)
#            ics(deque1, deque2)

        win_deque = deque1 or deque2
        return calc_score(win_deque)

#    game_cache = dict()

    def build_key(player1_cards, player2_cards):
        return (tuple(player1_cards),tuple(player2_cards))
#        return (player1_cards,player2_cards)

    def play_recursive_old(player1_cards, player2_cards, level=0):
        ics(level, player1_cards, player2_cards)
        deque1 = deque(player1_cards)
        deque2 = deque(player2_cards)
        deques = deque1, deque2
        round = 1
        game_cache = dict()

        while deque1 and deque2:
            key = build_key(deque1, deque2)
            prev = game_cache.get(key)

            if prev is not None:
                windex, win_deque = prev
                ics("cached!")
                return 0, win_deque

            cards = deque1.popleft(), deque2.popleft()
            card1, card2 = cards

            if card1 <= len(deque1) and card2 <= len(deque2):
#                windex, _ = play_recursive_old(tuple(deque1), tuple(deque2), level+1)
                windex, _ = play_recursive_old(tuple(deque1)[:card1], tuple(deque2)[:card2], level+1)
            else:
                windex = it_ut.argmax(cards)

#            ics(deque1, deque2, windex)
            win_deque = deques[windex]

            if windex == 1:
                cards = tuple(reversed(cards))

            win_deque.extend(cards)
            ics(level, round, windex, cards, deque1, deque2)

##            ics(deque1, deque2, windex)
#            win_deque = deques[windex]
#
#            if card1 > card2:
#                win_deque.extend(cards)
#            else:
#                win_deque.extend(reversed(cards))
            round += 1
            res = windex, win_deque
            game_cache[key] = res

        win_deque = deque1 or deque2
        windex = int(win_deque is deque2)
        ics(windex, win_deque)
        return res


    def play_recursive(player1_cards, player2_cards, level=1):
        ics(level, player1_cards, player2_cards)
        deque1 = deque(player1_cards)
        deque2 = deque(player2_cards)
        deques = deque1, deque2
        round = 1
        game_cache = dict()

        while deque1 and deque2:
            key = build_key(deque1, deque2)

            if key in game_cache:
                ics("cached!")
                return 0

            cards = deque1.popleft(), deque2.popleft()
            card1, card2 = cards
            ics(level, round, card1, card2, deque1, deque2)

            if card1 <= len(deque1) and card2 <= len(deque2):
                windex = play_recursive(tuple(deque1)[:card1], tuple(deque2)[:card2], level+1)
            else:
                windex = it_ut.argmax(cards)

#            ics(deque1, deque2, windex)
            win_deque = deques[windex]

            if windex == 1:
                cards = tuple(reversed(cards))

            win_deque.extend(cards)
            ics(level, round, windex, deque1, deque2)
#            ics(level, round, windex, cards, deque1, deque2)
#            ics(deque1, deque2)
            round += 1
            game_cache[key] = windex

        ics(windex, win_deque)
        return windex

    def play_recursive_start(player1_cards, player2_cards):
        deque1 = deque(player1_cards)
        deque2 = deque(player2_cards)
        deques = deque1, deque2
        round = 1
        game_cache = dict()

        while deque1 and deque2:
            key = build_key(deque1, deque2)
            ics(key)

            if key in game_cache:
                ics("cached!")
                raise Exception("unexpected level 0 caching!")
                return 0

            cards = deque1.popleft(), deque2.popleft()
            card1, card2 = cards
            ics(round, card1, card2, deque1, deque2)

            if card1 <= len(deque1) and card2 <= len(deque2):
                windex = play_recursive(tuple(deque1)[:card1], tuple(deque2)[:card2])
#                windex = play_recursive(tuple(deque1), tuple(deque2))
            else:
                windex = it_ut.argmax(cards)

#            ics(deque1, deque2, windex)
            win_deque = deques[windex]

            if windex == 1:
                cards = tuple(reversed(cards))

            win_deque.extend(cards)
            ics(round, windex)
#            ics(deque1, deque2)
            round += 1
            game_cache[key] = windex

        win_deque = deque1 or deque2
        return win_deque


    def process2(player1_cards, player2_cards):
#        windex, win_deque = play_recursive_old(tuple(player1_cards), tuple(player2_cards))
        win_deque = play_recursive_start(tuple(player1_cards), tuple(player2_cards))
        return calc_score(win_deque)


    @timefunction
    def part1(inp):
        player1_cards, player2_cards = data_parse(inp)
        result = process1(player1_cards, player2_cards)
        print_result(result)

    @timefunction
    def part2(inp):
        player1_cards, player2_cards = data_parse(inp)
        result = process2(player1_cards, player2_cards)
        print_result(result)

    part1(inp1)
    part2(inp2)

def main():
    if 1:
        if samp_inps:
            for n, samp_inp in enumerate(samp_inps, 1):
                print(f"{Fore.BLUE}{Style.BRIGHT}Sample {n}:{Style.RESET_ALL}")
                run(samp_inp, samp_inp, False)
        else:
            print(f"{Fore.BLUE}{Style.BRIGHT}Sample:{Style.RESET_ALL}")
            run(samp_inp1, samp_inp2, False)

    if 1:
        print(f"{Fore.BLUE}{Style.BRIGHT}Actual:{Style.RESET_ALL}")
        real_inp = get_aocd_data()
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)




samp_inp1 = r"""
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
"""

samp_inp2 = samp_inp1


short_samp = """
"""


samp_inps = [
#    short_samp,
#    samp_inp,
    ]


main()

