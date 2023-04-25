from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from tictactoe import TicTacToe


class TicTacToeApp(App):
    def build(self):
        # Set the window size
        Config.set('graphics', 'width', '600')
        Config.set('graphics', 'height', '600')
        Config.write()

        self.title = "Tic-Tac-Toe"
        self.game = TicTacToe()
        self.root = Builder.load_file("tictactoe.kv")
        return self.root

    def on_start(self):
        self.reset_game()

    def make_move(self, position):
        result = self.game.make_move(position)

        if result:
            # Update the status label
            status_label = self.root.ids["status_label"]
            status_label.text = result

            # Disable all buttons
            for i in range(9):
                self.root.ids[f"cell{i}"].disabled = True

        # Update the UI with the move
        button = self.root.ids[f"cell{position}"]
        button.text = self.game.board[position]
        button.disabled = True

    def reset_game(self):
        self.game = TicTacToe()

        # Reset UI
        for i in range(9):
            button = self.root.ids[f"cell{i}"]
            button.text = ""
            button.disabled = False

        status_label = self.root.ids["status_label"]
        status_label.text = "Tic-Tac-Toe"


if __name__ == "__main__":
    TicTacToeApp().run()

