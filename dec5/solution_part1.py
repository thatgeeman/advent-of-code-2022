import re
from collections import defaultdict
import sys
from typing import Dict


def read_state(filename, max_stacks=9):
    """
    Parse the input file line by line, only upto the state of the crates!

    ! The states are read line by line. Only stacked in order posteriori
    ! by `build_stack`

    Parameters
    ----------
    filename : str
        Input file with state and moves
    max_stacks : int, optional
        Number of stacks of crates in input file, by default 9

    Returns
    -------
    list
        State of the crates as nested list, indicating the crate position
        (1...N) and the corresponding crate name.
    """
    items = []
    with open(filename, "r", encoding="utf-8") as f:
        while True:
            n = f.readline()
            if len(n) == 1:
                break
            elif len(n) > 4 * max_stacks:  # one box "[A] " takes 4 characters
                break
            else:
                crates_ = n.strip("\n")  # keep the spaces
                crates = re.findall("([A-Z])+", crates_)
                # find position of crate
                expected_pos = [(i * 4) + 1 for i in range(max_stacks)]
                ghost_crates = [c for i, c in enumerate(crates_) if i in expected_pos]
                crate_idx = [i + 1 for i, l in enumerate(ghost_crates) if l != " "]
                items.append([crate_idx, crates])
    return items[:-1]


def read_moves(filename):
    """
    Parse the input file line by line, reading only the moves!

    Parameters
    ----------
    filename : str
        Input file with state and moves

    Returns
    -------
    list
        Nested list of number of crates and stack numbers to move from and to.
    """
    items = []
    with open(filename, "r", encoding="utf-8") as f:
        while True:
            n = f.readline()
            if n.startswith("move"):
                line = n.strip("\n")  # keep the spaces
                instruction = re.findall("([0-9]+)+", line)  # double digits!
                items.append([int(i) for i in instruction])
            elif len(n) == 0:
                break
    return items


def build_stack(state):
    """
    Arrange the crates read from `read_state` into a dict of lists.

    Parameters
    ----------
    state : list
        List of lists with stack number and crate name.

    Returns
    -------
    dict
        Dict of lists where the key denotes the stack number and the value is a
        list of crates assigned to the stack.
    """
    stack = defaultdict(lambda: [])
    # start from last to make the stack
    for s in state[::-1]:
        idxs, names = s
        for i, idx in enumerate(idxs):
            stack[idx].append(names[i])
    return dict(stack)


def find_top_crate(stack: Dict):
    """Read the last item in each stack (dict)."""
    top = ""
    for _, items in stack.items():
        try:
            top += items[-1]
        except IndexError:
            # if for some reason the stack is empty
            top += "-"
    return top


if __name__ == "__main__":
    # read line by line
    try:
        max_stacks = int(sys.argv[1])
    except IndexError:
        print("expected max_stacks argument")
        sys.exit(1)
    state = read_state("dec5/input.txt", max_stacks=max_stacks)
    print(state)
    # stack in reverse
    stack = build_stack(state)
    print(stack)
    # read the moves part
    moves = read_moves("dec5/input.txt")
    print("begin moves:")
    for m in moves:
        num, frm, to = m
        print(f"- move {num} from {frm} to {to}")
        put = stack[frm][-num:]
        # boxes moved one by one so stack in reverse
        stack[to].extend(put[::-1])
        take = stack[frm][:-num]
        stack[frm] = take
    print(f"\nfinal state after {len(moves)} moves")
    print(stack)
    top = find_top_crate(stack)
    print(top)
