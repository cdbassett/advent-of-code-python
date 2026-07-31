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

from icecream import ic

# %autoreload explicit
# import and reload these automatically,
# %aimport aoc_utils, Utilities, iter_utils, seq_extensions, func_utils, aoc_2019_intcode, pathfinding_redblob
from utils.aoc_utils import * # this includes adding c:\ut to sys.path
from utils.utilities import *
from utils.iter_utils import *
import utils.seq_extensions as seq_extensions # when running standalone, apparently need this import explicitly in main module
import utils.pathfinding_redblob
from aoc_2019_intcode import process_intcodes, parse_intcodes, send_and_receive_intcode_string, retrieve_state_id, IntCodeState


# %% [markdown]
# # Parse

# %%
def parse_data(inp):
    return parse_intcodes(inp)


# %% [markdown]
# # Process

# %%
def part1(inp):
    parsed = parse_data(inp)
    result = process(parsed)
    print_result(result)


# %%
def process_room(s, x, y, mem_state):
    title, doors, items, is_last = "", [], [], False
    line_chunks = seq(s.split("\n")).map(lambda l: l[2:] if l.startswith("- ") else l).split()
    #ic(line_chunks)
    
    for chunk in line_chunks:
        if not title and chunk[0].startswith("=="):
            title = chunk[0].strip("= ")
        elif chunk[0].startswith("Doors here"):
            doors = chunk[1:]
            
            if "ejected" in s:
                is_last = True
                break
        elif chunk[0].startswith("Items here"):
            items = [item for item in chunk[1:] if item not in skip_items]
                        
    #ic(doors, items)
    return Room(x, y, title, doors, items, False, is_last, mem_state)
    #return doors, items

def process_inv(generator):
    s = send_and_receive_intcode_string(generator, "inv\n")
    line_chunks = seq(s.split("\n")).map(lambda l: l[2:] if l.startswith("- ") else l).split()
    
    for chunk in line_chunks:
        if chunk[0].startswith("Items in your inventory"):
            return chunk[1:]

    return []

#Location = namedtuple("Location", "x,y,doors,state")
Room = namedtuple("Room", "x,y,title,doors,items,is_check,is_last,state")
skip_items = set("escape pod,infinite loop".split(","))

class ShipGraph(pathfinding_redblob.Graph):
    def __init__(self, generator, start_room):
        self.generator = generator
        self.rooms = { (0,0): start_room }
        self.check_room = None
        self.last_room = None
        self.edges = defaultdict(set)
        self.rooms_with_items = set()

    def next_room(self, from_room, x, y, cmd):
        self.generator.send(from_room.state)
        #ic(cmd)
        s = send_and_receive_intcode_string(self.generator, cmd+"\n")
        mem_state = self.generator.send(retrieve_state)
        room = process_room(s, x, y, mem_state)

        if 0:
            for item in room.items:
                send_and_receive_intcode_string(self.generator, "take " + item + "\n")

        if room.items:
            self.rooms_with_items.add((x, y))
            
        return room

    def get_room_info(self, id, from_room, cmd):
        room_info = self.rooms.get(id)

        if not room_info:
            room_info = self.rooms[id] = self.next_room(from_room, id[0], id[1], cmd)

            if room_info.is_last:
                from_room = from_room._replace(is_check=True)
                from_id = from_room.x, from_room.y
                self.check_room = self.rooms[from_id] = from_room
                self.last_room = room_info
                            
        return room_info
    
    def neighbors(self, id, came_from):
        #ic("neighbors", id)
        try:
            room_info = self.rooms[id]
        except KeyError as e:
            ic(id, came_from, self.rooms)
            raise
        neighbors = [add_tuple(id, compass_full_movements[door]) for door in room_info.doors]
        #ic(id, neighbors)
        # preload rooms for neighbors
        rooms = [self.get_room_info(neighbor, room_info, door) for door, neighbor in zip(room_info.doors, neighbors)]

        if 0:
            for neighbor in neighbors:
                self.edges[id].add(neighbor)
                self.edges[neighbor].add(id)
            
        return neighbors


