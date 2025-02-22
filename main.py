from tkinter import *
import random
from PIL import Image, ImageTk

CANVAS_WIDTH = 1400
CANVAS_HEIGHT = 800
BACKGROUND_COLOR = "#f3f3f3"
SPEED = 120
SPACE_SIZE = 75
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"

def load_and_resize_image(file_path, size):
    try:
        image = Image.open(file_path)
        image = image.resize((size, size))
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Error loading or resizing image {file_path}: {e}")
        exit()

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for _ in range(BODY_PARTS):
            self.coordinates.append((0, 0))

        for i, (x, y) in enumerate(self.coordinates):
            if i == 0:
                image = snake_head_image
            elif i == len(self.coordinates) - 1:
                image = snake_tail_image
            else:
                image = snake_body_image
            square = canvas.create_image(x, y, image=image, anchor="nw", tags="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (CANVAS_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (CANVAS_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = (x, y)
        canvas.create_image(x, y, image=food_image, anchor="nw", tags="food")

def isCollide(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= CANVAS_WIDTH:
        return True
    if y < 0 or y >= CANVAS_HEIGHT:
        return True

    for body in snake.coordinates[1:]:
        if x == body[0] and y == body[1]:
            return True

    return False

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    match direction:
        case "up":
            y -= SPACE_SIZE
        case "down":
            y += SPACE_SIZE
        case "left":
            x -= SPACE_SIZE
        case "right":
            x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_image(x, y, image=snake_head_image, anchor="nw")
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        label.config(text="Score:{}".format(score))

        canvas.delete("food")
        food = Food()

    else:

        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    for i, (x, y) in enumerate(snake.coordinates):
        if i == 0:
            canvas.itemconfig(snake.squares[i], image=snake_head_image)
        elif i == len(snake.coordinates) - 1:
            canvas.itemconfig(snake.squares[i], image=snake_tail_image)
        else:
            canvas.itemconfig(snake.squares[i], image=snake_body_image)

    if isCollide(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction

    if new_direction == "left":
        if direction != "right":
            direction = new_direction
    elif new_direction == "up":
        if direction != "down":
            direction = new_direction
    elif new_direction == "right":
        if direction != "left":
            direction = new_direction
    elif new_direction == "down":
        if direction != "up":
            direction = new_direction

window = Tk()
window.title("Snake Game")
window.resizable(False, False)

snake_head_image = load_and_resize_image("assets/iit_baba.png", SPACE_SIZE)
snake_body_image = load_and_resize_image("assets/degree.png", SPACE_SIZE // 2)
snake_tail_image = load_and_resize_image("assets/mic.png", SPACE_SIZE // 2)
food_image = load_and_resize_image("assets/weed.png", SPACE_SIZE)

score = 0
direction = "down"


label = Label(window, text="Score:{}".format(score))
label.pack()

canvas = Canvas(
    window, background=BACKGROUND_COLOR, height=CANVAS_HEIGHT, width=CANVAS_WIDTH
)
canvas.pack()
window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int(screen_width / 2 - window_width / 2)
y = int(screen_height / 2 - window_height / 2)

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

snake = Snake()
food = Food()
next_turn(snake, food)

def game_over():
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        text="GAME OVER",
        fill="red",
        tags="gameover",
    )

window.mainloop()