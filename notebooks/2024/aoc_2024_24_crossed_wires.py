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

# %% [markdown]
# [Advent of Code 2024 - Day 24](https://adventofcode.com/2024/day/24)

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

# ic(example)    

# %%
*sample_data1s, sample_data2 = split_example(example)

# %% [markdown]
# # Parse

# %%
Wire = namedtuple("Wire","name,val")
Gate = namedtuple("Gate","a,b,op,out,aval,bval,inp_lvl")
re_wire_val = re.compile(r"-?\d+")

def gate_repr(g):
    # return f"{g.out}={g.a} ({g.aval}) {g.op} {g.b} ({g.bval})"
    return f"{g.out}={g.a} {g.op} {g.b} {g.inp_lvl}"

def wire_val(wire):
    if (m := re_wire_val.search(wire)):    
        return int(m.group(0))
    
    return None

def parse_line1(line):
    parts = line.split(": ")
    return Wire(parts[0], int(parts[1]))

def parse_line2(line):
    a, op, b, _, out = line.split()
    a, b = sorted((a, b)) # this make analysize easier on input wires
    va, vb = wire_val(a), wire_val(b)
    return Gate(a, b, op, out, va, vb, va or vb)

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
step = namedtuple("Step","name,op,sub")
bad_wire = namedtuple("BadWire","op,exp_op,lvl,il")

def out_wire(n):
    return f"z{n:0>2d}"

# looking at data, it appears that any gate with an original input wire has both inputs as original inputs
# different inputs have different depths to resolution
# determine which bit are wrong
# theory: each output zn should only be affected by inputs yn and xn where xn <= zn and yn <= zn
#     every output's first gate is XOR (except last which is cary and thus OR)
# z09 z21, and z45 are wrong
# actually, highest should be an OR from the carry
# each output is 

# 1 bit full adder:
# Sum = A XOR B XOR Cin
# Cout = A AND B OR (Cin AND (A XOR B))

progression = {
    "sumx": ("XOR", "carry", 0, "xori", 0),
    "carry": ("OR", "andi", -1, "andcx", -1),
    "andi": ("AND", "inp", 0, "inp", 0),
    "andcx": ("AND", "xori", 0, "carry", 0),
    "xori": ("XOR", "inp", 0, "inp", 0),
    "z1": ("XOR", "andi", -1, "xori", 0),
    "z2": ("AND", "andi", 0, "xori", 0),
}

ic_null = lambda *a: None if not a else (a[0] if len(a) == 1 else a)

    # 8 wires bad, 4 pairs to swap
