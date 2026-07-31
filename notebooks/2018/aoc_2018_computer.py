from collections import *


from aoc_utils import * # this includes adding c:\ut to sys.path
from utilities import *
from iter_utils import *
import seq_extensions # when running standalone, apparently need this import explicitly in main module

def parse_line(line):
    #ic(line)
    return list(multimap(line.split(), identity, int, int, int))

def parse_instructions(inp):
    lines = inp.strip().split("\n")
    return string_to_integers(lines[0]), seq(lines[1:]).map(str.split).multimap(identity, int, int, int).list()
#    return seq(inp.strip().split("\n")).split().map(njoin).map(string_to_integers).list()


def build_instructions():
    bases = "add,mul,ban,bor,set,gt,eq".split(",")
    full_set = list(map(sjoin, product(("i", "r"), ("i", "r"))))
    return seq(product((base,), ("i", "r") if len(base) == 3 else full_set) for base in bases).level2_map(sjoin).flatten().list()

all_instructions = [inst for inst in build_instructions() if not inst.endswith("ii")]

#def

def handle_inst(inst, registers):
    #ic(inst, registers)
    opcode, a_val, b_val, c_val = inst
    base, a_code, b_code = opcode[:3], opcode[2], opcode[3]

    if base == "set":
        a = registers[a_val] if b_code == "r" else a_val
        registers[c_val] =  a # set is special, ignore b and uses a instead
    else:
        if base[:2] in ("gt", "eq"):
            base = opcode[:2]
            a = registers[a_val] if a_code == "r" else a_val
        else:
            a = registers[a_val]

        b = registers[b_val] if b_code == "r" else b_val

        #ic(base, a, b)

        match base:
            case "add":
                registers[c_val] =  a + b
            case "mul":
                registers[c_val] =  a * b
            case "ban":
                registers[c_val] =  a & b
            case "bor":
                registers[c_val] =  a | b
            case "gt":
                registers[c_val] =  int(a > b)
            case "eq":
                registers[c_val] =  int(a == b)
            case _:
                raise Exception(f"Unhandled instruction {inst}")

def run_instructions(instructions, registers):
    #ic(instructions, len(instructions))
    inst_len = len(instructions)
    ip = 0

    while ip < inst_len:
        inst = instructions[ip]
        #ic(ip, inst, registers)
        handle_inst(inst, registers)
        ip += 1

def run_instructions_with_ip(instructions, ip_idx, registers):
    #ic(instructions, len(instructions))
    inst_len = len(instructions)
    ip = 0

    while 0 <= ip < inst_len:
        registers[ip_idx] = ip
        inst = instructions[ip]
        #ic(ip, inst, registers)
        handle_inst(inst, registers)
        ip = registers[ip_idx] + 1

    registers[ip_idx] = ip

def run_instructions_with_ip_gen(instructions, ip_idx, registers):
    #ic(instructions, len(instructions))
    inst_len = len(instructions)
    ip = 0

    while 0 <= ip < inst_len:
        registers[ip_idx] = ip
        inst = instructions[ip]
        #ic(ip, inst, registers)
        handle_inst(inst, registers)

        yield registers
        ip = registers[ip_idx] + 1



reg_names = string.ascii_uppercase

def analyze_instructions(instructions, ip_idx=-1):
    def single_reg(a, b, c):
        if a == c:
            return b
        elif b == c:
            return a

    def pre_label_reduced(lines):
        lines = list(lines)

        for ip, inst in enumerate(lines):
#            match inst:
                pass

        return lines

    # converts to regsiter strings and base instruction names
    def labeled(instructions):
        def set_label(new_ip):
            new_label = f"label{new_ip}"
            labeled_lines[new_ip][0] = new_label
            return new_label

        def abs_jump(ip, new_ip):
            new_label = set_label(new_ip)
#            ic(new_ip, label)
            labeled_lines[ip][1] = [f"jmp {new_label}"]

        def get_desc(scode, val):
            return reg_names[val] if scode == "r" else val

        nonlocal ip_idx
        assert ip_idx >= 0
#        labeled_lines = [[str(ip), inst] for ip, inst in enumerate(instructions)] + [["", ["nop"]]] # add extra for out of bounds jumps
        labeled_lines = [["", inst] for ip, inst in enumerate(instructions)] + [["", ["nop"]]] # add extra for out of bounds jumps

        for ip, (label, inst) in enumerate(labeled_lines):
            match inst:
                case opcode, a_val, b_val, c_val:
#                    ic(ip, inst, ip_idx)

                    if c_val == ip_idx:
                        new_inst = None

                        match inst:
