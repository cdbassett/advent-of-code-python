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

import sympy as sp
from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from aoc_utils import * # this includes adding c:\ut to sys.path
from utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module


# %% [raw]
#          set b 99
#          set c b            # c <- 99
#          jz a label8
#          mul b 100          # b <- 9900
#          add b 100000       # b <- 109900
#          set c b            # c <- 109900
#          add c 17000        # c <- 126900
#
# label8:  set f 1
#          set d 2
#
# label10: set e 2
#
# label11: set g d
#          mul g e
#          jne g b label16
#          set f 0           # set f to 0 if d * e == b
# label16: add e 1
#          jne e b label11   # for (e=2; e != b; e++)
#
#          add d 1
#          jne d b label10   # for (d=2; d != b; d++)
#
#          jnz f label26
#
#          add h 1           # add 1 to h if f is 0 (previous d * e == b)
#                            # for every number from d:(2 to 126900) * e:(2 to 126900)
#                            # if any e*d == b, inc h
#
# label26: je b c label32
#
#          add b 17          # for (b=109900; b != 126900; b += 17) // 1000 times
#          jmp label8
#
# label32: n o p

# %%

# %% [markdown]
# # Parse

# %%
def parse_line(line):
    return line.split()

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
def try_int(val, default):
    try:
        return int(val)
    except:
        return default

def make_get_val(registers):
    def get_val(val):
        try:
            return int(val)
        except:
            return registers.get(val, 0)
    return get_val

def run(instructions, registers):
    get_val = make_get_val(registers)
    #ics(instructions, len(instructions))
    inst_len = len(instructions)
    ip = 0
    mult_count = 0

    while ip < inst_len:
        inst = instructions[ip]
        #ics(ip, inst, registers)

        match inst:
            case "add", reg, val:
                registers[reg] += get_val(val)
            case "sub", reg, val:
                registers[reg] -= get_val(val)
            case "mul", reg, val:
                registers[reg] *= get_val(val)
                mult_count += 1
            case "mod", reg, val:
                registers[reg] %= get_val(val)
            case "jnz", chk, val:
                if get_val(chk):
                    ip += get_val(val)
                    continue
            case "jgz", chk, val:
                if get_val(chk) > 0:
                    ip += get_val(val)
                    continue
            case "set", reg, val:
                registers[reg] = get_val(val)
            case _:
                raise Exception(f"Unhandled instruction {inst}")

        ip += 1

    return mult_count

def pre_label_reduced(lines):
    lines = list(lines)

    for ip, inst in enumerate(lines):
        match inst:
            case "jnz", chk, val:
                if chk == "0":
                    lines[ip] = ["nop"]
                #elif val == "2" and lines[ip+1][0] == "jnz" and lines[ip+1][1] == "1":
                elif chk == "1" and lines[ip-1][0] == "jnz" and lines[ip-1][2] == "2":
                    lines[ip-1] = ["jz", lines[ip-1][1], str(int(val)+1)] # we are the second instruction, have to adjust
                    lines[ip] = ["nop"]

    return lines

def labeled(parsed):
    labeled_lines = [["", inst] for inst in parsed] + [["", "nop"]] # add extra for out of bounds jumps

    for ip, (label, inst) in enumerate(labeled_lines):
        ics(ip, inst)
        match inst:
            case jmp, chk, val if jmp in ("jnz", "jmp", "jz"):
                new_ip = ip + int(val)
                new_label = f"label{new_ip}"
                #ic(new_ip, label)
                labeled_lines[ip] = [label, [jmp, chk, new_label]]
                labeled_lines[new_ip][0] = new_label
                #inst[2] = label

    return labeled_lines

def get_repr(labeled_lines):
    return "\n".join(f"[{ip:2}] {label+':' if label else '' :9}{' '.join(inst)}" for ip, (label, inst) in enumerate(labeled_lines))

def get_repr_no_ip(labeled_lines):
    return "\n".join(f"{label+':' if label else '' :9}{' '.join(inst)}" for ip, (label, inst) in enumerate(labeled_lines))

def get_comp_repr(parsed, labeled_lines):
    return "\n".join(f"{label:9}{' '.join(inst):15}{' '.join(old)}" for old, (label, inst) in zip(parsed, labeled_lines))

def reduced(labeled_lines):
    labeled_lines = list(labeled_lines)

    for ip, (label, inst) in enumerate(labeled_lines):
        match inst:
            case ("jnz", chk, val) | ("jz", chk, val):
                if chk == "1":
                    labeled_lines[ip][1] = ["jmp", val]

            case ("sub", reg, val) if try_int(val, 0) < 0:
                labeled_lines[ip][1] = ["add", reg, val[1:]]


    return labeled_lines

def remove_nops(labeled_lines):
    labeled_lines = list(labeled_lines)

    for ip, (label, inst) in enumerate(labeled_lines):
        match inst:
            case ["nop"]:
                if label:
                    assert not labeled_lines[ip+1][0] # make sure not a label in next isnt
                    labeled_lines[ip+1][0] = label

    return [[label, inst] for label, inst in labeled_lines if inst[0] != "nop"]

def process(parsed):
    #ics(parsed)
    return run(parsed, defaultdict(int))


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %% [markdown]
# # Process2

# %%
def has_factors(b):
    factors = sp.factorint(b)

    #if b < 110000:
        #ic(b, factors)

    for a in factors.keys():
        if 2 <= a < b:
            return True

    #ic(b, factors)
    return False

def process2(parsed):
       # for every number from d:(2 to 126900) * e:(2 to 126900)
       # if any e*d == b, inc h
    h = 0

    if 0:
        for x in range(109900,126900 + 1,17):
        	for i in range(2,x):
        		if x % i == 0:
        			h += 1
        			break
    else:
        ic(len(list(range(109900, 126900+1, 17))))
        for b in range(109900, 126900+1, 17):
            if has_factors(b):
                h += 1
    return h

    if 0:
        lines = pre_label_reduced(parsed)
        #print("Reduced 1:")
        #ic(lines)
        #print("\n".join(" ".join(line) for line in lines))
        labeled_lines = labeled(lines)
        #print("Labeled:")
        #print(get_repr(labeled_lines))
        labeled_lines = reduced(labeled_lines)
        #print("Reduced 2:")
        #print(get_repr(labeled_lines))
        #print(get_comp_repr(parsed, labeled_lines))
        labeled_lines = remove_nops(labeled_lines)
        #print("De-nopped:")
        print(get_repr_no_ip(labeled_lines))

    return run(parsed, defaultdict(int, {"a": 1 }))


# %%
def part2(inp):
    parsed = parse(inp)
    result = process2(parsed)
    print_result(result)


# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)
#ic(real_inp)
