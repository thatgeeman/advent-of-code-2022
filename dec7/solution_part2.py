import joblib
from solution_part1 import argmin, File

if __name__ == "__main__":
    tree = joblib.load("dec7/tree.joblib")
    # Part 2:
    update_req = 30000000
    total_space = 70000000
    free = total_space - tree[-1].size
    need = update_req - free

    diffs = []
    for t in tree:
        if t.is_dir:
            diff = need - t.size
            if diff < 0:
                diffs.append([t, abs(diff)])
                print(
                    f"deleting {t.name} of size {t.size}, will give more than needed: {abs(diff)}"
                )
            else:
                # print(f"deleting {t.name} of size {t.size}, will still need: {diff}")
                pass
    d = [x for _, x in diffs]
    dir = diffs[argmin(d)][0]

    print(f"\n\nSmallest dir: {dir} with size {dir.size}")
