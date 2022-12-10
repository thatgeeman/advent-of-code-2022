from solution_part1 import read_file, get_bottom, get_left, get_right, get_top


def view_blockers(item, others):
    if len(others) == 0:
        return 0
    else:
        for idx, x in enumerate(others, start=1):
            if x > item:
                break
            if x == item:
                return idx
        return idx


if __name__ == "__main__":
    g = read_file("dec8/input.txt")
    # g = read_file("dec8/example.txt")
    print(f"\nfull grid: \n{g}")
    r, c = len(g), len(g[0])
    print(f"\nrows: {r} cols: {c}")
    best_score = 0
    coord = 0, 0
    for i in range(r):
        for j in range(c):
            # if i == 1 and j == 1:
            item = g[i][j]
            top = get_top(i, j, g)
            bottom = get_bottom(i, j, g)
            left = get_left(i, j, g)
            right = get_right(i, j, g)

            bt = view_blockers(item, top[::-1])
            bb = view_blockers(item, bottom)
            bl = view_blockers(item, left[::-1])
            br = view_blockers(item, right)
            scenic_score = bt * bb * bl * br
            print(f"scenic_score ({i}, {j}): {scenic_score}")
            print(f"from top: {bt} bottom: {bb} left: {bl} right: {br}")
            print("--")
            if scenic_score > best_score:
                best_score = scenic_score
                coord = i, j
                print(f"new best score: {best_score} at {coord}")
    print(f"\nbest score: {best_score} at {coord}")
