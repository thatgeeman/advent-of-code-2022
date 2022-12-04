from string import ascii_letters


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


def regroup(items):
    return list(zip(items[::3], items[1::3], items[2::3]))


def get_item_priority(item):
    n = len(ascii_letters)
    priority = dict(zip(ascii_letters, range(1, n + 1)))
    return priority[item]


def find_common(bag1, bag2, bag3):
    a, b, c = set(bag1), set(bag2), set(bag3)
    return list(a & b & c)[0]  # assuming single common item


if __name__ == "__main__":
    item_list = read_file("dec3/input.txt")
    print(f"total rucksacks: {len(item_list)}")
    grouped_list = regroup(item_list)
    print(f"total regrouped: {len(grouped_list)}")
    # print(item_list)
    total = 0
    for items in grouped_list:
        a, b, c = items
        common_item = find_common(a, b, c)
        print(common_item)
        total += get_item_priority(common_item)
    print(f"\ntotal sum of priorities: {total}")
