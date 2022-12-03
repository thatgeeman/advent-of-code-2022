def read_file(filename):
    calories = [[]]
    with open(filename, "r") as f:
        while True:
            n = f.readline()
            if len(n) == 0:
                break
            else:
                if n == "\n":
                    calories.append([])
                else:
                    print(n)
                    calories[-1].append(int(n))
    return calories


def get_largest(x):
    largest_idx = 0
    largest_val = 0
    for idx, vals in enumerate(x):
        # print(vals)
        if sum(vals) > largest_val:
            largest_val = sum(vals)
            largest_idx = idx
    return largest_val, largest_idx


if __name__ == "__main__":
    calories = read_file("./input.txt")
    print(calories)
    max_calories, idx = get_largest(calories)
    print(f"largest calorie carrier: {max_calories} at index {idx}")
