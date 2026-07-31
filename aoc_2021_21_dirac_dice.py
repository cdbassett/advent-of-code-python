from functools import *
from collections import *
from sympy import *
from itertools import *
from math import *
from statistics import *
from dataclasses import dataclass
from builtins import pow
import pyperclip
from icecream import ic
from timer_utils import timefunction

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


@dataclass
class Player:
    name: str
    position: int # 1-based
    score: int = 0

    def play(self, die_iter):
#        n, die_value = next(die_iter)
        die_values = islice(die_iter, 3)
        rolls, values = zip(*die_values)
        total = sum(values)
        self.position = ((self.position + total - 1) % 10) + 1 # temporarily shift to 0-based for modulo
        self.score += self.position

#        if rolls[2] / 3 < 5:
#            ic(rolls, values, self)

        return self.score




def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

#    inp = inp.strip().split('\n')
    inp = inp.strip("\n").split('\n')

    p1_start = 4
    p2_start = 9 if is_real else 8
    p1 = Player("p1", p1_start)
    p2 = Player("p2", p2_start)



    def play_one_game(die_iter, win_score):
        def one_play(player):
            score = player.play(die_iter)
            return score >= win_score

        winner = None
        p1.position = p1_start
        p2.position = p2_start

        while not winner:
            if one_play(p1):
                winner = p1
            elif one_play(p2):
                winner = p2

        rolled, _ = next(die_iter)
        loser = p1 if winner == p2 else p2
        return winner, loser, rolled


    @timefunction
    def part1():
        die_iter = enumerate(cycle(range(1,101)))
        winner, loser, rolled = play_one_game(die_iter, 1000)
        ic(rolled)
        ic(p1)
        ic(p2)
        ic(loser.score)
        result = loser.score * rolled
        print_result(result)

        # need to return rolls based on index
        # 0 will be always rolling 1
        # 1 will be always rolling 1 except first roll, which will be 2
        # 3 will be always rolling 1 except second roll, which will be 1
        # bascially act like converting index into a base 3 number string
    def die_roller(index):
        nxt = index

        while True:
            nxt, rem = divmod(nxt)
            yield rem + 1

    range3 = range(1, 4)
    all_die_rolls = list(sum(r) for r in product(range3, range3, range3)) # sum of 3 rolls, every variation

    @cache
    def play(p1, s1, p2, s2):
        wins1, wins2 = 0, 0
        s = s1

        for d in all_die_rolls:
            p = ((p1 + d -1) % 10) + 1 # temporarily shift to 0-based for modulo
            s = s1 + p

            if s >= 21:
                wins1 += 1
            else:
                w2, w1 = play(p2, s2, p, s) # switch players
                wins1 += w1
                wins2 += w2



        return wins1, wins2






    @timefunction
    def part2():
        wins1, wins2 = play(p1_start, 0, p2_start, 0)
        result = max(wins1, wins2)
        print_result(result)

    part1()
    part2()

def main():
#    print(real_inp)

    if 1:
        for samp_inp in samp_inps:
            print("Sample:")
            run(samp_inp, False)

    print("Actual:")
    run(real_inp, True)




samp_inp = r"""
"""

short_samp = """
"""


samp_inps = [
#    short_samp,
    samp_inp,
    ]



real_inp = r"""
"""

main()

