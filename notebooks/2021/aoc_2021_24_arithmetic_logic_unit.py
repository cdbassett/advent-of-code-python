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
import pyperclip
from z3 import Int, Optimize, If, Real, Solver, Or, And, sat, unsat

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils
from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module


# %% [markdown]
# # Parse

# %%
def parse_data(inp):
    return seq(inp.strip().split("\n")).map(str.split).list()


# %%
def build_instructions(xs, ys, zs):
    test_inst = njoin(
    f"""inp w
mul x 0
add x z
mod x 26
div z {z}
add x {x}
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y {y}
mul y x
add z y""" for x,y,z in zip(xs, ys, zs))
    return test_inst


# %%
# attempt to use sympy and run through simulation with variables for inputs
# seemed to be wroking, but afte a few inputs it essentially stopped, presumably due to the complexity
    vars = { "x": 0, "y": 0, "z": 0 }
    w = sp.symbols("w")
#    all_ws = symbols(" ".join(f"w{n}" for n in range(14)))
    all_ws = (sp.symbols(f"w{n}", real=True) for n in range(14))
    w_iter = iter(all_ws)
    cur_w = None
    divisors = [10 ** n for n in reversed(range(14))]
#    ic(divisors)
    divisors_iter = iter(divisors)

        # real instructions only ever input to w, and then only use w as src
        # real instructions only ever mod or div by literal number
        # real instructions only ever mul by 0 or var
        # multiply x by zero results in zero even when x contains a symbol
        # use rotating symbol for w, realtime values for other vars
    for ip, instruction in enumerate(instructions):
        ics(ip, instruction)
        match instruction:
            case ["inp", dst]:
#                cur_w = (w // next(divisors_iter)) % 10
                cur_w = next(w_iter)

            case [instr, dst, src]:
                src_val = cur_w if src == "w" else vars[src] if src in vars else int(src)

                match instr:
                    case "add":
                        vars[dst] += src_val
                    case "mul":
                        vars[dst] *= src_val
                    case "div":
                        #vars[dst] //= src_val
                        vars[dst] = (vars[dst] - (vars[dst] % src_val)) / src_val
#                        vars[dst] /= src_val
                    case "mod":
                        vars[dst] %= src_val

                    # real instructions only eql 2 at a time, like this:
                    #    eql x w
                    #    eql x 0
                    # so 0 if x == w else 1
                    # and w is always within 1-9

                    case "eql":
#                        vars[dst] = int(vars[dst] == src_val)
#                        vars[dst] = Eq(vars[dst], src_val))
                        x = vars["x"]
                        if src == "0":
                            vars[dst] = ((x - cur_w) / cur_w) % 1
                    case _:
                        raise Exception(repr(instr))
            case _:
                raise Exception(repr(instruction))
    z = vars["z"]
    ic(z)
#    ivl = Interval(11111111111111,99999999999999)
#    print(minimum(z, w, ivl))
#    print(maximum(z, w, ivl))

#    ic(solve(z, w))
    if 1:
        ic(z.subs(w, 11111111111111))
        ic(z.subs(w, 11111111111111 * 2))
        ic(z.subs(w, 11111111111111 * 3))
        ic(z.subs(w, 11111111111111 * 4))
        ic(z.subs(w, 11111111111111 * 5))
        ic(z.subs(w, 11111111111111 * 6))
        ic(z.subs(w, 11111111111111 * 7))
        ic(z.subs(w, 11111111111111 * 8))
        ic(z.subs(w, 11111111111111 * 9))

#    for model in range(99999999999999, 11111111111111, -1):
#        res = z.subs(w, model)
#        ic(model, res)


# %%
# attempt to use simpy with interpretation of constraints
# did not succeed, but z3 did
        all_ws = [sp.symbols(f"w{n}", real=True) for n in range(14)]
        equations = []
        #w_old, c_old = 0, 0
        stack = []

        for n, a, b, c, w in zip(count(), As, Bs, Cs, all_ws):
            if a == 1:
                equations.append(w >= 1)
                equations.append(w <= 9)
                stack.append(w + c)
            else:
                past_z = stack.pop()
                #equations.append(sp.Eq(w, b + w_old + c_old))
                equations.append(sp.Eq(w, b + past_z))

            #w_old, c_old = w, c

        ics(equations)
        #res = sp.solvers.inequalities.reduce_rational_inequalities(equations, [])
        res = sp.reduce_inequalities(equations, [])
        ic(res)
        #solution = sp.solve(equations, t)


