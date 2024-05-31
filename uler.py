import ttkbootstrap as tb
from tkinter import Canvas, ALL
from tkinter.constants import X, LEFT, RIGHT  # Import constants from tkinter
import random
import os

GAME_WIDTH = 1000
GAME_HEIGHT = 600
SPEED = 100
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "#0000FF"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
HIGH_SCORE_FILE = "high_score.txt"  # File to store the highest score

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])
        
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label_score.config(text="Score: {}".format(score))

        if score > highest_score:
            update_highest_score(score)

        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
        
    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 50,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
    canvas.create_window(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 50, window=restart_button)


def load_highest_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, 'r') as file:
            return int(file.read().strip())
    return 0


def update_highest_score(new_highest_score):
    global highest_score
    highest_score = new_highest_score
    label_highest_score.config(text="Highest Score: {}".format(highest_score))
    with open(HIGH_SCORE_FILE, 'w') as file:
        file.write(str(highest_score))


def restart_game():
    global score, direction, snake, food
    score = 0
    direction = 'down'
    label_score.config(text="Score: {}".format(score))
    canvas.delete(ALL)  # Clear the canvas
    snake = Snake()  # Create a new snake
    food = Food()  # Create new food
    next_turn(snake, food)  # Start the game again


# Initialize the ttkbootstrap themed window
window = tb.Window(themename="darkly")
window.title("Snake Game")
window.resizable(False, False)

score = 0
highest_score = load_highest_score()  # Load the highest score at the start
direction = 'down'

frame = tb.Frame(window)
frame.pack(fill=X)

label_score = tb.Label(frame, text="Score: {}".format(score), font=('consolas', 20))
label_score.pack(side=LEFT, padx=10)

label_highest_score = tb.Label(frame, text="Highest Score: {}".format(highest_score), font=('consolas', 20))
label_highest_score.pack(side=RIGHT, padx=10)

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

restart_button = tb.Button(window, text="Restart Game", command=restart_game, bootstyle="success")
restart_button.pack_forget()  # sembunyike dulu buttonny

window.update()

# Calculate the center position
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

# Set the window position to the center of the screen
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
