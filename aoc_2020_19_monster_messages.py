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
from icecream import ic

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

icf = ic.format

@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
        lines = inp.strip().split('\n')
#        lines = inp.strip("\n").split('\n')
        rule_lines, messages = split_iterable(lines, "")

        rules = seq(rule_lines).map(colon_space_splitter).multimap(int, identity).to_dict()
#        ics(messages)
        return rules, messages



    def process(rules, messages):
        @cache
        def build_rules_desc(rule_num):
            rule_desc = rule_descs[rule_num]

            if isinstance(rule_desc, str):
                return rule_desc

#            if any(rule_num in or_piece for or_piece in rule_desc):
#                return

            or_parts = [sjoin(build_rules_desc(sub_rule_num) if sub_rule_num != rule_num else str(rule_num) for sub_rule_num in or_piece) for or_piece in rule_desc]
            return "(" + "|".join(or_parts) + ")"


        def letter_rule_func(rule_num, letter, msg, level=0):
#            ics(rule_num, letter, msg)
            return 1 if msg[0:1] == letter else 0

        def sub_rule_func(rule_num, or_pieces, msg, level=0):
            for or_piece in or_pieces:
                working_msg = msg
                padding = "   |" * level
#                ics(padding, rule_num, or_piece, msg, level)
#                print_sample(f"{padding}{rule_num}: {or_piece}, {msg}, {level}")
                total_consumed = 0

                for sub_rule_num in or_piece:
                    sub_func = rule_funcs[sub_rule_num]
                    consumed = sub_func(working_msg, level + 1)
#                    ics(sub_rule_num, consumed, working_msg)
#                    print_sample(f"{padding}  {sub_rule_num}: {working_msg} - {consumed}")

                    if not consumed:
                        total_consumed = 0
                        break

                    total_consumed += consumed
                    working_msg = working_msg[consumed:]

#                print_sample(f"{padding}  {rule_num}: {'matched' if total_consumed else 'unmatched'}! {total_consumed}, {working_msg}")

                    # failure happens when either sub_func failed, leaving remainder, or there was text left after all rules matched
                if total_consumed:
#                    print_sample(f"{padding}  {rule_num}: success, {total_consumed}, {msg}")
                    return total_consumed

#            print_sample(f"{padding}  {rule_num}: failure, {msg}")
            return 0 # nothing matched


        rule_funcs = {}
        rule_descs = {}

        for rule_num, text in rules.items():
            if text.startswith('"'):
#                rule_funcs[rule_num] = partial(operator.eq, text[1])
                rule_funcs[rule_num] = partial(letter_rule_func, rule_num, text[1])
                rule_descs[rule_num] = text[1]
#                ics(rule_num, text[1])
            else:
                or_pieces = seq(bin_or_splitter(text)).map(str.split).map(partial(map_tuple, int)).to_tuple()
#                ics(rule_num, or_pieces)
#                rule_funcs[rule_num] = [tuple_map(*()) for or_piece in or_pieces]
                rule_funcs[rule_num] = partial(sub_rule_func, rule_num, or_pieces)
                rule_descs[rule_num] = or_pieces

#        ics(build_rules_desc(8))
#        ics(build_rules_desc(11))
#        ics(build_rules_desc(42))
#        ics(build_rules_desc(31))
#        ics(build_rules_desc(0))

        base_rule = rule_funcs[0]
        matched_cnt = 0

        for n, msg in enumerate(messages):
            matched = base_rule(msg) == len(msg)
            ics(n, msg, matched)

            if matched:
                matched_cnt += 1

        return matched_cnt


    @timefunction
    def part1(inp):
        rules, messages = data_parse(inp)
        result = process(rules, messages)
        print_result(result)


    @timefunction
    def part2(inp):
        rules, messages = data_parse(inp)
#        rules[8] = "42 | 42 8"
#        rules[11] = "42 31 | 42 11 31"
            # cheating for asnwer by rearranging ruls rather than backtracking
            # 42 is only ever referenced from rules 8 and 11
            # so really rule is at least 2 42s, then at least 1 31, but greedily accept as many as there are
            # so really rule is at least one 42 then matching number of 42s then 31, at least one of each
            # we'll build rules for up to 4 extra 42s, and 4 pairs of 42 then 31
        rules[8] = "42"
        rule_base = ["42 " * n + "31 "  * n for n in range(4, 0, -1)] # 4 to 1
        use_rule = "| ".join("42 " * n  + rb for rb in rule_base for n in range(4, -1, -1)).strip() # 4 to 0
        ics(use_rule)
        rules[11] = use_rule
        ics(sorted(rules.items()))
        result = process(rules, messages)
#        result = process(rules, messages[2:3])
        print_result(result)

    part1(inp1)
    part2(inp2)

def main():
    if 1:
        if samp_inps:
            for n, samp_inp in enumerate(samp_inps, 1):
                print(f"{Fore.GREEN}{Style.BRIGHT}Sample {n}:{Style.RESET_ALL}")
                run(samp_inp, samp_inp, False)
        else:
            print(f"{Fore.BLUE}{Style.BRIGHT}Sample:{Style.RESET_ALL}")
            run(samp_inp1, samp_inp2, False)

    if 1:
        print(f"{Fore.YELLOW}{Style.BRIGHT}Actual:{Style.RESET_ALL}")
        real_inp = get_aocd_data()
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)




samp_inp1 = r"""
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
"""

samp_inp2 = samp_inp1
samp_inp2 = """
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
"""


short_samp = """
"""


samp_inps = [
#    short_samp,
#    samp_inp,
    ]


main()