# %% [markdown]
# # Process

# %%
def get_comp_repr(instructions, labeled_lines):
    return "\n".join(f"{' '.join(map(str, old)):20}  {' '.join(map(str, inst)):15}" for old, inst in zip(instructions, labeled_lines))

def process(parsed):
    ic(len(parsed))
    instructions = parsed
    """
    w = input
    if B < 0:
        z = z // 26
    if (z % 26 + B) != w: # only B can be negative
        z = z * 26 + (w + C)   # A is 1 or 26, 26 if B is negative

    breaks down into 2 functions (7 off each):
    if A is 26, B is negative, so:
    w = input
    z = (z // 26)
    if (z % 26 + B) != w:
        z *= 26 + (w + C)

    otherwise A is 1 and B is 10-16, so:
    w = input
    z = z * 26 + (w + C)

    for z to be 0 at the end we must have no additional multiplications in 2nd type, which means
    w_cur must be equal b_cur + w_old + c_old
    """
    # a true general solution would pull these numebrs from the input
    # not too hard, but I'm tired of this problem
    Bs = [ 15, 11, 10, 12, -11, 11, 14, -6, 10, -6, -6, -16, -4, -2 ] # B
    Cs = [ 9, 1, 11, 3, 10, 5, 0, 7, 9, 15, 4, 10, 4, 9 ] # C
    As = [ 1, 1, 1, 1, 26, 1, 1, 26, 1, 26, 26, 26, 26, 26 ] # A
    # A = 26 if B < 0 else 1
    ic(As == [26 if n < 0 else 1 for n in Bs] )
    ic(len(Bs))
    test_inst = build_instructions(Bs, Cs, As)
    #ics(test_inst)
    test_parsed = parse_data(test_inst)
    #ics(test_parsed)
    #print(get_comp_repr(instructions, test_parsed))
    ic(parse_data(test_inst) == parsed)

    opt = Optimize()
    all_ws = [Int(f"w{n}") for n in range(14)]
    bot_constraints = [ ]
    in_range_cnt = Int("in_range_cnt")
    buildup = 0

    for w in all_ws:
        opt.add(w >= 1)
        opt.add(w <= 9)
        buildup = buildup * 10 + w

    stack = []

    for n, a, b, c, w in zip(count(), As, Bs, Cs, all_ws):
        if a == 1:
            stack.append(w + c)
        else:
            past_z = stack.pop()
            #equations.append(sp.Eq(w, b + w_old + c_old))
            opt.add(w == b + past_z)

    input_number = Int("input")
    opt.add(input_number == buildup)
    return opt, input_number


# %%
def part1(inp):
    parsed = parse_data(inp)
    opt, input_number = process(parsed)
    opt.maximize(input_number)
    ics(opt.check())
    assert opt.check() == sat
    model = opt.model()
    ics(model)
    result = model[input_number].as_long()
    print_result(result)


# %%
def part2(inp):
    parsed = parse_data(inp)
    opt, input_number = process(parsed)
    opt.minimize(input_number)
    ics(opt.check())
    assert opt.check() == sat
    model = opt.model()
    ics(model)
    result = model[input_number].as_long()
    print_result(result)


# %% [markdown]
# # Sample data processing

# %%
insert_sample_functions(False, globals())
real_inp = get_aocd_data()
part1(real_inp)
part2(real_inp)

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)
part2(real_inp)


# %% [markdown]
# # Others' solutions

