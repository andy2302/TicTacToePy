class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"

    def make_move(self, position):
        if self.board[position] == " ":
            self.board[position] = self.current_player
            if self.check_winner():
                return f"{self.current_player} wins!"
            if self.check_draw():
                return "It's a draw!"
            self.switch_player()
        else:
            return "Invalid move!"

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combination in winning_combinations:
            if all(self.board[pos] == self.current_player for pos in combination):
                return True
        return False

    def check_draw(self):
        return all(cell != " " for cell in self.board)

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"
