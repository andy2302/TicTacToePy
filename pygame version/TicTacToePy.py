import pygame
import sys
import json


# TicTacToe implementation for pygame, it's not completely functional
class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        self.x_color = [1, 0, 0, 1]
        self.o_color = [0, 0, 1, 1]
        self.cell_size = 40
        self.game_over = False

    def make_move(self, position):
        if self.board[position] == " " and not self.game_over:
            self.board[position] = self.current_player
            if self.check_winner():
                self.game_over = True
                return f"{self.current_player} wins!"
            if self.check_draw():
                self.game_over = True
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


# Constants
WIDTH = 1000
HEIGHT = 1000
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 4
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
CIRCLE_COLOR = (255, 0, 0)
CROSS_COLOR = (0, 0, 255)

# Initialize Pygame
pygame.init()

# Create a screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")
screen.fill(BG_COLOR)

# Load settings
try:
    with open("settings.json", "r") as f:
        settings = json.load(f)
        CIRCLE_COLOR = tuple(settings["x_color"])
        CROSS_COLOR = tuple(settings["o_color"])
        FONT_SIZE = settings["cell_size"]
except FileNotFoundError:
    # Set default values if the settings file doesn't exist
    CIRCLE_COLOR = (255, 0, 0, 255)
    CROSS_COLOR = (0, 0, 255, 255)
    FONT_SIZE = 40

# Initialize the game
game = TicTacToe()


def draw_lines():
    # Draw horizontal lines
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
    # Draw vertical lines
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if game.board[row * BOARD_COLS + col] == "X":
                draw_cross(row, col)
            elif game.board[row * BOARD_COLS + col] == "O":
                draw_circle(row, col)


def draw_circle(row, col):
    pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), CIRCLE_RADIUS, CIRCLE_WIDTH)


def draw_cross(row, col):
    pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
    pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)


def mark_square(row, col):
    global game
    position = row * BOARD_COLS + col

    if not check_win() and not check_draw():
        result = game.make_move(position)

        if result:
            status_text = f"{game.current_player} wins!"
        elif game.check_draw():
            status_text = "It's a draw!"
        else:
            game.switch_player()
            status_text = f"{game.current_player}'s turn"
    else:
        reset_game()
        status_text = f"{game.current_player}'s turn"

    print(status_text)


def check_win():
    return game.check_winner()


def check_draw():
    return game.check_draw()


def reset_game():
    game.__init__()


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def switch_player():
    game.switch_player()


draw_lines()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not check_win() and not check_draw():
                row, col = get_row_col_from_mouse(pygame.mouse.get_pos())
                mark_square(row, col)
                draw_figures()
                switch_player()
            else:
                reset_game()
                screen.fill(BG_COLOR)
                draw_lines()

    pygame.display.update()

pygame.quit()
sys.exit()