# %%
# https://cutonbuminband.github.io/AOC/qmd/2021.html#day-24-arithmetic-logic-unit
def solve1():
    chunks = [[y.split() for y in x.split("\n") if y] for x in real_inp.split("inp w\n")][1:]
    indices = [3, 4, 14]
    table = [[chunk[index][2] for index in indices] for chunk in chunks]
    triples = [[int(n) for n in row] for row in table]

    def run(triple, z, w):
        a, b, c = triple

        if w == z % 26 + b:
            return z // a

        return (z // a) * 26 + w + c

    zs = [[0, 0]]

    for triple in triples:
        new_zs = []
        a, b, c = triple

        for prefix, z in zs:
            if a == 26:
                w = z % 26 + b
                ws = [w] if 1 <= w < 10 else []
            else:
                ws = range(1, 10)
            new_zs += [(10 * prefix + w, run(triple, z, w)) for w in ws]

        zs = new_zs

    print(max(x[0] for x in zs))
    print(min(x[0] for x in zs))
#solve1()

# %%
# https://www.reddit.com/r/adventofcode/comments/rnejv5/comment/hpsjfis/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
instr, stack = real_inp.splitlines(), []

p, q = 99999999999999, 11111111111111

for i in range(14):
    a = int(instr[18*i+5].split()[-1])
    b = int(instr[18*i+15].split()[-1])

    if a > 0: stack+=[(i, b)]; continue
    j, b = stack.pop()

    p -= abs((a+b)*10**(13-[i,j][a>-b]))
    q += abs((a+b)*10**(13-[i,j][a<-b]))

print(p, q)


# %% [markdown]
# # analyze_instructions

# %%
def analyze_instructions(instructions, ip_idx=-1):
    def pre_label_reduced(lines):
        lines = list(lines)

        for ip, inst in enumerate(lines):
            match inst:
                case "div", dst, "1":
                    lines[ip] = ["nop"]
                case "mul", dst, "0":
                    lines[ip][0] = "set"
                case "add", dst, src:
                    prev = lines[ip-1]
                    #ic(inst, prev)
                    if prev == ["set", dst, "0"]:
                    #if prev[0] == "set" and lines[-1][1] == dst:
                        #ic("   yes")
                        lines[ip][0] = "set"
                        lines[ip-1] = ["nop"]

        return lines

    def get_repr(labeled_lines):
        return "\n".join(f"[{ip:2}] {' '.join(map(str, inst))}" for ip, inst in enumerate(labeled_lines))

    def get_repr_no_ip(labeled_lines):
        return "\n".join(f"{' '.join(map(str, inst))}" for ip, inst in enumerate(labeled_lines))

    def get_comp_repr(instructions, labeled_lines):
        return "\n".join(f"{' '.join(map(str, old)):20}  {' '.join(map(str, inst)):15}" for old, inst in zip(instructions, labeled_lines))

    def explained(labeled_lines):
        def build_op(ip, op, dst, src):
            prev = prev_inst[ip-1]

            if prev[0] == "set" and prev[1] == dst:
                labeled_lines[ip-1] = ["nop"]
                return f"{dst} = {prev[2]} {op} {src}"

            return f"{dst} {op}= {src}"

        prev_inst = labeled_lines
        labeled_lines = list(labeled_lines)
        prev = None

        for ip, inst in enumerate(labeled_lines):
            new_inst = None

            match inst:
                case "inp", dst:
                    new_inst = f"{dst} = input"

                case "set", dst, src:
                    new_inst = f"{dst} = {src}"

                case "mul", dst, src:
                    new_inst = build_op(ip, "*", dst, src)

                case "div", dst, src:
                    new_inst = build_op(ip, "//", dst, src)

                case "mod", dst, src:
                    new_inst = build_op(ip, "%", dst, src)

                case "add", dst, src:
                    new_inst = build_op(ip, "+", dst, src)

                case "eql", dst, "0":
                    if prev[:2] == ["eql", dst]:
                        new_inst = f"{dst} = {dst} == {prev[2]}"
                        labeled_lines[ip-1] = ["nop"]

            if new_inst:
                labeled_lines[ip] = [ new_inst]

            prev = inst

        return remove_nops(labeled_lines)

    def remove_nops(labeled_lines):
        return [inst for inst in labeled_lines if inst[0] != "nop"]

#ic(ip_idx, instructions)
    lines = pre_label_reduced(instructions)
    if 0:
        print("Pre-label reduced:")
        print("\n".join(" ".join(map(str, line)) for line in lines))
    if 0:
        labeled_lines = reduced(labeled_lines)
        print("Reduced:")
        print(get_repr(labeled_lines))
    if 0:
        print(get_comp_repr(instructions, labeled_lines))
    lines = remove_nops(lines)
    if 0:
        print("De-nopped:")
        print(get_repr_no_ip(lines))
#    print("explained:")
#    print(get_comp_repr(instructions, explained(labeled_lines)))
    #print(get_repr(lines))
    print(get_repr_no_ip(explained(lines)))

#analyze_instructions(parse_data(real_inp))
