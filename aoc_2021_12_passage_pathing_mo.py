import marimo

__generated_with = "0.13.13"
app = marimo.App(width="medium")


@app.cell
def _():
    from dataclasses import dataclass, field
    import traceback
    import collections
    from collections import defaultdict

    import marimo as mo
    from icecream import ic
    from functional import seq
    from colorama import Fore, Style

    import seq_extensions
    import aoc_utils
    from aoc_utils import get_aocd_example, split_example, insert_sample_functions, get_aocd_data
    import timer_utils
    #aoc_utils.aocd_filename = __file__
    return (
        collections,
        dataclass,
        defaultdict,
        field,
        get_aocd_data,
        get_aocd_example,
        insert_sample_functions,
        seq,
        split_example,
    )


@app.cell
def _(get_aocd_example):
    example = get_aocd_example()
    #example
    return (example,)


@app.cell
def _(example, split_example):
    sample_data1s = split_example(example)
    sample_data2s = sample_data1s
    return sample_data1s, sample_data2s


@app.cell
def _(dataclass, field):
    @dataclass
    class Node:
        name: str
        neighbors: list = field(default_factory=list)

        def add_neighbor(self, node):
            self.neighbors.append(node)
            node.neighbors.append(self)

        def remove_neighbor(self, node):
            if node in self.neighbors:
                self.neighbors.remove(node)
    return (Node,)


@app.cell
def _(Node, collections):
        # we subclass this for __missing__ functionality, which is called when key not in dict upon
        # __getitem__() call (called by  dict[key] reference)
        # normal defaultdict behavior is to return default value and add to dict
        # we want to create a node and initialize it with key
    class DefaultDictNode(collections.defaultdict):
        def __missing__(self, key):
            node = Node(key)
            self[key] = node
            return node
    return (DefaultDictNode,)


@app.cell
def _(seq):
    def parse_line(line):
        return line.split("-")

    def parse_data(inp):
        return seq(inp.strip().split("\n")).map(parse_line).list()
    return (parse_data,)


@app.cell
def _():
    def simple_nodes(nodes):
    #        return [[(p.x, p.y, p.val) for p in line_points] for line_points in points]
    #        return [[p.val for p in line_points] for line_points in points]
        return [f"{node.name}: {','.join(n.name for n in node.neighbors)}" for node in nodes]

    def get_path_desc(path):
    #        return "->".join(node.name for node in path)
        return ",".join(node.name for node in path)

    #ics(simple_nodes())
    return


@app.cell
def _(DefaultDictNode, defaultdict):
    def setup(parsed):
        nodes = DefaultDictNode() # name -> node

        for source, target in parsed:
            nodes[source].add_neighbor(nodes[target])

        all_nodes = list(nodes.values())
        start_node = nodes["start"]
        end_node = nodes["end"]

            # don't bother with connections back to start
        for node in all_nodes:
            node.remove_neighbor(start_node)
    
        connections = defaultdict(set)

        for a, b in parsed:
            connections[a].add(b)
            connections[b].add(a)
        
        return all_nodes, start_node, end_node, connections
    return (setup,)


@app.cell
def _(parse_data, print_result, setup):
    def traverse_path1(node, end_node, paths, path, visited):
    #        ics(node.name)

        if node == end_node:
            path.append(node)
    #            ics(get_path_desc(path))
            paths.append(path)
            return

        if node.name.islower():
            if node.name in visited:
                return
            else:
                visited.add(node.name)

        path.append(node)

        for n, neighbor in enumerate(node.neighbors):
    #            ics(node.name, n)
            traverse_path1(neighbor, end_node, paths, path[:], set(visited))


    def process(parsed):
        all_nodes, start_node, end_node, connections = setup(parsed)
        paths = []
        traverse_path1(start_node, end_node, paths, [], set())
    #    path_desc = [get_path_desc(path) for path in paths]
    #        ics(path_desc)
    #        ics(simple_nodes(paths[0]))
        return len(paths)

    def part1(inp):
        #for frame in traceback.extract_stack():
            #print(frame[0])
        parsed = parse_data(inp)
        result = process(parsed)
        print_result(result)
    return (part1,)


@app.cell
def _(parse_data, print_result, setup):
    def traverse_path2(node, end_node, paths, path, visited, small_cave=None):
    #        ics(node.name)

        if node == end_node:
            path.append(node)
    #            ics(get_path_desc(path))
            paths.append(path)
            return

        if node.name.islower():
            if node.name in visited:
                if small_cave:
                    return
                else:
                    small_cave = node
            else:
                visited.add(node.name)

        path.append(node)

        for n, neighbor in enumerate(node.neighbors):
    #            ics(node.name, n)
            traverse_path2(neighbor, end_node, paths, path[:], set(visited), small_cave)

    def process2(parsed):
        all_nodes, start_node, end_node, connections = setup(parsed)
        paths = []
        traverse_path2(start_node, end_node, paths, [], set())
    #    path_desc = [get_path_desc(path) for path in paths]
    #        ics(path_desc)
    #        ics(simple_nodes(paths[0]))
        return len(paths)

    def part2(inp):
    #    for frame in traceback.extract_stack():
    #        print(frame[0])
    
        parsed = parse_data(inp)
        result = process2(parsed)
        print_result(result)
    return (part2,)


@app.cell
def _(
    insert_sample_functions,
    part1,
    part2,
    print_preface_notebook,
    sample_data1s,
    sample_data2s,
):
    insert_sample_functions(False, globals())
    #print(f"{Fore.GREEN}{Style.BRIGHT}Sample results:{Style.RESET_ALL}")
    print_preface_notebook()

    for sample_data1 in sample_data1s:
        part1(sample_data1)
    
    for sample_data2 in sample_data2s:
        part2(sample_data2)
    return


@app.cell
def _(
    get_aocd_data,
    insert_sample_functions,
    part1,
    part2,
    print_preface_notebook,
):
    real_inp = get_aocd_data()
    insert_sample_functions(True, globals())
    print_preface_notebook()
    #print(f"{Fore.GREEN}{Style.BRIGHT}Real results:{Style.RESET_ALL}")
    part1(real_inp)
    part2(real_inp)

    return


if __name__ == "__main__":
    app.run()
