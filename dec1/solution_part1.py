def read_file(filename):
    sums = [[]]
    with open(filename, "r") as f:
        while True:
            n = f.readline()
            if len(n) == 0:
                break
            else:
                if n == "\n":
                    sums.append([])
                else:
                    print(n)
                    sums[-1].append(int(n))
    return sums


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
    calories = read_file("dec1/input.txt")
    print(calories)
    max_calories, idx = get_largest(calories)
    print(f"largest calorie carrier: {max_calories} at index {idx}")
