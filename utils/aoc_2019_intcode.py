from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import operator
import queue


from utils.aoc_utils import * # this includes adding c:\ut to sys.path

print("loaded aoc_2019_intcode")
from icecream import ic


def mem_repr(memory):
#        ics(memory.keys())
    min_key = min(memory.keys())
    max_key = max(memory.keys())
    return [memory[n] for n in range(min_key,max_key+1)]

def parse_intcodes(inp):
    lines = inp.strip().split(',')
    parsed = map_list(int, lines)
    return parsed

binops = {
    1: operator.add,
    2: operator.mul,
    7: operator.lt,
    8: operator.eq,
}

retrieve_state_id="RTRVSTATE"
#set_state_id="SETSTATE"


IntCodeState = namedtuple("IntCodeState", "ip,relative,mem")


# start with :
#     generator = process_intcodes(parsed, ics=ics)
# send and receive a value:
#     output = generator.send(input)
# just receive a value without sending:
#     output = next(generator)
def process_intcodes(int_codes, id=None, ics=nothing, input_func = None, output_func = None, state = None):
    def read_val(param_ndx, mode=0):
        addr = ip + param_ndx + 1
        val = memory[addr]
#            ic(addr, val, memory[val], mode)

        match mode:
            case 2: # relative
                val = memory[val + relative]
            case 1: # immediate
                pass
            case 0: # position
                val = memory[val]
            case _:
                raise Exception(f"Unknown mode {mode}")

        return val

    def get_out_idx(param_ndx, mode):
        addr = ip + param_ndx + 1
        val = memory[addr]
        assert mode != 1
        return (val + relative) if mode == 2 else val

    def get_inp_out_idx():
#            values = [read_val(param_ndx, mode) for param_ndx, mode in zip(range(3), modes)]
#            ic(ip, val, op, modes, values)
        return get_double(), get_out_idx(2, mode3rd)

    def get_single():
        return read_val(0, mode1st)

    def get_double():
        return (read_val(0, mode1st), read_val(1, mode2nd))

    def get_state():
#        return ip, relative, tuple(memory.values())
#        return ip, relative, tuple(set(dict_diff(tuple(memory.values())
#        return ip, relative, tuple(p for p in sorted(set(memory.items())-set(enumerate(int_codes))) if p[1])
        return IntCodeState(ip, relative, tuple(sorted(set(memory.items())-set(enumerate(int_codes)))))

    def set_state(state):
        nonlocal ip, relative
        ip, relative, mem = state
        memory.clear()
        memory.update(enumerate(int_codes))
        memory.update(mem)


    ip = 0
    inst_len = len(int_codes)
    memory = defaultdict(int)
    q = queue.Queue()
    relative = 0
    memory.update(enumerate(int_codes))

    if state is not None:
        ip, relative, mem_values = state
        memory.update(mem_values)

    while ip < inst_len:
        val = memory[ip]
#        ics(ip, val)
        op = val % 100
        modes = map_tuple(int, str(val // 100).zfill(3))
        mode3rd, mode2nd, mode1st = modes
#            mode1st, mode2nd, mode3rd = modes
        instr = [memory[n] for n in range(ip, ip + 4)]
#            ic(ip, op, modes, instr)
#            ics(ip, val, op, modes, mem_repr(memory))

        if (binop := binops.get(op)) is not None:
            inp, out_idx = get_inp_out_idx()
            res = int(binop(*inp))
#            ic(binop, inp, res, out_idx, memory[out_idx])
            memory[out_idx] = res
            ip += 4
        else:
            match op:
                case 3: # INPUT
                    out_idx = get_out_idx(0, mode1st)

                    if not q.empty():
                        input = q.get()
                        ics(id, "INPUT from queue", input, out_idx, memory[out_idx])
                    else:
                        if input_func:
                            ics(id, "INPUT before input_func")
                            input = input_func()
                        else:
                            ics(id, "INPUT before yield")
                            input = (yield) # yields None
                            if input is None:
                                break
                            ics(id, "INPUT", input, out_idx, memory[out_idx])

                    if input is retrieve_state_id:
                        #ic("get_state", ip, relative)
                        input = (yield get_state())

                        if input is not None:
                            q.put(input)

                        continue
                    elif isinstance(input, IntCodeState):
                        #ic("set_state", ip, relative)
                        set_state(input)
                        #ic(ip, relative)
                        continue

                    memory[out_idx] = input
                    ip += 2
                case 4: # OUTPUT
                    res = get_single()
                    ics(id, "OUTPUT", res)

                    if output_func:
                        output_func(res)
                    else:
                        input = (yield res)

                        if input is not None:
                            q.put(input)

                        ics(id, "OUTPUT after yield", res, input)
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
                case 9: # RELATIVE
                    relative += get_single()
                    ip += 2
                case 99:
                    break
                case _:
                    raise Exception(f"Unknown op {op}")

def send_intcode_string(s, generator):
    outputs = []
    last = None

    for c in s:
        if (output := generator.send(ord(c))) is not None:
            outputs.append(chr(last := output))

    # any returned string and whether currently waiting for input
    return sjoin(outputs), last is not None


# pulls until generator is waiting for input
def read_intcode_string(generator):
    outputs = []
#    halted = False


    try:
        while (output := generator.send(None)) is not None:
            outputs.append(chr(output))
    except StopIteration as e:
        pass
#        return sjoin(outputs), e


#    return ic(sjoin(outputs))
    return sjoin(outputs)


def send_and_receive_intcode_string(generator, s=""):
    if s:
        s, waiting = send_intcode_string(s, generator)

        if not waiting:
            return s

    return s + read_intcode_string(generator)
#
#        r, e = read_intcode_string(generator)
#
#
#    try:
#        return s + read_intcode_string(generator)
#    except StopIteration:
#        print("interrupted: " + s)
#        raise
#

