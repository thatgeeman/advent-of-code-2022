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
    def __init__(self, initial_state=(0, 0)) -> None:
        self.head = list(initial_state)
        self.tail = list(initial_state)
        self._op = "-"
        self._axis = 1
        self.head_tracker = defaultdict(lambda: 0)
        self.tail_tracker = defaultdict(lambda: 0)
        self._move_diag = False
        self.head_tracker[str(initial_state)] += 1
        self.tail_tracker[str(initial_state)] += 1

    def move(self, dir="R", by=1, thresh=1.0):
        print(f"move to {dir} by {by} ")
        log = f"-> complete, H:{self.head} T:{self.tail}-> "
        # move_tail = by > 1
        for _ in range(by):
            self._update_head_norm(dir)
            if self._move_diag:
                print(f"move tail from {self.tail} ", end="")
                self._update_tail_diag()
                print(f"to {self.tail}, dist: {self.dist_head_to_tail()}")
            self._need_move_tail(thresh=thresh)

        self._reset()
        log += f" H:{self.head} T:{self.tail}, dist: {self.dist_head_to_tail()}\n"
        print(log)

    def _need_move_tail(self, thresh=1):
        """If needed move tail."""
        dist = self.dist_head_to_tail()
        if dist > thresh:
            print(f"head to tail distance: {dist}! ", end="")
            if self._is_diag():
                print("mark [diag]!")
                self._move_diag = True
                return
            else:
                print(f"move tail [normal] from {self.tail} ", end="")
                self._update_tail_norm()
            print(f"to {self.tail}, dist: {self.dist_head_to_tail()}")

    def _update_head_norm(self, dir):
        tracker = self.head_tracker
        # update y axis
        print(f"move head from {self.head} ", end="")
        if dir == "R" or dir == "U":
            self._op = "+"
        else:
            self._op = "-"
        # update x axis
        if dir == "R" or dir == "L":
            self._axis = 0
        else:
            self._axis = 1
        self._update("head")
        print(f"to {self.head}, dist: {self.dist_head_to_tail()}")
        key = str(self.head)
        tracker[key] += 1

    def _update_tail_norm(self):
        tracker = self.tail_tracker
        # update y axis
        if self._is_same_col():
            self._axis = 1
            self._op = "+" if self._head_is_up() else "-"
            self._update("tail")
        # update x axis
        elif self._is_same_row():
            self._axis = 0
            self._op = "+" if self._head_is_right() else "-"
            self._update("tail")
        self._reset()
        key = str(self.tail)
        tracker[key] += 1

    def _update_tail_diag(self):
        tracker = self.tail_tracker
        if self._head_is_up():
            # make diagonal move by moving each axis once
            # this is a single move although done in two steps
            self._axis = 0
            self._op = "+" if self._head_is_right() else "-"
            self._update("tail")
            self._axis = 1
            self._op = "+"
            self._update("tail")
        elif not self._head_is_up():
            self._axis = 0
            self._op = "+" if self._head_is_right() else "-"
            self._update("tail")
            self._axis = 1
            self._op = "-"
            self._update("tail")
        self._reset()
        key = str(self.tail)
        tracker[key] += 1

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
        self._move_diag = False
        self._op = "-"
        self._axis = 1

    def dist_head_to_tail(self):
        hx, hy = self.head
        tx, ty = self.tail
        euc_dist = pow((pow(hx - tx, 2) + pow(hy - ty, 2)), 0.5)
        # abs_dist = (abs(hx - tx) + abs(hy - ty)) / 2
        return round(euc_dist, 2)

    def _head_is_up(self):
        """Check if head is up"""
        _, hy = self.head
        _, ty = self.tail
        return hy > ty

    def _head_is_right(self):
        """Check if head is on the right"""
        hx, _ = self.head
        tx, _ = self.tail
        return hx > tx

    def _is_same_row(self):
        _, hy = self.head
        _, ty = self.tail
        return hy == ty

    def _is_same_col(self):
        hx, _ = self.head
        tx, _ = self.tail
        return hx == tx

    def _is_diag(self):
        return self.dist_head_to_tail() == 1.41

    def show_map(self, max_x=None, max_y=None):
        tail_hist = list(self.tail_tracker.keys())
        tail_hist = [eval(p) for p in tail_hist]
        print(tail_hist)
        if not max_x:
            max_x = max(tail_hist, key=lambda x: x[0])[0]
        if not max_y:
            max_y = max(tail_hist, key=lambda x: x[1])[1]
        print(max_x, max_y)
        for i in range((max_x + 1) * (max_y + 1)):
            print(".", end=" ")
            if (i + 1) % (max_x + 1) == 0:
                print("\n")


if __name__ == "__main__":
    commands = read_file("dec9/example.txt")
    # commands = read_file("dec9/input.txt")

    print(commands)
    rope = Rope()
    for c in commands:
        dir, by = c.split(" ")
        rope.move(dir, int(by))
    # add ending position to tracker
    # rope.head_tracker[str(rope.head)] += 1
    # rope.tail_tracker[str(rope.tail)] += 1

    # print(f"\nH: {dict(rope.head_tracker)}")
    # print(f"\nT: {dict(rope.tail_tracker)}")
    count = 0
    for k, v in rope.tail_tracker.items():
        if v > 0:
            count += v
    counth = 0
    for k, v in rope.head_tracker.items():
        if v > 0:
            counth += v
    print(f"\nfinal abs distance between final HT: {rope.dist_head_to_tail()}")

    print(f"total visits by head: {counth}")
    print(f"total visits by tail: {count}")
    print(f"unique sites visited by head: {len(rope.head_tracker)}")
    print(f"unique sites visited by tail: {len(rope.tail_tracker)}")

    # rope.show_map(5, 4)
