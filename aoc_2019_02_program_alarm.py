from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
from timer_utils import timefunction

from sympy import *

from colorama import Fore, Style
from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
import pyperclip
from icecream import ic

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from quicklambda import _1, _2



@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
#        lines = inp.strip().split('\n')
        lines = inp.strip().split(',')
        parsed = map_list(int, lines)
        return parsed

    def mem_repr(memory):
        ics(memory.keys())
        min_key = min(memory.keys())
        max_key = max(memory.keys())
        return [memory[n] for n in range(min_key,max_key+1)]

    def process_intcodes(int_codes):
        def get_inp_out_idx():
            values = memory[memory[ip+1]], memory[memory[ip+2]], memory[ip+3]
            ic(ip, op, values)
            return values[:2], values[-1]

#            return (int_codes[int_codes[ip+1]], int_codes[int_codes[ip+2]]), int_codes[ip+3]
#            return (int_codes[int_codes[ip+1]], int_codes[int_codes[ip+2]]), int_codes[ip+3]

        ip = 0
        inst_len= len(int_codes)
        memory = defaultdict(int)
        memory.update(enumerate(int_codes))

        while ip < inst_len:
            op = memory[ip]
            ics(ip, op, mem_repr(memory))

            match memory[ip]:
                case 1:
                    inp, out_idx = get_inp_out_idx()
                    memory[out_idx] = sum(inp)
                case 2:
                    inp, out_idx = get_inp_out_idx()
                    memory[out_idx] = prod(inp)
                case 99:
                    break
            ip += 4

        return memory


    def process_intcodes(int_codes, inputs=[]):
        def read_val(param_ndx, mode=0):
            val = memory[ip + param_ndx + 1]

            if not mode:
                val = memory[val]

            return val


        def get_inp_out_idx():
#            values = [read_val(param_ndx, mode) for param_ndx, mode in zip(range(3), modes)]
#            ic(ip, val, op, modes, values)
#            return values[:2], values[-1]
            return (read_val(0, mode1st), read_val(1, mode2nd)), read_val(2,1)
    #        params = [memory[n] for n in range(ip+1,ip+4)]
    ##        return (memory[memory[ip+1]], memory[memory[ip+2]]), memory[ip+3]
    #        return (memory[params[0]], memory[params[1]]), params[-1]

        def get_single(modes):
            return read_val(0, modes[0])

        ip = 0
        inst_len= len(int_codes)
        memory = defaultdict(int)
        memory.update(enumerate(int_codes))
        outputs = []
        input_iter = iter(inputs)

        while ip < inst_len:
#            ic(ip)
            val = memory[ip]
            op = val % 100
            modes = map_tuple(int, str(val // 100).zfill(3))
#            mode3rd, mode2nd, mode1st = modes
            mode1st, mode2nd, mode3rd = modes
#            ic(ip, val, op, modes)
#            ics(ip, val, op, modes, mem_repr(memory))

            match op:
                case 1:
                    inp, out_idx = get_inp_out_idx()
                    res = sum(inp)
#                    ic("add", res, out_idx, memory[out_idx])
                    memory[out_idx] = res
                    ip += 4
                case 2:
                    inp, out_idx = get_inp_out_idx()
                    memory[out_idx] = prod(inp)
                    ip += 4
#                    ics(ip)
                case 3:
                    out_idx = memory[ip+1]
                    input = next(input_iter)
#                    ic("input", input, out_idx, memory[out_idx])
                    memory[out_idx] = input
                    ip += 2
                case 4:
                    res = get_single(memory, ip, modes)
#                    ic("output", res, out_idx)
                    outputs.append(res)
                    ip += 2
                case 99:
                    break
                case _:
                    raise Exception(f"Unknown op {op}")

#        ics(outputs)
        return memory


    def process1(parsed):
        return process_intcodes(parsed)

    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)

        if is_real:
            parsed[1] = 12
            parsed[2] = 2

        memory = process1(parsed)
        result = memory[0]
        print_result(result)

    process2 = process1

#    def process2(parsed):

    @timefunction
    def part2(inp):
        parsed = data_parse(inp)

        for noun, verb in product(range(100), range(100)):
            parsed[1] = noun
            parsed[2] = verb
            memory = process2(parsed)

            if 19690720 == memory[0]:
                result = 100 * noun + verb
                print_result(result)
                break


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
            # needs env var AOC_SESSION
        real_inp = get_aocd_data()
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)




samp_inp1 = r"""
1,9,10,3,2,3,11,0,99,30,40,50
"""

samp_inp2 = samp_inp1


samp_inps = [
#    "1,9,10,3,2,3,11,0,99,30,40,50",
#    "1,0,0,0,99",
#    "2,3,0,3,99",
#    "2,4,4,5,99,0",
#    "1,1,1,4,99,5,6,0,99",
    ]


main()

