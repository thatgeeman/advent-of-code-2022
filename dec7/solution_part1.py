from collections import defaultdict
import re
import joblib


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
    def __init__(
        self,
        name,
        type="file",
        size=0,
        is_dir=None,
        parent=None,
        depth=None,
        children=None,
    ) -> None:
        self.name = name
        self.type = type
        self.size = size
        self.is_dir = is_dir
        self.parent = parent
        self.depth = depth
        self.children = children

    def __iter__(self):
        return iter([self])

    def __repr__(self) -> str:
        return f"File(parent={self.parent}, name={self.name}, t={self.type}, s={self.size}, d={self.depth})"

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
                size = int(re.findall("[(0-9)]+", item)[0])
                # some files do not have .ext
                name = re.findall("[a-zA-Z].+|[a-zA-Z]+", item)[0]
            file = File(
                size=size,
                name=name,
                type=type,
                is_dir=is_dir,
                parent=self._prev_dirs[-1],
                depth=self.depth,
            )
            print(f"found {file} in {self._prev_dirs[-1]}")
            self.log[self.depth].append(file)


def build_flat_tree(log):
    max_depth = max(log)  # key to access deepest node
    tree = []
    reverse_order = list(range(0, max_depth + 1))[::-1]
    for depth in reverse_order:
        parent = None
        for contents in log[depth]:
            if depth > 0:
                # find parent
                for prev_contents in log[depth - 1]:
                    if prev_contents.name == contents.parent:
                        parent = prev_contents
                        break
            contents.parent = parent
            tree.append(contents)
    return tree


def find_common_parent(t, other_paths):
    """
    Take a path `t` and compare iteratively with other paths `other_path` to
    find if they are in the same directory (under the same parent).

    Will return [`t`] if no other paths with same parent.
    """
    l = []
    for op in other_paths:
        if t.parent == None:
            # if last node
            continue
        if t.parent != op.parent:
            # if different parents
            continue
        l.append(op)
    return l


def assign_dir_size(t, other_paths):
    """
    Find parent directories and assign the size attribute of
    each parent, starting from the deepest File (see `build_flat_tree`).
    """
    siblings = find_common_parent(t, other_paths)
    print(f"sib: {len(siblings)}, d={t.depth}, name={t.name}", end=" ")
    dir_size = 0
    for s in siblings:
        # if s.size <= 100000:
        # assign all sizes, filter later
        dir_size += s.size
    if (t.parent) and (t.parent.size == 0):
        # only assign oif not already assigned by other paths.
        print(f"assigned {t.parent.size} -> {dir_size}")
        t.parent.size = dir_size
    elif t.parent:
        print(f"not assigned current: {t.parent.size} suggested add: {dir_size}")


if __name__ == "__main__":

    _depth = 1
    console_log = read_file("dec7/input.txt")
    # print(console_log)
    os = System(console_log)
    for c in console_log:
        os.run(c)
    # save
    tmp_log = os.log.copy()
    root_folder = File(parent=None, name="/", size=0, depth=0, type="dir", is_dir=True)
    tmp_log[0] = [root_folder]
    joblib.dump(dict(tmp_log), "dec7/inp.joblib")
    tmp_log = joblib.load("dec7/inp.joblib")
    # print(f"\nbuilding tree")
    print(tmp_log)
    tree = build_flat_tree(tmp_log)

    for t in tree:
        assign_dir_size(t, tree)

    # taker sum
    sum_lt = 0
    for t in tree:
        for p in set(os._prev_dirs):
            if t.parent is None:
                continue
            if (t.parent.name == p) and (t.size <= 100000) and (t.is_dir):
                # print(t.size)
                sum_lt += t.size

    print(f"\n\nsum is {sum_lt}")
