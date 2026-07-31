from functools import *
from collections import *
#from sympy import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
#import numpy as np
#import shapely
#import shapely.ops
from timer_utils import timefunction
#import networkx as nx
#import matplotlib.pyplot as plt
#from construct import *

#from Levenshtein import distance as levenshtein_distance
#from sympy import *

from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
import pyperclip
from icecream import ic
import aocd # https://github.com/wimglenn/advent-of-code-data
# aocd.lines  # like data.splitlines()
# aocd.numbers # uses regex pattern -?\d+ to extract integers from data


from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from quicklambda import _1


@timefunction
def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    lines = inp.strip().split('\n')
#    lines = inp.strip("\n").split('\n')
    ic(len(lines))
    ics(lines)

#    instructions = seq(lines).map(str.split).map(lambda p: (p[0], int(p[1]))).to_list()
    instructions = seq(lines).map(str.split).multimap(identity, int).to_list()
    ics(instructions)

    def check_infinite(instructions, ip=0, acc=0, visited=None):
        inst_count = len(instructions)
        visited = set() if visited is None else visited

        while 1:
            if ip == inst_count:
                return False
            elif ip in visited:
                return True
            else:
                op, val = instructions[ip]
                visited.add(ip)

                if op == "jmp":
                    ip += val
                else:
                    ip += 1

    def run_code(instructions, ip=0, acc=0, visited=None, report = False):
        inst_count = len(instructions)
        visited = set() if visited is None else visited

        while 1:
            if ip == inst_count:
                if report:
                    print("Reached the end!")
                break
            elif ip in visited:
                if report:
                    print("Infinite loop detected!")
                break
            else:
                op, val = instructions[ip]
                visited.add(ip)

                if op == "jmp":
                    ip += val
                else:
                    ip += 1

                    if op == "acc":
                        acc += val

        return acc, visited

    @timefunction
    def part1():
        result, _ = run_code(instructions)
        print_result(result)

    @timefunction
    def part2():
        result = None
        inst_count = len(instructions)

        last_safe_ip = None

        for ip, (op, val) in reversed(list(enumerate(instructions))):
            if op == "jmp" and val < 0:
                break

            last_safe_ip = ip

        ic(last_safe_ip)


            # search for nops that if turned into jumps would hit exact end or last section with no more jumps
        for ip, (op, val) in enumerate(instructions):
            if op == "nop" and ip + val >= last_safe_ip and ip + val <= inst_count:
                print("found")
                ic(ip, op, val)
                result, _ = run_code(new_list(instructions, ip, ("jmp", val)), report = True)
                ic(result)
                break


        _, visited = run_code(instructions)

        if result is None:
            for ip in visited:
                op, val = instructions[ip]

                if op == "jmp":
                    new_inst = new_list(instructions, ip, ("nop", val))
                    if not check_infinite(new_inst, ip=ip+1, visited=set(visited)):
                        print("found")
                        ic(ip, op, val)
                        result, _ = run_code(new_inst, report = True)
                        ic(result)
                        break


            if 0:
                    # seems like highest visited negative jmp could be changed to nop?
                    # not true, can have further negative jumps after that weren't previously visited
                for ip, (op, val) in reversed(list(enumerate(instructions))):
                    if op == "jmp" and val < 0 and ip in visited:
                        ic(ip, op, val)
                        result, _ = run_code(new_list(instructions, ip, ("nop", val)), report = True)
                        ic(result)
                        break



        print_result(result)

    part1()
    part2()

def main():
    if 0:
        for samp_inp in samp_inps:
            print("Sample:")
            run(samp_inp, False)

    if 1:
        print("Actual:")
#        real_inp = aocd.get_data(day=25, year=2021)
            # needs env var AOC_SESSION
        real_inp = aocd.data # supposed to work if filename is clear enough (year would need to be 4-digit)
        run(real_inp, True)
#        aocd.submit(my_answer)




samp_inp = r"""
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""


short_samp = """
"""


samp_inps = [
#    short_samp,
    samp_inp,
    ]


main()

