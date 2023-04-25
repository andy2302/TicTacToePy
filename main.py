from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from tictactoe import TicTacToe
import json


class TicTacToeApp(App):
    def build(self):
        # Set the window size
        Config.set('graphics', 'width', '1000')
        Config.set('graphics', 'height', '1000')

        self.title = "Tic-Tac-Toe"
        self.game = TicTacToe()
        self.root = Builder.load_file("tictactoe.kv")
        return self.root

    def on_start(self):
        self.load_settings()
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
        else:
            # Update the status label to show the current player
            status_label = self.root.ids["status_label"]
            status_label.text = f"{self.game.current_player}'s turn"

        # Update the UI with the move
        button = self.root.ids[f"cell{position}"]
        button.text = self.game.board[position]
        button.background_color = self.game.x_color if self.game.board[position] == "X" else self.game.o_color
        button.color = self.game.x_color if self.game.board[position] == "X" else self.game.o_color
        button.font_size = self.game.cell_size
        button.background_normal = ""
        button.disabled = True

    def reset_game(self):
        self.game = TicTacToe()
        self.load_settings()  # Add this line to load the settings after re-initializing the game

        # Reset UI
        for i in range(9):
            button = self.root.ids[f"cell{i}"]
            button.text = ""
            button.disabled = False
            button.background_normal = 'atlas://data/images/defaulttheme/button'
            button.background_color = [1, 1, 1, 1]
            button.colors = {"X": [0, 0, 0, 1], "O": [0, 0, 0, 1]}

        status_label = self.root.ids["status_label"]
        status_label.text = f"{self.game.current_player}'s turn"

    def apply_settings(self, x_color, o_color, cell_size):
        self.game.x_color = x_color
        self.game.o_color = o_color
        self.game.cell_size = int(cell_size)  # Convert the cell_size to an integer
        self.save_settings()

        for index, button in enumerate(self.root.ids.grid.children):
            if button.text == "X":
                button.background_color = x_color
                button.font_size = int(cell_size)  # Convert the cell_size to an integer
            elif button.text == "O":
                button.background_color = o_color
                button.font_size = int(cell_size)  # Convert the cell_size to an integer

        App.get_running_app().root.current = "main_menu"

    def save_settings(self):
        settings = {
            "x_color": self.game.x_color,
            "o_color": self.game.o_color,
            "cell_size": self.game.cell_size,
        }
        with open("settings.json", "w") as f:
            json.dump(settings, f)

    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
                self.game.x_color = settings["x_color"]
                self.game.o_color = settings["o_color"]
                self.game.cell_size = settings["cell_size"]
        except FileNotFoundError:
            # Set default values if the settings file doesn't exist
            self.game.x_color = [1, 0, 0, 1]
            self.game.o_color = [0, 0, 1, 1]
            self.game.cell_size = "max"


if __name__ == "__main__":
    TicTacToeApp().run()
