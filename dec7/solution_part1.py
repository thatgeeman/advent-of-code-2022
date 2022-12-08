from collections import defaultdict
import re
import joblib

_SMALLEST = 10e32


def argmin(x: list, minval=_SMALLEST):
    """Find the smallest index from a list"""
    idx = None
    for i, xi in enumerate(x):
        if xi < minval:
            minval = xi
            idx = i
    return idx


def read_file(filename):
    """Read the input file, nothing fancy."""
    with open(filename, "r", encoding="utf-8") as f:
        commands = []
        while True:
            n = f.readline()
            if len(n) > 0:
                commands.append(n.strip("\n"))
            else:
                break
    return commands


class File:
    def __init__(
        self,
        name: str,
        id: int,
        parent: str = None,
        type: str = "file",
        size: int = 0,
        is_dir: bool = None,
        depth: int = None,
        n_sib: int = None,
    ) -> None:
        """A simple class that holds the several attributes of each file or
        directory.

        Parameters
        ----------
        name : str
            Name of the item.
        id : int
            Identifier for the item, used sometimes to check absolute distance.
        parent : str, optional
            Parent name of the item, by default None
        type : str, optional
            Indicates the type of the item, can be "file" for a file or
            "dir" for a folder, by default "file"
        size : int, optional
            Size of the item, by default 0
        is_dir : bool, optional
            Indicates if the item is a folder, by default None
        depth : int, optional
            Indicates at what depth from the root directory "/" the item is
            located, by default None
        n_sib : int, optional
            Number of siblings (items in the same folder includng self),
            by default None
        """

        self.name = name
        self.id = id
        self.type = type
        self.size = size
        self.is_dir = is_dir
        self.parent = parent
        self.depth = depth
        self.n_sib = n_sib

    def __iter__(self):
        return iter([self])

    def __repr__(self) -> str:
        return f"File(id={self.id} p={self.parent}, n={self.name}, t={self.type}, s={self.size}, d={self.depth}, sib={self.n_sib})"
        # return f"{self.parent}/{self.name}"

    def __str__(self) -> str:
        return self.__repr__()


class System:
    """
    Class that reads the input file and parses the commands, files, folders,
    subdirectories and their attributes into a plain list of File() objects.
    """

    def __init__(self, console_log: list, commands: list = ["$ cd", "$ ls"]) -> None:
        """Initialize the System() class.

        Parameters
        ----------
        console_log : list
            Whole input from the AOC2022/7 input file
        commands : list, optional
            Commands accepted by the System, by default ["$ cd", "$ ls"]
        """
        self.commands = commands
        self.console_log = console_log
        self.log = defaultdict(lambda: [])
        self.counter = 0
        self.depth = 0
        self._prev_dirs = []
        self.n_items = 0
        self.id = 1

    def run(self, command):
        """Run each command iteratively.

        Separates the command from the arguments.

        Parameters
        ----------
        command : str
            Command as a string.
        """
        command_arg = None
        operation = command[:4]
        command_arg = command[5:]
        self.counter += 1
        if operation.startswith("$ cd"):
            if not command_arg == "..":
                # store history of directories to id parents
                self._prev_dirs.append(command_arg)
            self.cd(command_arg)

        elif operation.startswith("$ ls"):
            self.ls(command_arg)
        else:
            # print(f"skipping non-commands {command}")
            pass

    def cd(self, arg):
        print(f"executing cd {arg}")
        self.curr_path = arg
        # add/sub depth with each call to cd()
        self.depth += -1 if arg == ".." else 1

    def ls(self, arg):
        print(f"executing ls {arg}")
        self.capture_out()
        self.parse_out()

    def capture_out(self):
        """
        Capture the output from the console_log.

        Using the counter as a slicer variable, read all of the
        console_log up until the next comamnd.
        """
        self.out = []
        for out in self.console_log[self.counter :]:
            if out.startswith("$"):
                break
            self.out.append(out)
        self.n_items = len(self.out)

    def parse_out(self):
        """
        Parse the captured output as File() objects.

        If the item is a file, the size, name attributes are read from the
        captured out. If the item is a directory, the name is read.

        The parent and depth attributes are set by corresponding tracker
        variables from run() and cd().
        """
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
                id=self.id,
                name=name,
                type=type,
                is_dir=is_dir,
                parent=self._prev_dirs[-1],
                depth=self.depth,
                n_sib=self.n_items,
            )
            print(f"found {file} in {self._prev_dirs[-1]}")
            self.log[self.depth].append(file)
            self.id += 1


