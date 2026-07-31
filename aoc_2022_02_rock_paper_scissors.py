from functools import *
from collections import *
from itertools import *
from math import *
from builtins import pow
import pyperclip
from icecream import ic

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it


plays = "ABC"
responses = "XYZ"

scores = [
    ( 3, 6, 0 ), # rock
    ( 0, 3, 6 ), # paper
    ( 6, 0, 3 ), # scissors
    ]


matches = [ dict((s, n) for n, s in enumerate(row)) for row in scores ]

def play_score(p):
#    return plays.find(p) + 1
    return responses.find(p) + 1

# lose = 0, tie = 3, win = 6
def result_score(p, r):
    pi = plays.find(p)
    ri = responses.find(r)
    return scores[pi][ri]

def match_score(r):
    return responses.find(r) * 3


def main(inp, is_real):
    insert_sample_functions(is_real, globals())
    print_preface(is_real)
    inp = inp.strip().split('\n')
    strategy_guide = [line.split() for line in inp]
    print_list("strategy_guide", strategy_guide)
    print_list("matches", matches)

    def part1(inp, is_real):
        play_scores = [play_score(r) for p, r in strategy_guide]
        result_scores = [result_score(p, r) for p, r in strategy_guide]
        scores = [p + r for p, r in zip(play_scores, result_scores)]

        print_list("play_scores", play_scores)
        assert all(s >= 0 for s in play_scores)
        print_list("result_scores", result_scores)
        assert all(s >= 0 for s in result_scores)
        print_list("scores", scores)
        assert all(s >= 0 for s in scores)

        score = sum(scores)
        print_result(score)

    def part2(inp, is_real):
#        result_scores = [result_score(p, r) for p, r in strategy_guide]
        match_scores = [match_score(r) for p, r in strategy_guide]
        print_list("match_scores", match_scores)
        assert all(s >= 0 for s in match_scores)

        needed_plays = [matches[plays.find(p)][m] for (p, r), m in zip(strategy_guide, match_scores)]
        print_list("needed_plays", needed_plays)
        assert all(s >= 0 for s in needed_plays)

        play_scores = [p + 1 for p in needed_plays]
        print_list("play_scores", play_scores)
        assert all(s >= 0 for s in play_scores)

        scores = [p + r for p, r in zip(play_scores, match_scores)]
        print_list("scores", scores)
        assert all(s >= 0 for s in scores)

        score = sum(scores)
        print_result(score)

    part1(inp, is_real)
    part2(inp, is_real)



samp_inp = r"""
A Y
B X
C Z
"""

main(samp_inp, False)

real_inp = get_aocd_data()
main(real_inp, True)

