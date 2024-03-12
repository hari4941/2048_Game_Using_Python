import tkinter as tk
import random
from copy import deepcopy

class Game2048(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("2048 Game")
        self.geometry("400x500")
        self.score = 0
        self.board = [[0] * 4 for _ in range(4)]
        self.prev_board = []
        self.colors = {
            0: "lightgray",
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e"
        }
        self.create_widgets()
        self.spawn_tile()
        self.spawn_tile()
        self.update_board()
        self.bind("<Key>", self.handle_keypress)

    def create_widgets(self):
        self.score_label = tk.Label(self, text="Score: 0")
        self.score_label.pack()

        self.canvas = tk.Canvas(self, width=400, height=400, bg="lightgray")
        self.canvas.pack()

        self.restart_button = tk.Button(self, text="Restart", command=self.restart_game)
        self.restart_button.pack()

    def update_board(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.canvas.delete("tile")
        for i in range(4):
            for j in range(4):
                value = self.board[i][j]
                x, y = j * 100, i * 100
                self.canvas.create_rectangle(x, y, x+100, y+100, fill=self.colors[value], outline="black")
                if value:
                    self.canvas.create_text(x+50, y+50, text=str(value), fill="black", font=("Arial", 24, "bold"), tags="tile")

    def spawn_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = 2 if random.random() < 0.9 else 4
            self.update_board()

    def restart_game(self):
        self.score = 0
        self.board = [[0] * 4 for _ in range(4)]
        self.prev_board = []
        self.spawn_tile()
        self.spawn_tile()
        self.update_board()

    def check_valid_moves(self):
        # Check if there are any empty cells
        if any(0 in row for row in self.board):
            return True
        # Check if there are any adjacent cells with the same value
        for i in range(4):
            for j in range(3):
                if self.board[i][j] == self.board[i][j+1] or self.board[j][i] == self.board[j+1][i]:
                    return True
        return False

    def undo_move(self):
        if self.prev_board:
            self.board = deepcopy(self.prev_board)
            self.prev_board = []
            self.update_board()

    def move(self, direction):
        self.prev_board = deepcopy(self.board)
        if direction == "up":
            self.board = list(map(list, zip(*self.board[::-1])))
        elif direction == "down":
            self.board = list(map(list, zip(*self.board)))[::-1]
        elif direction == "right":
            self.board = [row[::-1] for row in self.board]
        for i in range(4):
            self.board[i] = self.merge(self.board[i])
        if direction == "up":
            self.board = list(map(list, zip(*self.board[::-1])))
        elif direction == "down":
            self.board = list(map(list, zip(*self.board)))[::-1]
        elif direction == "right":
            self.board = [row[::-1] for row in self.board]
        self.spawn_tile()
        self.update_board()
        if not self.check_valid_moves():
            self.game_over()

    def merge(self, line):
        merged = [False] * 4
        for i in range(3, 0, -1):
            if line[i] == line[i-1] and line[i] != 0 and not merged[i] and not merged[i-1]:
                line[i] *= 2
                self.score += line[i]
                line[i-1] = 0
                merged[i] = True
        return [val for val in line if val] + [0] * line.count(0)

    def handle_keypress(self, event):
        key = event.keysym.lower()
        if key in ["up", "down", "left", "right"]:
            self.move(key)
        elif key == "z":
            self.undo_move()
        else:
            return

    def game_over(self):
        self.canvas.create_text(200, 200, text="Game Over", fill="red", font=("Arial", 36, "bold"))

if __name__ == "__main__":
    game = Game2048()
    game.mainloop()