def process2(parsed, oper=operator.add):
        # special cases: first has no carry, last only has carry
    def validate(gates_by_out, just_check):
        validated = set()            
        bad_wires = dict()  
        icd = ic_null if just_check else ic
        # icd = ic
        # icd(validate)

            #check the next level
        def probe(out, lvl, prog_key, disp=False):
            op, inpa, alc, inpb, blc = progression[prog_key]
            g = gates_by_out[out]
            gr = gate_repr(g)

            if op != g.op:
                if disp: icd("  probe wrong op", op, gr)
                return False

            if inpa == inpb == "inp": # both are first level inputs
                if g.a not in in_wires and g.b not in in_wires:
                    if disp: icd("  probe wires not inputs", gr)
                    return False
            else:
                if g.a in in_wires and g.b in in_wires:
                    if disp: icd("  probe wires both inputs", gr)
                    return False
                
            return True

        def expected_op(prog_key):        
            op, inpa, alc, inpb, blc = progression[prog_key]
            return op

        def val_recur(out, lvl, prog_key, last_prog = None):
            if out in validated:
                return True

                # special gates for the beginning to account for no carry input for z0
            if lvl == 1:
                if prog_key == "sumx":
                    # icd("switched validate 1", out, gate_repr(gates_by_out[out]))
                    prog_key = "z1"
                elif prog_key == 'andcx':
                    # icd("switched validate 2", out, gate_repr(gates_by_out[out]))
                    prog_key = "z2"
            
            op, inpa, alc, inpb, blc = progression[prog_key]
            g = gates_by_out[out]
            gr = gate_repr(g)
            aop = (t := gates_by_out.get(g.a)) and t.op # will be none if input
            bop = (t := gates_by_out.get(g.b)) and t.op

            if op != g.op:
                icd("unexpected op", op, gr, prog_key, lvl, last_prog)                    
                bad_wires[out] = bad_wire(g.op, op, lvl, g.inp_lvl)
                return False

            if inpa == inpb == "inp": # both are first level inputs
                if not g.a in in_wires and not g.b in in_wires:
                    bad_wires[out] = bad_wire(",".join((g.a, g.b)), "inp", lvl, g.inp_lvl)
                    icd("double not in", gr, lvl)
                    if just_check: return False

                if g.a not in in_wires:
                    bad_wires[g.a] = bad_wire(aop, "inp", lvl, g.inp_lvl)
                    icd("not in", gr.a, gr, lvl)
                    if just_check: return False
                
                if g.b not in in_wires:
                    bad_wires[g.b] = bad_wire(bop, "inp", lvl, g.inp_lvl)
                    icd("not in", gr.b, gr, lvl)
                    if just_check: return False

                assert g.inp_lvl is not None

                if g.inp_lvl != lvl:
                    icd("wrong in level", gr, lvl, op, prog_key, last_prog)
                    if just_check: return False
            else:
                if g.a in in_wires and g.b in in_wires:
                    bad_wires[out] = bad_wire("inp", ",".join((g.a, g.b)), lvl, g.inp_lvl)
                    icd("double in", inpa, inpb, gr, lvl)
                    if just_check: return False
                elif inpa == "inp" or inpb == "inp":
                    raise Exception("shouldn't have only single projected input!")
                else:
                        # check for swapped
                    if probe(g.b, lvl, inpa) and probe(g.a, lvl, inpb):
                        inpa, inpb = inpb, inpa

                    aa = probe(g.a, lvl, inpa)
                    bb = probe(g.b, lvl, inpb)

                    if aa or bb:
                        res = val_recur(g.a, lvl + alc, inpa, prog_key)
                        if just_check and not res: return False
                        res = val_recur(g.b, lvl + blc, inpb, prog_key)
                        if just_check and not res: return False
                    else:
                        # if we get here one or both sub-ops don't match
                        if aa or (ab := probe(g.a, lvl, inpb)):
                            inp = inpb if aa else inpa
                            # probe(g.b, lvl, inp, True)
                            eop = expected_op(inp)
                            bad_wires[g.b] = bad_wire(bop, eop, lvl, g.inp_lvl)
                            icd("bad next op", g.b, op, bop, eop, gr, prog_key, lvl, last_prog)
                            if just_check: return False
                        elif bb or probe(g.b, lvl, inpa):
                            inp = inpa if bb else inpb
                            # probe(g.a, lvl, inp, True)
                            eop = expected_op(inp)
                            bad_wires[g.a] = bad_wire(aop, eop, lvl, g.inp_lvl)
                            icd("bad next op", g.a, op, aop, eop, gr, prog_key, lvl, last_prog)
                            if just_check: return False
                        else: # neither one matched either
                            icd("both bad", inpa, inpb, gr, lvl)
                            bad_wires[out] = bad_wire(g.op, op, lvl, g.inp_lvl)
                            if just_check: return False

            validated.add(out)
            return True

        for n in range(1, out_wire_count-1):
            res = val_recur(out_wire(n), n, "sumx")
            if just_check and not res: return False

        res = val_recur(out_wire(0), 0, "xori") # first output includes no carry
        if just_check and not res: return False
        res = val_recur(last_wire, out_wire_count-1, "carry") # last output is only carry
        if just_check and not res: return False
        return True if just_check else bad_wires            


    wires, gates = parsed
    ic(len(gates))
    gates_by_out = dict((g.out, g) for g in gates)
    gates_by_in = defaultdict(set)

    for g in gates:
         gates_by_in[g.a].add(g)
         gates_by_in[g.b].add(g)

        # input wires start with x or y, output wires with z
    out_wires = sorted(g.out for g in gates if g.out.startswith("z"))
    in_wires = set(wire.name for wire in wires)
    out_wire_count = len(out_wires)
    last_wire = out_wire(out_wire_count-1)
    max_val = 1 << out_wire_count
    ic(out_wire_count, max_val)
    bad_wires = validate(gates_by_out, False)
    ic(len(bad_wires), bad_wires)

    def collect_need(op):
        return list(i[0] for i in bad_wires.items() if i[1].exp_op==op)

    def collect_have(op):
        return list(i[0] for i in bad_wires.items() if i[1].op==op)

    need_xor_wires = collect_need("XOR")
    need_and_wires = collect_need("AND")
    need_or_wires = collect_need("OR")
    have_xor_wires = collect_have("XOR")
    have_and_wires = collect_have("AND")
    have_or_wires = collect_have("OR")
    ic(need_xor_wires, have_xor_wires)
    ic(need_and_wires, have_and_wires)
    ic(need_or_wires, have_or_wires)

    def validate_with_swaps(swaps):
        test_gates = gates_by_out.copy()

        for a, b in swaps:
            test_gates[a] = gates_by_out[b]
            test_gates[b] = gates_by_out[a]

        return validate(test_gates, True)

    def do_swap_tests():
        # cnter = iter(count())
        
        for xor_permutations in itertools.permutations(need_xor_wires):
            test_xors = tuple(zip(have_xor_wires, xor_permutations))

            for and_permutations in itertools.permutations(need_and_wires):
                test_and = tuple(zip(have_and_wires, and_permutations))

                for or_permutations in itertools.permutations(need_or_wires):
                    test_ors = tuple(zip(have_or_wires, or_permutations))

                    swap_wires = test_xors + test_and + test_ors

                    # if (n := next(cnter)) < 5:
                    #     ic(swap_wires)

                    if validate_with_swaps(swap_wires):  
                        return swap_wires
                
    result = do_swap_tests()
    ic(result)

    if result:
        return ",".join(sorted(bad_wires))

    if 0: # analysis
        in_gates = set()
        for w in wires:
            in_gates.update(gates_by_in[w.name])
        ic(sorted(in_gates)[:3])
        # def get_good_bad_gates(out):

        def get_conn_out(out, depth=1000):
            g = gates_by_out.get(out)
    
            if not g or not depth:
                return [out]
            #return f"{out}={get_conn(g.a)} {g.op} {get_conn(g.b)}"
            # return gate_repr(g)
            return [gate_repr(g), get_conn_out(g.a, depth-1), get_conn_out(g.b, depth-1)]
            #  return [gate_repr(g), get_conn(g.a), get_conn(g.b)]

        def get_conn_in(in_, depth=1000):
            in_gates = gates_by_in.get(in_)
    
            if not in_gates or not depth:
                return [in_]
            #return f"{out}={get_conn(g.a)} {g.op} {get_conn(g.b)}"
            # return gate_repr(g)
            return [(gate_repr(g), get_conn_in(g.out, depth-1)) for g in in_gates]
            # return [(gate_repr(g := gates_by_out[gi]), get_conn_in(g.out)) for gi in in_gates]
            #  return [gate_repr(g), get_conn(g.a), get_conn(g.b)]
            
        ic(get_conn_out("z00"))
        ic(get_conn_out("z01"))
        ic(get_conn_out("z02"))
        ic(get_conn_out("z03"))
        # ic(get_conn_out("z12", 4))
        # ic(get_conn_out("z13", 4))
        # ic(get_conn_out("z14", 4))
        ic(get_conn_out(out_wire(out_wire_count-2), 5))
        ic(get_conn_out(last_wire, 5))
        # ic(get_conn_out("z02"))
        # ic(get_conn_in("y44"))
        # ic(get_conn_in("y43"))
        # ic(get_conn_in("x44"))
        # ic(get_conn_in("x01"))

        if 0:
            connections = []

            for wire in out_wires:   
                connections.append(get_conn_out(wire, 1))
            
            ic(connections)
        



# %%
def part2(inp, oper=operator.add):
    parsed = parse_data(inp)
    result = process2(parsed, oper)
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())

for sample_data1 in sample_data1s:
    part1(sample_data1)

if 0: # samples from aocd don't work yet, replaced from hardcoded to put on github
    part2(sample_data2, oper=operator.and_)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)

