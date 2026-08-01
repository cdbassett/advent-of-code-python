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

# %% editable=false
from utils.aoc_utils import *
if is_notebook():
    print(get_aoc_url())

# %% [markdown]
# # Imports

# %%
# %load_ext autoreload

# %%
import os
import sys
from collections import *
import re
import math
import operator
import random

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module

# %% [markdown]
# # Sample Data

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
sample_data1s = [split_example(example)[0], """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""]
sample_data2 = """x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00"""

# %% [markdown]
# # Parse

# %%
Wire = namedtuple("Wire","name,val")
Gate = namedtuple("Gate","a,b,op,out")

def parse_line1(line):
    parts = line.split(": ")
    return Wire(parts[0], int(parts[1]))

def parse_line2(line):
    a, op, b, _, out = line.split()
    return Gate(a,b,op,out)

def parse_data(inp):
    parts = inp.strip().split("\n\n")
    return seq(parts[0].strip().split("\n")).map(parse_line1).list(), seq(parts[1].strip().split("\n")).map(parse_line2).list()


# %% [markdown]
# # Process

# %%
ops = {
    "AND": operator.and_,
    "OR": operator.or_,
    "XOR": operator.xor,
}

def process(parsed):
    # cache 
    def value(wire):
        v = wire_values.get(wire)
        
        if v is None:
            g = gates_dict[wire]
            v = ops[g.op](value(g.a), value(g.b))
        return v            
    
    #ics(parsed)
    wires, gates = parsed
    wire_values = dict(wires)
    gates_dict = dict((g.out, g) for g in gates)

    for g in gates:
        wire_values[g.out] = value(g.out)

    #ics(wire_values)
    wire_z_vals = sorted((w for w in wire_values.items() if w[0].startswith("z")), reverse=True)
    #ics(wire_z_vals)
    return int(sjoin(str(w[1]) for w in wire_z_vals), 2)


# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
# looking at data, it appears that any gate with an original input wire has both inputs as original inputs
# different inputs have different depths to resolution
# determine which bit are wrong
# theory: each output zn should only be affected by inputs yn and xn where xn <= zn and yn <= zn
#     every output's first gate is XOR
# z09 z21, and z45 are wrong
# each putput is 
def gate_repr(g):
    return f"{g.out}={g.a} {g.op} {g.b}"
    
def process2(parsed, oper=operator.add):
    wires, gates = parsed
    ic(len(gates))
    gates_dict = dict((g.out, g) for g in gates)
    out_wires = sorted(g.out for g in gates if g.out.startswith("z"))
    wire_count = len(out_wires)
    ics(out_wires)
    max_val = 1 << wire_count
    ic(wire_count, max_val)

    if 0: # analysis
        def get_conn(out):
            g = gates_dict.get(out)
    
            if not g:
                return [out]
            #return f"{out}={get_conn(g.a)} {g.op} {get_conn(g.b)}"
            return [gate_repr(g), get_conn(g.a), get_conn(g.b)]
            
        connections = []

        for out_wire in out_wires:   
            connections.append(get_conn(out_wire))
        
        ic(connections)
        
    def value(wire_values, wire):
        v = wire_values.get(wire)
        
        if v is None:
            g = gates_dict[wire]
            v = ops[g.op](value(wire_values, g.a), value(wire_values, g.b))
        return v            

    def val_to_wire_vals(val, prefix):
        return dict((f"{prefix}{n:02}", (val >> n) & 1) for n in range(wire_count))

    def final_value(x_val, y_val):
        wire_values = val_to_wire_vals(x_val, "x")
        wire_values.update(val_to_wire_vals(y_val, "y"))
        pv = partial(value, wire_values)
        return int(sjoin(str(pv(w)) for w in out_wires), 2)
                    

    def gate_is_input(g):
        return g.a[0] in "xy" or g.b[0] in "xy"
        

    if 0:
        for n in range(10):
            x, y = random.randint(0, max_val), random.randint(0, max_val)
            ics(x, y, final_value(x, y), oper(x, y)) 

    if 0:
        wrong_bits = set()
        wrong_bits_set = 0
        wrong_bits_clear = 0
        
        for n in range(100):
            x, y = random.randint(0, max_val), random.randint(0, max_val)
            expected = oper(x, y)
            actual = final_value(x, y)
            ics(x, y, expected, actual) 
            #num.bit_count()
            wrong_bits_set |= (expected ^ actual)
        
        #num.bit_count()
        ic(bin(wrong_bits_set))

    #ic(list((out, gates_dict[out].op) for out in out_wires))
    #ic(list(gate_repr(gates_dict[out]) for out in out_wires))
    #ic(list(gate_repr(gates_dict[out]) for out in out_wires if gates_dict[out].op != "XOR"))
    #ic(list(gate_repr(g) for g in gates if (g.a[0] in "xy" or g.b[0] in "xy") and g.op == "XOR"))
    right_entry_gates = set(out for out in out_wires if gates_dict[out].op == "XOR")
    #wrong_entry_gates = list(gates_dict[out] for out in out_wires if gates_dict[out].op != "XOR")
    wrong_entry_gates = list(gates_dict[out] for out in out_wires if out not in right_entry_gates)
    ic(map_list(gate_repr, wrong_entry_gates))
    xor_gates = list(g for g in gates if g.op == "XOR" and g.out not in right_entry_gates)
    #ic(len(xor_gates), xor_gates)
    #reduced_xor_gates = list(g for g in xor_gates if not gate_is_input(g)) 
    #ic(len(reduced_xor_gates), reduced_xor_gates)

    if 0:
        possibles = []
    
        for chk_gates in permutations(xor_gates, 4):
            old_gates_dict = gates_dict
            gates_dict = dict(gates_dict)
    
            for gb, gn in zip(wrong_entry_gates, chk_gates):
                gates_dict[gb.out], gates_dict[gn.out] = gates_dict[gn.out], gates_dict[gb.out]
    
            try:
                if all(oper(x, y) == final_value(x, y) for x, y in product((0, max_val-1), repeat = 2)):
                    possibles.append(gb, gn)
                    ic(possibles)
            except RecursionError:
                pass
        
            gates_dict = old_gates_dict
    
        ic(possibles)


    def validate(g, n):
        a, b = gates_dict[g.a], gates_dict[g.b]

        #     every output's first gate is XOR
        def cond1(a, b):
            return gate_is_input(a) and a.op == "XOR" and b.op == "OR" and not gate_is_input(b)
        
        if not ((f:=cond1(a, b)) or (s:=cond1(b, a))):
            ic(n, "Expected XOR of input and OR of non-input", gate_repr(g), gate_repr(a), gate_repr(b))
            return

        c = b if f else a
        assert c.op == "OR"
        d, e = gates_dict[c.a], gates_dict[c.b]
        
        def cond2(a, b):
            return gate_is_input(a) and a.op == "AND" and not gate_is_input(b) and b.op == "AND"
            
        if not ((f:=cond2(d, e)) or (s:=cond2(e, d))):
            ic(n-1, "Expected AND of input and AND of non-input", gate_repr(c), gate_repr(d), gate_repr(e))
            return

        return
        h = e if f else d
        assert h.op == "AND"
        i, j = gates_dict[h.a], gates_dict[h.b]
        
        def cond3(a, b):
            return gate_is_input(a) and a.op == "XOR" and b.op == "OR"
            
        if not ((f:=cond3(i, j)) or (s:=cond3(i, j))):
            ic(n-2, "Expected XOR of input and OR", gate_repr(c), gate_repr(d), gate_repr(e))
            return

    

    def swap(a, b):
        gates_dict[a], gates_dict[b] = gates_dict[b], gates_dict[a]

    swap("z39", "jct")
    swap("z21", "rcb")
    swap("z09", "gwh")
    swap("wbw", "wgb")
    
    for n, out in enumerate(out_wires[3:], 3):
        g = gates_dict[out]

        if g.op == "XOR":
            validate(g, n)
    
    return ",".join(sorted(["z39", "jct", "z21", "rcb", "z09", "gwh","wbw", "wgb"])) # right answer


# %%
def part2(inp, oper=operator.add):
    parsed = parse_data(inp)
    result = process2(parsed, oper)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

#for sample_data1 in sample_data1s:
#    part1(sample_data1)

if 0: # samples from aocd don't work yet, replaced from hardcoded to put on github
    part2(sample_data2, oper=operator.and_)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)

