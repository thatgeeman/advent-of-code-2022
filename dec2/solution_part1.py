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


def check_rule_book(A_choice: str, B_choice: str, order):
    if A_choice == B_choice:
        return "draw"
    elif A_choice == "S" and B_choice == "R":
        order = order[1:]
    elif A_choice == "R" and B_choice == "S":
        order = order[1:]
    elif A_choice == "P" and B_choice == "R":
        order = order[:-1]
    elif A_choice == "R" and B_choice == "P":
        order = order[:-1]
    A_idx = order.index(A_choice)
    B_idx = order.index(B_choice)
    _tmp_order = {A_choice: A_idx, B_choice: B_idx}
    return max(_tmp_order, key=lambda x: _tmp_order[x])


def play(player1, player2, order):
    assert isinstance(player1, RPSGamer)
    assert isinstance(player2, RPSGamer)
    result = check_rule_book(player1.choice, player2.choice, order)
    print(f"{player1.choice}, {player2.choice} -> {result}")
    if result == "draw":
        player1.draw()
        player2.draw()
    elif player1.choice == result:
        player1.win()
        player2.lose()
    elif player2.choice == result:
        player1.lose()
        player2.win()


# Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock
# 0 if you lost, 3 if the round was a draw, and 6 if you won

if __name__ == "__main__":
    # R < P < S < R
    order = "RPSR"
    strategy_sheet = read_file("dec2/input.txt")
    print(f"total rounds: {len(strategy_sheet)}")
    p1 = RPSGamer("Elf", "ABC")
    p2 = RPSGamer("Geevarghese", "XYZ")
    for round in strategy_sheet:
        m1, m2 = round
        p1.set_choice(m1)
        p2.set_choice(m2)
        play(p1, p2, order)
        # print(p1.score, p2.score)
    print(f"final score: {p1.name}: {p1.score}, {p2.name}: {p2.score}")
