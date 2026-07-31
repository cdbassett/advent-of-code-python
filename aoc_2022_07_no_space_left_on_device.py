from functools import *
from collections import *
from itertools import *
from math import *
from dataclasses import dataclass, field
from builtins import pow
import pyperclip
from icecream import ic

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

dir_entry = namedtuple("dir_entry", "name,size")
file_entry = namedtuple("file_entry", "name,size")

@dataclass
class DirEntry:
    name: str
    parent: object = None
    size: int = 0
    dirs: list = field(default_factory=list)
    files: list = field(default_factory=list)

@dataclass
class FileEntry:
    name: str
    size: int = 0



def split_commands(i):
    return (list(c) for match, c in itertools.groupby(i, lambda p: p[0] == "$"))

def join(parts):
#    return "/".join(p for p in parts if p)
    return "/".join(parts)

def split(path):
    return list(filter(None, path.split("/")))


def run(inp, is_real):
    insert_sample_functions(is_real, globals())
    inp = inp.strip('\n').split('\n')
    commands = []

    for cmd in inp:
        if cmd.startswith("$"):
            last = [ cmd ]
            commands.append(last)
        else:
            last.append(cmd)

    print_list("commands", commands)

    directories = defaultdict(list)
    cur_path = ""
    cur_node = root_node = DirEntry("/")

    for cmd in commands:
        run = cmd[0].split()
        output = cmd[1:]
        exe = run[1]
#        ics(run, exe)

        if exe == "ls":
            for files_and_dirs in output:
                parts = files_and_dirs.split()

                if parts[0] == "dir":
                    cur_node.dirs.append(DirEntry(parts[1], cur_node))
                else:
                    cur_node.files.append(FileEntry(parts[1], int(parts[0])))
        elif exe == "cd":
            d = run[2]

            if d == "/":
                cur_node = root_node
            elif d == "..":
                cur_node = cur_node.parent
            else:
                cur_node = first(de for de in cur_node.dirs if de.name == d)
#
#                ics(split(cur_path))
#                ics(split(cur_path) + [d])
#                cur_path = join(split(cur_path) + [d])

#            ics(cur_path)




    def traverse_size(dir_node):
        node_size = 0

        for de in dir_node.dirs:
            node_size += traverse_size(de)

        for fe in dir_node.files:
            node_size += fe.size

        dir_node.size = node_size
        return node_size

    def traverse_cond(dir_node, cond, build=[]):
        if cond(dir_node):
            build.append(dir_node)

        for de in dir_node.dirs:
            traverse_cond(de, cond, build)

    root_size = traverse_size(root_node)
    ics(root_node)
#    ics(size)


    def part1():
        dir_list = []
        traverse_cond(root_node, lambda de: de.size <= 100000, dir_list)
        result = sum(de.size for de in dir_list)
        print_result(result)

    def part2():
        dir_list = []
        free_space = 70000000 - root_size
        needed_space = 30000000 - free_space
        traverse_cond(root_node, lambda de: de.size >= needed_space, dir_list)

#        dir_list = sorted(dir_list, key = lambda de: de.size)
#        ics(dir_list)
#        result = dir_list[-1].size

        name_and_size = sorted((de.size, de.name) for de in dir_list)
        ics(name_and_size)
        result = name_and_size[0][0]
        print_result(result)


    part1()
    part2()

def main():
    example = get_aocd_example()
    samp_inps = split_example(example)

    for n, samp_inp in enumerate(samp_inps, 1):
        print(f"{Fore.BLUE}{Style.BRIGHT}Sample {n}:{Style.RESET_ALL}")
        run(samp_inp, False)

    if 1:
        print(f"{Fore.BLUE}{Style.BRIGHT}Actual:{Style.RESET_ALL}")
        real_inp = get_aocd_data()
        run(real_inp, True)

main()