#                        match opcode:
                            case "addr", ar, br, ip_idx:
                                if (sr := single_reg(ar, br, ip_idx)) is not None:
                                    new_label = set_label(ip + 1)
                                    new_inst = f"jmp {new_label} + {reg_names[sr]}"
                                else:
                                    new_inst = f"jmp {reg_names[ar]} + {reg_names[br]} + 1"
                            case "addi", ar, b, ip_idx:
                                if ar == ip_idx:
                                    abs_jump(ip, ip + b + 1)
                                else:
                                    new_inst = f"jmp {reg_names[ar]} + {b + 1}"
                            case "setr", ar, _, ip_idx:
                                new_inst = f"jmp {reg_names[ar]} + 1"
                            case "seti", a, _, ip_idx:
                                abs_jump(ip, a + 1)

                        if new_inst:
                            labeled_lines[ip][1] = [new_inst]

                    else:
#                    opcode, a_val, b_val, c_val = inst
                        base, a_code, b_code = opcode[:3], opcode[2], opcode[3]
                        new_inst = [base]

                        if base == "set":
                            new_inst.append(get_desc(b_code, a_val))
                        else:
                            if base[:2] in ("gt", "eq"):
                                base = opcode[:2]
                                new_inst[0] = base
                                a = get_desc(a_code, a_val)
                            else:
                                a = reg_names[a_val]

                            b = get_desc(b_code, b_val)
                            new_inst.extend((a, b))

                        new_inst.append(reg_names[c_val])
                        labeled_lines[ip][1] = new_inst


        return labeled_lines

    def get_repr(labeled_lines):
        return "\n".join(f"[{ip:2}] {label+':' if label else '' :9}{' '.join(map(str, inst))}" for ip, (label, inst) in enumerate(labeled_lines))

    def get_repr_no_ip(labeled_lines):
        return "\n".join(f"{label+':' if label else '' :9}{' '.join(map(str, inst))}" for ip, (label, inst) in enumerate(labeled_lines))

    def get_repr_no_ip_sep_labels(labeled_lines):
        return "\n".join(f"{p1+':' if p1 else '' :9}{' '.join(map(str, p2))}" for (label, inst) in labeled_lines for p1, p2 in ([label, ""], ["", inst]) if p1 or p2)

    def get_comp_repr(instructions, labeled_lines):
        return "\n".join(f"{label:9}{' '.join(map(str, old)):20}  {' '.join(map(str, inst)):15}" for old, (label, inst) in zip(instructions, labeled_lines))

    def reduced(labeled_lines):
        labeled_lines = list(labeled_lines)

        for ip, (label, inst) in enumerate(labeled_lines):
#            match inst:
                pass


        return labeled_lines

    def explained(labeled_lines):
        labeled_lines = list(labeled_lines)

        for ip, (label, inst) in enumerate(labeled_lines):
            new_inst = None
            match inst:
                case "set", a, c:
                    new_inst = f"{c} = {a}"

                case "add", a, b, c:
                    if (s := single_reg(a, b, c)):
                        new_inst = f"{c} += {s}"
                    else:
                        new_inst = f"{c} = {a} + {b}"

                case "mul", a, b, c:
                    if (s := single_reg(a, b, c)):
                        new_inst = f"{c} *= {s}"
                    else:
                        new_inst = f"{c} = {a} * {b}"

                case "ban", a, b, c:
                    if (s := single_reg(a, b, c)):
                        new_inst = f"{c} &= {s}"
                    else:
                        new_inst = f"{c} = {a} & {b}"

                case "bor", a, b, c:
                    if (s := single_reg(a, b, c)):
                        new_inst = f"{c} |= {s}"
                    else:
                        new_inst = f"{c} = {a} | {b}"
                case "gt", a, b, c:
                    new_inst = f"{c} = {a} > {b}"
                case "eq", a, b, c:
                    new_inst = f"{c} = {a} == {b}"

            if new_inst:
                labeled_lines[ip][1] = [ new_inst]


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

#ic(ip_idx, instructions)
    lines = pre_label_reduced(instructions)
    if 0:
        print("Pre-label reduced:")
        print("\n".join(" ".join(map(str, line)) for line in lines))
    labeled_lines = labeled(lines)
    #ic(labeled_lines)
    if 0:
        print("Labeled:")
        print(get_repr(labeled_lines))
    if 0:
        labeled_lines = reduced(labeled_lines)
        print("Reduced:")
        print(get_repr(labeled_lines))
    if 0:
        print(get_comp_repr(instructions, labeled_lines))
    labeled_lines = remove_nops(labeled_lines)
    if 0:
        print("De-nopped:")
        print(get_repr_no_ip(labeled_lines))
#    print("explained:")
#    print(get_comp_repr(instructions, explained(labeled_lines)))
    print(get_repr(explained(labeled_lines)))
    print(get_repr_no_ip_sep_labels(explained(labeled_lines)))




