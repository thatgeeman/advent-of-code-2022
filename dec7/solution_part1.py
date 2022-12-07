from collections import defaultdict
import re


def read_file(filename):
    """Read the input file."""
    with open(filename, "r", encoding="utf-8") as f:
        commands = []
        while True:
            n = f.readline()
            if len(n) > 0:
                commands.append(n.strip("\n"))
            else:
                break
    return commands


def join(string):
    return "".join(string)


class File:
    def __init__(self, name, type="file", size=0, is_dir=None, parent=None) -> None:
        self.name = name
        self.type = type
        self.size = size
        self.is_dir = is_dir
        self.parent = parent

    def __iter__(self):
        return iter([self])

    def __repr__(self) -> str:
        return f"File({self.parent}, {self.name}, {self.type})"

    def __str__(self) -> str:
        return self.__repr__()


class System:
    def __init__(self, console_log) -> None:
        self.commands = ["$ cd", "$ ls"]
        self.console_log = console_log
        self.log = defaultdict(lambda: [])
        self.counter = 0
        self.depth = 0
        self._prev_dirs = []
        self._parent = None

    def run(self, command):
        command_arg = None
        operation = command[:4]
        command_arg = command[5:]
        self.counter += 1
        if operation.startswith("$ cd"):
            if not command_arg == "..":
                self._prev_dirs.append(command_arg)
            self.cd(command_arg)

        elif operation.startswith("$ ls"):
            self.ls(command_arg)
        else:
            pass
            # print(f"skipping non-commands {command}")

    def cd(self, arg):
        print(f"executing cd {arg}")
        self.curr_path = arg
        self.depth += -1 if arg == ".." else 1

    def ls(self, arg):
        print(f"executing ls {arg}")
        self.capture_out()
        self.parse_out()

    def capture_out(self):
        self.out = []
        for out in self.console_log[self.counter :]:
            if out.startswith("$"):
                break
            self.out.append(out)

    def parse_out(self):
        for item in self.out:
            is_dir = item.startswith("dir")
            if is_dir:
                type = "dir"
                size = 0
                name = item[4:]
            else:
                type = "file"
                size = int(join(re.findall("[(0-9)+]", item)))
                name = join(re.findall("[([aA-zZ)+.]", item))
            file = File(
                size=size,
                name=name,
                type=type,
                is_dir=is_dir,
                parent=self._prev_dirs[-1],
            )
            self.log[self.depth].append(file)


class Tree:
    def __init__(self, node, parent=None, children=[]) -> None:
        self.node = node
        self.parent = parent
        self.children = children

    def __repr__(self) -> str:
        return f"Tree({self.parent}, {self.node}, {len(self.children)})"

    def __str__(self) -> str:
        return self.__repr__()


def build_tree(log):
    tree = defaultdict(lambda: [])
    for depth in log:
        for item in log[depth]:
            tree[f"{item.parent}"].append(item)
    print(dict(tree))
    # process directories again
    for dir in tree.copy():
        print(dir)
        items = tree[dir]
        tree[dir] = defaultdict(lambda: [])
        for item in items:
            if item.is_dir:
                tree[dir][f"{item.name}"].append(tree[f"{item.name}"])
                tree.pop(f"{item.name}")
            else:
                tree[dir][f"{item.name}"].append(item)

        tree[dir] = dict(tree[dir])
    print(f"complete")
    return dict(tree)


if __name__ == "__main__":

    _depth = 1
    console_log = read_file("dec7/input.txt")
    # print(console_log)
    os = System(console_log)
    for c in console_log:
        os.run(c)
    # print(os.counter)
    print(f"full tree: {dict(os.log)}")
    print(f"full tree: {os.log.keys()}")
    print(f"full tree-x: {[n.name for n in os.log[1]]}")
    print(f"full tree-x: {[n.parent for n in os.log[1]]}")
    # print(f"\nbuilding tree")
    tree = build_tree(dict(os.log))
    print(tree.keys())
    print(tree)
