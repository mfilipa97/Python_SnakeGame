from tkinter import *
import random

GAME_WIDTH = 800
GAME_HEIGHT = 600
INITIAL_SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
BACKGROUND_COLOR = "#000000"


class GameSnake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        self.color = SNAKE_COLOR

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=self.color, tag="snake")
            self.squares.append(square)

    def update_color(self, new_color): # Update the snake's color
        self.color = new_color
        for square in self.squares:
            canvas.itemconfig(square, fill=new_color)


class Food:
    def __init__(self):
        # Generates a random color for the food
        self.color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255),
                                                  random.randint(0, 255))

        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=self.color, tag="food")


def next_turn():
    global direction, snake, food, score, SPEED

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
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=snake.color, tag="snake")
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete("food")


        snake.update_color(food.color)

        food = Food()


        if score % 5 == 0:
            SPEED = max(50, SPEED - 5)
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn)


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

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():

    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=('Arial', 70), text="GAME OVER", fill="red", tag="gameover")


    restart_button = Button(window, text="Restart", font=('Arial', 20), command=restart_game)
    restart_button.place(relx=0.5, rely=0.9, anchor=CENTER)  # Center the button


def restart_game():
    global score, direction, snake, food, SPEED


    score = 0
    direction = "down"
    SPEED = INITIAL_SPEED
    label.config(text="Score: {}".format(score))


    canvas.delete("snake")
    canvas.delete("food")
    canvas.delete("gameover")


    for widget in window.winfo_children():
        if isinstance(widget, Button):
            widget.destroy()


    snake = GameSnake()
    food = Food()


    window.after(SPEED, next_turn)


window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = "down"
SPEED = INITIAL_SPEED
label = Label(window, text="Score: {}".format(score), font=("Arial", 20))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

snake = GameSnake()
food = Food()

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

window.after(SPEED, next_turn)
window.mainloop()