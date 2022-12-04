from typing import List
from collections import Counter
from string import ascii_letters
from dataclasses import dataclass


def read_file(filename):
    items = []
    with open(filename, "r") as f:
        while True:
            n = f.readline()
            if len(n) == 0:
                break
            else:
                n = n.strip()
                items.append(n)
    return items


@dataclass
class Rucksack:
    items: List

    def __call__(self):
        self.pack()
        self.set_priority()
        self.shared_items()
        self.count_priority()
        return self

    def pack(self):
        items = self.items
        half = int(len(items) / 2)
        self.A = items[:half]
        self.B = items[half:]

    def set_priority(self):
        n = len(ascii_letters)
        self.priority = dict(zip(ascii_letters, range(1, n + 1)))

    def shared_items(self):
        self.shared = Counter()
        for a in self.A:
            if a in self.B:
                self.shared.update(a)

    def count_priority(self):
        self.sum_priority = 0
        for item, c in self.shared.items():
            self.sum_priority += self.priority[item]


if __name__ == "__main__":
    item_list = read_file("dec3/input.txt")
    print(f"total rucksacks: {len(item_list)}")
    # print(item_list)
    total = 0
    for items in item_list:
        r = Rucksack(items)()
        print(r.A, r.B, r.sum_priority)
        total += r.sum_priority
    print(f"\ntotal sum of priorities: {total}")
