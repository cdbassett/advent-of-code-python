from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
from utils.timer_utils import timefunction

from sympy import *

from colorama import Fore, Style
from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
import pyperclip
from icecream import ic

from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
import utils.seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it
from utils.quicklambda import _1, _2



@timefunction
def run(inp1, inp2, is_real):
    insert_sample_functions(is_real, globals())

    def data_parse(inp):
#        lines = inp.strip().split('\n')
        lines = inp.strip().split(',')
        parsed = map_list(int, lines)
        return parsed


    def mem_repr(memory):
#        ics(memory.keys())
        min_key = min(memory.keys())
        max_key = max(memory.keys())
        return [memory[n] for n in range(min_key,max_key+1)]

    ADD = 1
    MULT = 2
    INPUT = 3
    OUTPUT = 4

    def process_intcodes(int_codes, inputs=[]):
        def read_val(param_ndx, mode=0):
            addr = ip + param_ndx + 1
            val = memory[addr]
#            ic(addr, val, memory[val], mode)

            if not mode:
                val = memory[val]

            return val


        def get_inp_out_idx():
#            values = [read_val(param_ndx, mode) for param_ndx, mode in zip(range(3), modes)]
#            ic(ip, val, op, modes, values)
#            return values[:2], values[-1]
            return get_double(), read_val(2,1)
    #        params = [memory[n] for n in range(ip+1,ip+4)]
    ##        return (memory[memory[ip+1]], memory[memory[ip+2]]), memory[ip+3]
    #        return (memory[params[0]], memory[params[1]]), params[-1]

        def get_single():
            return read_val(0, mode1st)

        def get_double():
            return (read_val(0, mode1st), read_val(1, mode2nd))

        ip = 0
        inst_len= len(int_codes)
        memory = defaultdict(int)
        memory.update(enumerate(int_codes))
        outputs = []
        input_iter = iter(inputs)

        while ip < inst_len:
#            ic(ip)
#            ic(memory[225])
            val = memory[ip]
            op = val % 100
            modes = map_tuple(int, str(val // 100).zfill(3))
            mode3rd, mode2nd, mode1st = modes
#            mode1st, mode2nd, mode3rd = modes
            instr = [memory[n] for n in range(ip, ip + 4)]
#            ic(ip, op, modes, instr)
#            ics(ip, val, op, modes, mem_repr(memory))

            match op:
                case 1: # ADD
                    inp, out_idx = get_inp_out_idx()
                    res = sum(inp)
#                    ic("ADD", inp, res, out_idx, memory[out_idx])
                    memory[out_idx] = res
                    ip += 4
                case 2: # MULTIPLY
                    inp, out_idx = get_inp_out_idx()
                    res = prod(inp)
#                    ic("MULTIPLY", inp, res, out_idx, memory[out_idx])
                    memory[out_idx] = res
                    ip += 4
#                    ics(ip)
                case 3: # INPUT
                    out_idx = memory[ip+1]
                    input = next(input_iter)
#                    ic("INPUT", input, out_idx, memory[out_idx])
                    memory[out_idx] = input
                    ip += 2
                case 4: # OUTPUT
                    res = get_single()
#                    ic("OUTPUT", res)
                    outputs.append(res)
                    ip += 2
                case 5: # JUMPIFTRUE
                    chk, addr = get_double()

                    if chk:
                        ip = addr
                    else:
                        ip += 3
                case 6: # JUMPIFFALSE
                    chk, addr = get_double()

                    if not chk:
                        ip = addr
                    else:
                        ip += 3
                case 7: # LESSTHAN
                    inp, out_idx = get_inp_out_idx()
                    memory[out_idx] = int(inp[0] < inp[1])
                    ip += 4
                case 8: # EQUALS
                    inp, out_idx = get_inp_out_idx()
                    memory[out_idx] = int(inp[0] == inp[1])
                    ip += 4
                case 99:
                    break
                case _:
                    raise Exception(f"Unknown op {op}")

        ic(outputs)
        return memory, outputs


    def process1(parsed, inputs):
        memory, outputs = process_intcodes(parsed, inputs)
        return outputs[-1]

    @timefunction
    def part1(inp):
        parsed = data_parse(inp)
        ics(parsed)
        result = process1(parsed, [1])
        print_result(result)

    process2 = process1

#    def process2(parsed):

    @timefunction
    def part2(inp):
        parsed = data_parse(inp)
        ics(parsed)
        result = process1(parsed, [5])
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

