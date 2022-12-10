import sys


def read_file(filename):
    """Read the input file, nothing fancy."""
    with open(filename, "r", encoding="utf-8") as f:
        grid = []
        while True:
            n = f.readline()
            if len(n) > 0:
                n = n.strip("\n")
                n = [int(x) for x in n]
                grid.append(n)
            else:
                break
            print(n)
    return grid


def get_top(i, j, grid):
    item = grid[i][j]
    top = [grid[p][j] for p in range(0, i)]
    print(f"items to top of {item}: {top}")
    return top


def get_bottom(i, j, grid):
    item = grid[i][j]
    bottom = [grid[p][j] for p in range(i + 1, len(grid))]
    print(f"items to bottom of {item}: {bottom}")
    return bottom


def get_left(i, j, grid):
    item = grid[i][j]
    left = [grid[i][p] for p in range(0, j)]
    print(f"items to left of {item}: {left}")
    return left


def get_right(i, j, grid):
    item = grid[i][j]
    right = [grid[i][p] for p in range(j + 1, len(grid[0]))]
    print(f"items to right of {item}: {right}")
    return right


def item_is_taller(item, others):
    if len(others) == 0:
        return True
    else:
        all_true = [item > x for x in others]
        return True if len(others) == sum(all_true) else False


if __name__ == "__main__":
    g = read_file("dec8/input.txt")
    # g = read_file("dec8/example.txt")
    print(f"\nfull grid: \n{g}")
    r, c = len(g), len(g[0])
    print(f"\nrows: {r} cols: {c}")
    counts = 0
    for i in range(r):
        for j in range(c):
            # if i == 1 and j == 1:
            item = g[i][j]
            top = get_top(i, j, g)
            bottom = get_bottom(i, j, g)
            left = get_left(i, j, g)
            right = get_right(i, j, g)

            vt = item_is_taller(item, top)
            vb = item_is_taller(item, bottom)
            vl = item_is_taller(item, left)
            vr = item_is_taller(item, right)
            print(f"item is taller than top: {vt} bottom: {vb} left: {vl} right: {vr} ")
            is_visible = sum([vt, vb, vl, vr]) > 0
            print(f"visibility of {item} at {i},{j}: {bool(is_visible)}")
            counts += is_visible
            print("--")
    print(f"total trees visible: {counts}")
