from collections import defaultdict


def read_file(filename):
    """Read the input file, nothing fancy."""
    with open(filename, "r", encoding="utf-8") as f:
        commands = []
        while True:
            n = f.readline()
            if len(n) > 0:
                n = n.strip("\n")
                commands.append(n)
            else:
                break
    return commands


class Rope:
    def __init__(self) -> None:
        self.head = [0, 0]
        self.tail = [0, 0]
        self._op = "-"
        self._axis = 1
        self.head_tracker = defaultdict(lambda: 0)
        self.tail_tracker = defaultdict(lambda: 0)
        self.head_tracker[f"{self.tail}"] += 1
        self.tail_tracker[f"{self.tail}"] += 1

    def move(self, dir="R", by=1):
        log = f"H:{self.head} T:{self.tail}->"
        for i in range(by):
            self._move(dir)
        self._reset()
        log += f"H:{self.head} T:{self.tail}"
        print(log)

    def _move(self, dir="R", thresh=1):
        self._update_head(dir)
        dist = self.dist()
        if dist > thresh:
            # check if same row
            # check if same col
            # check if need to change direction (if head is left)
            # should be independent of heads move
            self._update_tail(dir)

    def _update_head(self, dir):
        if dir == "R" or dir == "U":
            self._op = "+"
        if dir == "R" or dir == "L":
            self._axis = 0
        self._update("head")
        self.head_tracker[f"{self.head}"] += 1

    def _update_tail(self, dir):
        self._update("tail")
        self.tail_tracker[f"{self.tail}"] += 1

    def _update(self, ht):
        if ht == "tail":
            val = self.tail[self._axis]
        else:
            val = self.head[self._axis]
        new_val = eval(f"{val}{self._op}{1}")
        if ht == "tail":
            self.tail[self._axis] = new_val
        else:
            self.head[self._axis] = new_val

    def _reset(self):
        self._op = "-"
        self._axis = 1

    def dist(self):
        x1, y1 = self.head
        x2, y2 = self.tail
        return pow((pow(x1 - x2, 2) + pow(y1 - y2, 2)), 0.5)


if __name__ == "__main__":
    # commands = read_file("dec9/input.txt")
    commands = read_file("dec9/example.txt")
    print(commands)
    rope = Rope()
    for c in commands:
        dir, by = c.split(" ")
        rope.move(dir, int(by))

    print(f"\nH: {dict(rope.head_tracker)}")
    print(f"\nT: {dict(rope.tail_tracker)}")
    count = 0
    for k, v in rope.tail_tracker.items():
        if v > 0:
            count += 1
    print(len(rope.head_tracker))
    print(f"positions visited by tail at least once: {count}")
