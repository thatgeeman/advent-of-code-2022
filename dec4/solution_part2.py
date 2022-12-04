def read_file(filename):
    items = []
    with open(filename, "r") as f:
        while True:
            n = f.readline()
            if len(n) == 0:
                break
            else:
                n = n.strip()
                p1, p2 = n.split(",")
                a, b = p1.split("-")
                p1 = range(int(a), int(b) + 1)
                c, d = p2.split("-")
                p2 = range(int(c), int(d) + 1)
                items.append([set(p1), set(p2)])
    return items


if __name__ == "__main__":
    item_list = read_file("dec4/input.txt")
    print(f"total pairs: {len(item_list)}")
    print(item_list)
    total = 0
    for items in item_list:
        p1, p2 = items
        common = p1 & p2
        n_common = len(common)
        total += 1 if n_common > 0 else 0
    print(f"\ntotal pairs: {total}")
