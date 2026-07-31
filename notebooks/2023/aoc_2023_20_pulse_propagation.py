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
from utils.aoc_utils import *
if is_notebook():
    print(get_aoc_url())

# %% [markdown]
# # Imports

# %%
# %load_ext autoreload

# %%
from collections import *
import math
from dataclasses import dataclass,field

from icecream import ic

# %autoreload explicit
# import and reload these automatically
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module

# %% [markdown]
# # Sample Data

# %%
sample_data1 = """
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""
sample_data2 = sample_data1

# %%
if "example" not in dir() or not example:
    example = get_aocd_example()

# %%
sample_data1s = split_example(example)
sample_data1 = sample_data1s[0]
sample_data2 = sample_data1

# %%
print(sample_data1)

# %% [markdown]
# # Parse

# %%
Module = namedtuple("Module","name,outputs")

def parse_line(line):
    name, o = line.split(" -> ")
    return Module(name, o.split(", "))

def parse(inp):
    return seq(inp.strip().split("\n")).map(parse_line).list()


# %% [markdown]
# # Process

# %%
#LO = True
#HI = False
LO = False
HI = True

@dataclass
class BaseModule:
    module_name: str
    modules_by_name: dict
    outputs: list
    queue: list

    def pulse(self, mod_name, pulse):
        pass

    def add_input(self, mod_name):
        pass

@dataclass
class Broadcaster(BaseModule):
    def __str__(self):
        return "broadcaster"

    def pulse(self, mod_name, pulse):
        #ics(mod_name, pulse)
        for output in self.outputs:
            self.queue.append((output, self.module_name, pulse))

@dataclass
class Monitor(BaseModule):
    state: bool  = HI

    def __str__(self):
        return f"Monitor {self.module_name}: {self.state}"

    def pulse(self, mod_name, pulse):
        self.state = pulse

@dataclass
class FlipFlop(BaseModule):
    state: bool = LO

    def __str__(self):
        return f"FlipFlop {self.module_name}: {self.state}"

    def pulse(self, mod_name, pulse):
        #ics(mod_name, pulse)
        if pulse == LO:
            self.state = not self.state

            for output in self.outputs:
                self.queue.append((output, self.module_name, self.state))

@dataclass
class Conjunction (BaseModule):
    memory:dict = field(default_factory=dict) # default remembered value for inputs is LO (true)

    def __str__(self):
        return f"Conjunction {self.module_name}: {self.memory}"

    def add_input(self, mod_name):
        self.memory[mod_name] = LO

    def pulse(self, mod_name, pulse):
        #ics(mod_name, pulse)
        self.memory[mod_name] = pulse
        send = LO if all(k==HI for k in self.memory.values()) else HI # send low (true) if all remembered is high (false)

        for output in self.outputs:
            self.queue.append((output, self.module_name, send))

def setup(parsed):
    ics(parsed)
    #modules_by_name = dict((m.name, m) for m in parsed)
    modules_by_name = {}
    queue = deque()

    for m in parsed:
        match m.name:
            case "broadcaster":
                #module = Broadcaster(m.name, modules_by_name, m.outputs, queue)
                cls = Broadcaster
            case name if name.startswith("%"):
                cls = FlipFlop
            case name if name.startswith("&"):
                cls = Conjunction
            case _:
                raise Exception(f"unhandled line {mod}")

        m_name = m.name.lstrip("&%")
        modules_by_name[m_name] = cls(m_name, modules_by_name, m.outputs, queue)

    for mod_obj in modules_by_name.values():
        for output in mod_obj.outputs:
            other_module = modules_by_name.get(output)

            if other_module:
                other_module.add_input(mod_obj.module_name)


    for mod_obj in modules_by_name.values():
        print_sample(mod_obj)

    return queue, modules_by_name

def process_one_button_press(queue, modules_by_name):
    lo_pulses = 0
    hi_pulses = 0
    put, get = get_queue_functions_fifo(queue)
    went_high = set()

    #print_sample("---------------")
    put(("broadcaster", "button", LO))

    while queue:
        mod_name, from_name, pulse = get()

        if pulse == HI:
            hi_pulses += 1
            went_high.add(from_name)
        else:
            lo_pulses += 1
        #ics(mod_name, from_name, pulse)
        m = modules_by_name.get(mod_name)

        if m:
            m.pulse(from_name, pulse)

        if 0:
            p_name = "high" if pulse == HI else "low"
            print_sample(f"{from_name} -{p_name}-> {mod_name} ||| {m}")

    return hi_pulses, lo_pulses, went_high

def process(parsed):
    queue, modules_by_name = setup(parsed)
    all_lo_pulses = 0
    all_hi_pulses = 0

    for n in range(1000):
        hi_pulses, lo_pulses, _ = process_one_button_press(queue, modules_by_name)
        all_lo_pulses += lo_pulses
        all_hi_pulses += hi_pulses

    ic(all_hi_pulses, lo_pulses)
    return all_hi_pulses * all_lo_pulses


# %%
def part1(inp):
    parsed = parse(inp)
    result = process(parsed)
    print_result(result)


# %%
def part2(inp, monitor):
    parsed = parse(inp)
    queue, modules_by_name = setup(parsed)
    rx_input = seq(modules_by_name.values()).where(lambda m: "rx" in m.outputs).one()
    conj_inputs = seq(modules_by_name.values()).where(lambda m: rx_input.module_name in m.outputs).map(lambda m: m.module_name).list()
    conj_inputs_set = set(conj_inputs)
    ic(conj_inputs_set)

    #modules_by_name["rx"] = rx = Monitor("rx", modules_by_name, [], queue)
    #monitor = modules_by_name[monitor]
    #print(rx)
    prog_step = 1000000
    went_high_at = {}

    for button_presses in count(1):
        if not (button_presses % prog_step):
            print(button_presses)

        _, _, went_high = process_one_button_press(queue, modules_by_name)

        #ic(button_presses, conj_inputs_set, went_high)

        for mod_name in conj_inputs_set:
            if mod_name in went_high:
                went_high_at[mod_name] = button_presses
                ic(mod_name, button_presses)

        conj_inputs_set -= went_high

        if not conj_inputs_set:
            break

        #if monitor.state == LO:
        #    break

    ic(went_high_at)
    needed_presses = math.lcm(*went_high_at.values())
    print_result(needed_presses)


# %% [markdown]
# # Sample data

# %%
insert_sample_functions(False, globals())
part1(sample_data1)
#part2(sample_data2, "b")

# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
insert_sample_functions(True, globals())
real_inp = get_aocd_data()
part1(real_inp)
part2(real_inp, "rx")
