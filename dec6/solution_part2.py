from solution_part1 import read_file, check_chunks


if __name__ == "__main__":
    message = read_file("dec6/input.txt")
    print(message)
    # message = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
    marker, pos = check_chunks(message, 14)
    print(f"got marker: {marker} at {pos}")