def map_it(parsed):
    generator = process_intcodes(parsed)
    s = send_and_receive_intcode_string(generator)
    mem_state = generator.send(retrieve_state)
    start = 0, 0
    start_room = process_room(s, 0, 0, mem_state)
    graph = ShipGraph(generator, start_room)
    ic(start)
    came_from, current = pathfinding_redblob.breadth_first_search(graph, start, None) # no goal, map it all
    #ic(came_from)
    short_rooms = sorted(room._replace(state=None) for room in graph.rooms.values())
    ic(short_rooms)

    xs, ys = xs_and_ys(came_from.keys())
    #print(get_vis_map_multiline_str(xs, ys, special_chars=[("G", 0, 0), ("D", W-1, 0), ("O", empty_node.x, empty_node.y)]))
    print(get_vis_map_multiline_str(xs, ys, special_chars=[("S", 0, 0),("C", graph.check_room.x, graph.check_room.y),("L", graph.last_room.x, graph.last_room.y),] + [(str(len(room.items)), room.x, room.y) for room in short_rooms if room.items]))
    #print(get_edge_grid_map_multiline_str(graph.edges))
    ic(graph.rooms_with_items)

    check = graph.check_room.x, graph.check_room.y
    last = graph.last_room.x, graph.last_room.y
    master_path = [start]
    rooms_with_items = list(graph.rooms_with_items)
    rooms_with_items = seq(rooms_with_items).map(partial(distance, last)).zip(rooms_with_items).sorted(reverse=True)
    ic(rooms_with_items)
    rooms_with_items = rooms_with_items.map(itemgetter(1)).list()
    
    # we're not worrying about optimal paths, just one that covers all 
    traverse_rooms = [start] + rooms_with_items + [check]
    ic(traverse_rooms)
    
    for from_pos, to_pos in pairwise(traverse_rooms):
        #ic(from_pos, to_pos)
        came_from, current = pathfinding_redblob.breadth_first_search(graph, from_pos, to_pos)
        #ic(current, came_from)
        path = pathfinding_redblob.reconstruct_path(came_from, from_pos, to_pos)
        #ic(path)
        master_path.extend(path[1:]) # skip starting node
        
    ic(master_path)
    reverse_compass = dict((a, b) for b, a in compass_full_movements.items())

    generator = process_intcodes(parsed)
    s = send_and_receive_intcode_string(generator)
    held_items = set()
    
    for from_pos, to_pos in pairwise(master_path):
        cmd = reverse_compass[subtract_tuple(to_pos, from_pos)] + "\n"
        room = graph.rooms[to_pos]
        send_and_receive_intcode_string(generator, cmd)

        for item in room.items:
            send_and_receive_intcode_string(generator, "take " + item + "\n")
            held_items.add(item)

    held_items = list(held_items)    
    ic(held_items)
    s = send_and_receive_intcode_string(generator, "inv\n")
    print(s)                
    mem_state = generator.send(retrieve_state)
    cmd = reverse_compass[subtract_tuple(last, check)] + "\n"
    s = send_and_receive_intcode_string(generator, cmd)
    print(s)                

    for n, combo in enumerate(powerset(held_items)):
        ic(n, combo)
        generator.send(mem_state)

        for item in combo:
            send_and_receive_intcode_string(generator, f"drop {item}\n")
        ic(process_inv(generator))    
        #s = send_and_receive_intcode_string(generator, "inv\n")
        #print(s)                
        s = send_and_receive_intcode_string(generator, cmd)
        
        if "ejected" not in s:
            print(s)
            break

        msg = seq(s.split("\n")).find(lambda l: l.startswith("A loud,"))
        msg = msg.split('"')[1]
        print(msg)
        #A loud, robotic voice says "Alert! Droids on this ship are lighter than the detected value!" and you are ejected back to the checkpoint.
        #if n % 10 == 0:
        #    print(s)
        
            
    print(s)

                              
def process(parsed):
    if 1:
        map_it(parsed)
        return
    #ics(parsed)
    generator = process_intcodes(parsed)
    input_line = ""
    ic(len(parsed))
    last = 0, 0, dict(enumerate(parsed))

    while True:
        s = send_and_receive_intcode_string(generator, input_line)
        print(s)
        #doors, items = process_room(s)
        mem_state = generator.send(retrieve_state)
        room = process_room(s, 0, 0, None)
            #line_chunks  = list(split_iterable(lines))
        ic(room)

        if 0:
            mem_state = generator.send(retrieve_state)
            ip, relative, mem = mem_state
            ic(ip, relative, len(mem))
            ic(mem_state)
            ic(ip, last[0])
            diff = dict_diff(dict(mem_state[2]), dict(last[2]))
            diff = seq(diff[0]).outer_join(diff[1]).sorted().list()
            ic(diff)
            last = mem_state
        input_line = input().strip() + "\n"

    return None


# %% [markdown]
# # Actual data

# %% editable=true slideshow={"slide_type": ""}
real_inp = get_aocd_data()
insert_sample_functions(True, globals())
part1(real_inp)


# %% [markdown]
# # Others' solutions

# %%
def solve1():
    import utils
    from intcode import IntCodeProgram
    load = utils.year_load(2019)

    program = IntCodeProgram(load(25, "np"), inputs=[])
    
    def run():
        for char in program.run():
            if program.state != 1:
                print(chr(char), end="")
            else:
                s = input().strip()
                program.inputs += [ord(x) for x in s + "\n"]
    run()                
solve1()                

# %%
