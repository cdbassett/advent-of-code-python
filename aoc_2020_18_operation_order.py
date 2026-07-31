from functools import *
from collections import *
#from sympy import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import operator
from timer_utils import timefunction

from colorama import Fore, Style
from functional import seq # https://github.com/EntilZha/PyFunctional
import iteration_utilities as it_ut # https://pypi.org/project/iteration-utilities/
from icecream import ic

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

# fourFn.py
#
# Demonstration of the pyparsing module, implementing a simple 4-function expression parser,
# with support for scientific notation, and symbols for e and pi.
# Extended to add exponentiation and simple built-in functions.
# Extended test cases, simplified pushFirst method.
# Removed unnecessary expr.suppress() call (thanks Nathaniel Peterson!), and added Group
# Changed fnumber to use a Regex, which is now the preferred method
# Reformatted to latest pypyparsing features, support multiple and variable args to functions
#
# Copyright 2003-2019 by Paul McGuire
#
from pyparsing import (
    Literal,
    Word,
    Group,
    Forward,
    alphas,
    alphanums,
    Regex,
    ParseException,
    CaselessKeyword,
    Suppress,
    delimitedList,
)
import operator

exprStack = []


def push_first(toks):
    exprStack.append(toks[0])


def push_unary_minus(toks):
    for t in toks:
        if t == "-":
            exprStack.append("unary -")
        else:
            break


bnfs = [None] * 3


def BNF(part):
    """
    expop   :: '^'
    multop  :: '*' | '/'
    addop   :: '+' | '-'
    integer :: ['+' | '-'] '0'..'9'+
    atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
    factor  :: atom [ expop factor ]*
    term    :: factor [ multop factor ]*
    expr    :: term [ addop term ]*
    """
    global bnfs

    if not bnfs[part]:
        # fnumber = Combine(Word("+-"+nums, nums) +
        #                    Optional("." + Optional(Word(nums))) +
        #                    Optional(e + Word("+-"+nums, nums)))
        # or use provided pyparsing_common.number, but convert back to str:
        # fnumber = ppc.number().addParseAction(lambda t: str(t[0]))
        fnumber = Regex(r"[+-]?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?")
        ident = Word(alphas, alphanums + "_$")

        plus, minus, mult, div = map(Literal, "+-*/")
        lpar, rpar = map(Suppress, "()")

        if part == 1:
            addop = plus | minus | mult | div
        else:
            addop = plus | minus

        multop = mult | div
        expop = Literal("^")

        expr = Forward()
        expr_list = delimitedList(Group(expr))
        atom = (
            addop[...]
            + (
                (fnumber | ident).setParseAction(push_first)
                | Group(lpar + expr + rpar)
            )
        ).setParseAction(push_unary_minus)

        # by defining exponentiation as "atom [ ^ factor ]..." instead of "atom [ ^ atom ]...", we get right-to-left
        # exponents, instead of left-to-right that is, 2^3^2 = 2^(3^2), not (2^3)^2.
        factor = Forward()
        factor <<= atom + (expop + factor).setParseAction(push_first)[...]

        if 0:
            term = factor + (multop + factor).setParseAction(push_first)[...]
            expr <<= term + (addop + term).setParseAction(push_first)[...]
        elif part == 2:
            term = factor + (addop + factor).setParseAction(push_first)[...]
            expr <<= term + (multop + term).setParseAction(push_first)[...]
        elif part == 1:
            expr <<= factor + (addop + factor).setParseAction(push_first)[...]

        bnfs[part] = expr
    return bnfs[part]


# map operator symbols to corresponding arithmetic operations
epsilon = 1e-12
opn = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "^": operator.pow,
}


def evaluate_stack(s):
    op, num_args = s.pop(), 0

    if isinstance(op, tuple):
        op, num_args = op

    if op == "unary -":
        return -evaluate_stack(s)

    if op in "+-*/^":
        # note: operands are pushed onto the stack in reverse order
        op2 = evaluate_stack(s)
        op1 = evaluate_stack(s)
        return opn[op](op1, op2)
    elif op[0].isalpha():
        raise Exception("invalid identifier '%s'" % op)
    else:
        # try to evaluate as int first, then as float if int fails
        try:
            return int(op)
        except ValueError:
            return float(op)



@timefunction
def run(inp1, inp2, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    def data_parse(inp):
#        lines = inp.strip().split('\n')
        lines = inp.strip("\n").split('\n')
        return lines



    def process(inp, part):
        exprStack[:] = []

        try:
            results = BNF(part).parseString(inp, parseAll=True)
            val = evaluate_stack(exprStack[:])
        except ParseException as pe:
            print(inp, "failed parse:", str(pe))
        except Exception as e:
            print(inp, "failed eval:", str(e), exprStack)
        else:
            ics(inp, val)
            return val



    @timefunction
    def part1(inp):
        lines = data_parse(inp)
        result = sum(process(line, 1) for line in lines)
#        result = process(inp.strip(), 1)
        print_result(result)


    @timefunction
    def part2(inp):
        lines = data_parse(inp)
        result = sum(process(line, 2) for line in lines)
        print_result(result)

    part1(inp1)
    part2(inp2)

def main():
    if 1:
        if samp_inps:
            for samp_inp in samp_inps:
                print(f"{Fore.GREEN}{Style.BRIGHT}Sample:{Style.RESET_ALL}")
                run(samp_inp, samp_inp, False)
        else:
            print(f"{Fore.BLUE}{Style.BRIGHT}Sample:{Style.RESET_ALL}")
#            print("Sample:")
            run(samp_inp1, samp_inp2, False)

    if 1:
        print(f"{Fore.YELLOW}{Style.BRIGHT}Actual:{Style.RESET_ALL}")
        real_inp = get_aocd_data()
        run(real_inp, real_inp, True)
#        aocd.submit(my_answer)




samp_inp1 = r"""
.#.
..#
###
"""

samp_inp2 = samp_inp1


short_samp = """
"""


samp_inps = [
    "1 + 2 * 3 + 4 * 5 + 6",
    "2 * 3 + (4 * 5)",
    "5 + (8 * 3 + 9 + 3 * 4 * 3)",
    "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))",
    "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2",
#    short_samp,
#    samp_inp,
    ]


main()