def traverse_from_bottom(log: list):
    """Traverse the File() list collected in the log attribute of System().

    Read from the deepest node to the root node.

    Parameters
    ----------
    log : list
        Collection of File()'s

    Returns
    -------
    list
        A list of File() with the parents assigned as File() objects.
    """
    max_depth = max(log)  # key to access deepest node
    tree = []
    reverse_order = list(range(0, max_depth + 1))[::-1]
    for depth in reverse_order:
        parent = None
        for contents in log[depth]:
            if depth > 0:
                # find parent
                candidates = []
                for prev_depth in log[depth - 1]:
                    if (prev_depth.name == contents.parent) and prev_depth.is_dir:
                        # it should be a dir to be a parent
                        parent = prev_depth
                        candidates.append(parent)
                # if duplicate file names are used at the same depth, multiple
                # parent candidates can arise!
                if len(candidates) > 1:
                    print(contents, candidates, contents.id)
                    print(f"Warning: found {len(candidates)} parents!")
                    # Check for the closest node using absolute distance
                    # of their ids.
                    diffs = []
                    for c in candidates:
                        diff = abs(contents.id - c.id)
                        print(f"{c}: {c.id}, diff:{contents}-{c}={diff}")
                        diffs.append(diff)
                    min_idx = argmin(diffs)
                    parent = candidates[min_idx]
                    print(f"Select {parent}")
            contents.parent = parent
            tree.append(contents)
    return tree


def find_common_parent(t, other_paths):
    """
    Take a path `t` and compare iteratively with other paths `other_path` to
    find if they are in the same directory (under the same parent).

    Will return self if no other paths with same parent.
    """
    items = []
    for op in other_paths:
        conditions = (
            (t.parent is not None) and (t.parent == op.parent) and (t.depth == op.depth)
        )
        if conditions:
            items.append(op)
    return items


def assign_dir_size(t, other_paths):
    """
    Find parent directories and calculate the size attribute of
    each parent directory by summing up all of its child attribute (size),
    starting from the deepest File.
    """
    siblings = find_common_parent(t, other_paths)
    print(f"sib: {len(siblings)}, d={t.depth}, name={t.name}", end=" ")
    dir_size = 0
    for s in siblings:
        dir_size += s.size
    if (t.parent) and (t.parent.size == 0):
        # only assign oif not already assigned by other paths.
        print(f"assigned {t.parent.size} -> {dir_size}")
        t.parent.size = dir_size


if __name__ == "__main__":

    _depth = 1
    console_log = read_file("dec7/input.txt")
    # print(console_log)
    os = System(console_log)
    for c in console_log:
        os.run(c)
    # save
    tmp_log = os.log.copy()
    root_folder = File(
        id=0, parent=None, name="/", size=0, depth=0, type="dir", is_dir=True
    )
    tmp_log[0] = [root_folder]
    joblib.dump(dict(tmp_log), "dec7/inp.joblib")
    # print(f"\nbuilding tree")
    print(tmp_log)

    tree = traverse_from_bottom(tmp_log)

    for t in tree:
        assign_dir_size(t, tree)

    # save tree
    joblib.dump(tree, "dec7/tree.joblib")
    # Part 1:
    dirs = []
    sum_ = 0
    dirs_sum = []

    for t in tree:
        if t.is_dir and t.size <= 100000:
            sum_ += t.size
            # name, size, cumulative sum
            dirs_sum.append((t.name, t.size, sum_))

    print(f"\n\nSum of dirs with size <100000: {sum_}")
