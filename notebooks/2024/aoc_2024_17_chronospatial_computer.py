# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% editable=false jupyter={"source_hidden": true}
from aoc_utils import *
if is_notebook():
    print(get_aoc_url())

# %% [markdown]
# # Imports

# %%
# %load_ext autoreload

# %%
from collections import *
import re

from icecream import ic
import z3
from z3 import Int, Optimize, If, Real, Solver, Or, And, Xor, BitVec, BitVecs, sat

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module

# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
example

# %%
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0]
sample_data2 = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""

# %%
for sample in sample_data1s:
    print(sample)
    print("=======================")


# %% [markdown]
# # Parse

# %%
def parse_data(inp):
    return string_to_integers_list(inp)


# %% [markdown]
# # Process

# %%
opcodes = "adv,bxl,bst,jnz,bxc,out,bdv,cdv".split(",")

def operand_repr(opcode, operand):
    if opcode in (0,2,5,6,7):
        if operand < 4:
            return operand
        
        return "abc"[operand - 4]
        
    return operand

def opcode_repr(opcode, operand):
    operand_val = operand_repr(opcode, operand)
    if opcode == 0:
        return f"a = a >> {operand_val}"
        #return f"a = a // (1 << {operand_val})"
    if opcode == 1:
        return f"b = b ^ {operand_val}"
    if opcode == 2:
        return f"b = {operand_val} & 7"
    if opcode == 3:
        return f"janz {operand_val}"
    if opcode == 4:
        return f"b = b ^ c"
    if opcode == 5:
        return f"out {operand_val} & 7"
    if opcode == 6:
        #return f"b = a // (1 << {operand_val})"
        return f"b = a >> {operand_val}"
    if opcode == 7:
        #return f"c = a // (1 << {operand_val})"
        return f"c = a >> {operand_val}"
    
    return operand

def program_repr(program):
    #return [f"{n}: {opcode_repr(opcode,operand)} {operand_repr(opcode, operand)}" for (n, opcode),(_, operand) in batched(enumerate(program), 2)]
    return [f"{n}: {opcode_repr(opcode,operand)}" for (n, opcode),(_, operand) in batched(enumerate(program), 2)]


# %%
def process_intcodes(a, b, c, int_codes, max_out=10000, id=None, ics=nothing, input_func = None, output_func = None, state = None):
    def combo(operand):
        if operand < 4:
            return operand
        
        return (a, b, c)[operand - 4]
            
    ip = 0
    inst_len = len(int_codes)
    out_count = 0

    while ip < inst_len:
#        ics(ip, val)
        opcode = int_codes[ip]
        ip += 1
        operand = int_codes[ip]
        ip += 1
        
        match opcode:
            case 0: # ADV
                #a = a // (1 << combo(operand))
                a = a >> combo(operand)
            case 1: # BXL
                b = b ^ operand
            case 2: # BST
                b = combo(operand) & 7
            case 3: # JNZ
                if a:
                    ip = operand
            case 4: # BXC
                b = b ^ c
            case 5: # OUT
                yield combo(operand) & 7
                out_count += 1
                
                if out_count >= max_out:
                    break
            case 6: # BDV
                #b = a // (1 << combo(operand)) & 7 # "& 7" is not part of spec but is valid for actual program
                b = a >> combo(operand)
            case 7: # CDV
                #c = (a // (1 << combo(operand))) & 7 # "& 7" is not part of spec but is valid for actual program
                c = a >> combo(operand)
            case _:
                raise Exception(f"Unknown opcode {opcode}")
                
def process(parsed):
    #ics(parsed)
    [a], [b], [c], program = parsed
    ic("part1", a,b,c,program)
    return ",".join(map(str, process_intcodes(a, b, c, program)))


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
# this method uses specifics of my input data
# it could be conceivably be modified to translate input data into constraints
def process2(parsed):
    [a], [b], [c], program = parsed
    #pr = program_repr(program)
    #ic("part2", a,b,c,len(program),program,pr)

    s = Solver()
    prog_len = len(program)
    int_bits = 3 * (prog_len + 1)
    aas = [BitVec(f"a_{n}", int_bits) for n in range(prog_len)]
    bs = [BitVec(f"b_{n}", int_bits) for n in range(prog_len)]
    last_a = None
    
    for n,i in enumerate(program):
        sa, sb = aas[n], bs[n]

        if last_a is not None:
            s.add(sa == last_a >> 3)
        
        s.add(sb == (sa & 7) ^ 1)
        s.add(i == ((sb ^ 5) ^ (sa / (1 << sb)) & 7) & 7)
        last_a = sa

    s.add(aas[-1] >> 3 == 0)

    if s.check() == sat:
        m = s.model()
        return ic(m.evaluate(aas[0]).as_long())
    else:
        print("failed to solve")


# %%
# this method is roughly 16X faster and only uses general program knowledge rather than specifics like the z3 solution, actually running the simulator repeatedly to get the result
def process2(parsed):
    [a], [b], [c], program = parsed
    # search backwards for parts of a, each output is affected by bits at and to the left of n * 3, where n is the index of the output
    # the trick is that at any step multiple values of a could produce the correct outoutput so far, so we'll use a queue
    def find_a():
        queue = deque()
        put, get = get_queue_functions_fifo(queue)
        put((len(program) - 1, 0))
        
        while queue:
            pos, val = get()
            match = program[pos:]
            
            for pv in range(8):
                if list(process_intcodes(new_a := val + pv, 0, 0, program)) == match:
                    if not pos:
                        return new_a
                    put((pos - 1, new_a << 3))
                    
    return find_a()


# %%
def part2(inp):
    parsed = parse_data(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

for sample_data1 in sample_data1s:
    part1(sample_data1)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp) # 4747842763526860477 is too high

# %%
parsed = parse_data(get_aocd_data())
[a], [b], [c], program = parsed
#a = 164278899142333
a = 164278899142272
ic(program)
#",".join(map(str, process_intcodes(a, b, c, program)))
#",".join(map(str, process_intcodes( 5 << 45 + 5 << 42, 0, 0, program)))
",".join(map(str, process_intcodes(a + 27, 0, 0, program)))

# %%
281474976710656/8

# %%
47513501/8

# %%
1 << 3
a,b = 2321, 5
(a // (1 << b)), (a >> b)

# %%
n = 256
n // 8, n >> 3


# %% [markdown]
# # Others' solutions

# %%
def solve():
    def run(a, b, c):
        return list(process_intcodes(a, b, c, program))
    
    parsed = parse_data(get_aocd_data())
    [a], [b], [c], prog = parsed
    todo = [(len(prog)-1, 0)]
    for pos, val in todo:
        for a in range(val*8, val*8+8):
            if run(a, 0, 0) == prog[pos:]:
                todo += [(pos-1, a)]
                if pos == 0: 
                    print(a)
                    return
                ic(pos, val, a)                    
solve()
