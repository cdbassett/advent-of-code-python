from functools import *

from iteration_utilities import return_identity as identity
import iteration_utilities

compose = iteration_utilities.chained

# use these for simple mapping
def first_arg(*args):
    return args[0]

def second_arg(*args):
    ic(args)
    return args[1]

def first_elem(args):
    return args[0]

def second_elem(args):
    return args[1]

def third_elem(args):
    return args[2]

def fourth_elem(args):
    return args[3]

def last_elem(args):
    return args[-1]

# examples:
#def foo(a, b, c, /, *, d):
#    print(f"A({a}) B({b}) C({c}) D({d})")
#
#f1 = bind(foo, 1, 2, 3, d=4)
#f1()
#f2 = bind(foo, 1, 2, d=4)
#f2(3)
#f3 = bind(foo, 1, ..., 3, d=4)
#f3(2)
#f4 = bind(foo, ..., 2, ..., d=4)
#f4(1, 3)
#f5 = bind(foo, ..., d=5)
#f5(1, 2, 3, d=4)
# from https://stackoverflow.com/questions/7811247/how-to-fill-specific-positional-arguments-with-partial-in-python/66274908#66274908
class bind(partial):
    """
    An improved version of partial which accepts Ellipsis (...) as a placeholder
    """
    def __call__(self, *args, **keywords):
        keywords = {**self.keywords, **keywords}
        iargs = iter(args)
        args = (next(iargs) if arg is ... else arg for arg in self.args)
        return self.func(*args, *iargs, **keywords)



# like partial but fills arguments on right side
# untested
def partial_right(func, /, *args, **keywords):
    def newfunc(*fargs, **fkeywords):
        newkeywords = {**keywords, **fkeywords}
        return func(*fargs, *args, **newkeywords)

    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc


# like partial but fills arguments on right side, from funcy
def rpartial(func, *args):
    return lambda *a: func(*(a + args))


# composite_function accepts N
# number of function as an
# argument and then compose them
# can just use iteration_utilities.chained
def composite_function(*func):
    def compose(f, g):
        return lambda x : f(g(x))

#    return functools.reduce(compose, reversed(func), lambda x : x)
    return reduce(compose, reversed(func)) # identity at end is to handle empty list of functions, which I don't anticipate ever doing


