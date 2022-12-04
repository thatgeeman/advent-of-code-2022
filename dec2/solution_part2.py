from solution_part1 import read_file, RPSGamer


def make_move(curr_choice, objective="w"):
    assert objective in ["w", "l"]
    ref = order if objective == "l" else order[::-1]
    idx = [i for i, alp in enumerate(ref) if alp == curr_choice][0]
    return ref[idx + 1]


# X means you need to lose, Y means you need to end the round in a draw,
# and Z means you need to win.
def play_unfair(player1, player2):
    assert isinstance(player1, RPSGamer)
    assert isinstance(player2, RPSGamer)
    print(player1.choice, player2.choice, end=" ")

    if player2._item == "X":
        player2.choice = make_move(player1.choice, "l")
        player2.lose()
    elif player2._item == "Y":
        player2.choice = player1.choice
        player2.draw()
    elif player2._item == "Z":
        player2.choice = make_move(player1.choice, "w")
        player2.win()
    print(f"(change) {player2.choice}")


# Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock
# 0 if you lost, 3 if the round was a draw, and 6 if you won

if __name__ == "__main__":
    # R > S > P > R
    order = "RSPR"
    strategy_sheet = read_file("dec2/input.txt")
    print(f"total rounds: {len(strategy_sheet)}")
    p1 = RPSGamer("Elf", "ABC")
    p2 = RPSGamer("Geevarghese", "XYZ")
    for round in strategy_sheet:
        m1, m2 = round
        p1.set_choice(m1)
        p2.set_choice(m2)
        play_unfair(p1, p2)
        print(p1.score, p2.score)  # does not count P1 score
    print(f"final score: {p1.name}: xx, {p2.name}: {p2.score}")
