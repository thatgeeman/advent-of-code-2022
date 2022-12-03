from solution_part1 import get_largest, read_file


if __name__ == "__main__":
    calories = read_file("dec1/input.txt")
    print(calories)
    total_top_3 = 0
    for i in range(3):
        max_calories, idx = get_largest(calories)
        print(f"calories (rank {i}): {max_calories} at index {idx}")
        calories.pop(idx)
        total_top_3 += max_calories
    print(f"total calories carried by top-3 carriers: {total_top_3}")
