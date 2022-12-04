def read_file(filename):
    round = []
    with open(filename, "r") as f:
        while True:
            n = f.readline()
            if len(n) == 0:
                break
            else:
                n = n.strip()
                m1, m2 = n.split(" ")
                round.append([m1, m2])
    return round


class RPSGamer:
    def __init__(self, name, encoding):
        self.name: str = name
        self.encoding: str = encoding  # ABC
        self.choice = None
        self.score = 0
        self.rps = "RPS"
        # {R: 1, P: 2, S: 3}
        self._points = dict(zip(self.rps, [1, 2, 3]))
        # {A: 1, B: 2, C: 3}
        self._points_enc = dict(zip(self.encoding, [1, 2, 3]))
        # {A: R, B: P, C: S}
        self._vocab = dict(zip(self.encoding, self.rps))
        # print(self.points, self.vocab)

    def set_choice(self, item):
        assert item in self.encoding
        # print(item, self.vocab[item])
        self._item = item
        self.choice = self._vocab[item]

    def win(self):
        # print(self.points[self.choice])
        self.score += self._points[self.choice] + 6

    def lose(self):
        self.score += self._points[self.choice]

    def draw(self):
        self.score += self._points[self.choice] + 3


def find_choice(curr_choice, obective="w"):
    assert obective in ["w", "l"]
    ref = "RSPR" if obective == "l" else "RPSR"
    idx = [i for i, alp in enumerate(ref) if alp == curr_choice][0]
    return ref[idx + 1]


# X means you need to lose, Y means you need to end the round in a draw,
# and Z means you need to win.
def play_unfair(player1, player2):
    assert isinstance(player1, RPSGamer)
    assert isinstance(player2, RPSGamer)
    print(
        player1.choice,
        player2.choice,
    )

    if player2._item == "X":
        player2.choice = find_choice(player1.choice, "l")
        print(f"*{player2.choice}")
        player2.lose()
    elif player2._item == "Y":
        player2.choice = player1.choice
        player2.draw()
    elif player2._item == "Z":
        player2.choice = find_choice(player1.choice, "w")
        print(f"*{player2.choice}")
        player2.win()


# Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock
# 0 if you lost, 3 if the round was a draw, and 6 if you won

if __name__ == "__main__":
    # R > S > P > R
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
