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
        # default points for choice
        self.score += self._points_enc[item]

    def win(self):
        # print(self.points[self.choice])
        self.score += 6

    def lose(self):
        self.score += 0

    def draw(self):
        self.score += 3


def play(player1, player2):
    assert isinstance(player1, RPSGamer)
    assert isinstance(player2, RPSGamer)
    print(player1.choice, player2.choice)
    if player1.choice == player2.choice:
        player1.draw()
        player2.draw()
    if player1.choice == "R" and player2.choice == "S":
        player1.win()
        player2.lose()
    if player1.choice == "S" and player2.choice == "R":
        player1.lose()
        player2.win()
    if player1.choice == "S" and player2.choice == "P":
        player1.win()
        player2.lose()
    if player1.choice == "P" and player2.choice == "S":
        player1.lose()
        player2.win()
    if player1.choice == "P" and player2.choice == "R":
        player1.win()
        player2.lose()
    if player1.choice == "R" and player2.choice == "P":
        player1.lose()
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
        play(p1, p2)
        # print(p1.score, p2.score)
    print(f"final score: {p1.name}: {p1.score}, {p2.name}: {p2.score}")
