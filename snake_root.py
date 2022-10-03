from tkinter import *
from random import randint

BG_COLOR = 'black'
BG_WIDTH = 900
BG_HEIGHT = 600
GAME_SPEED = 100
SPACE_SIZE = 50
SNAKE_COLOR = 'green'
BODY_PARTS = 3
FOOD_COLOR = 'red'
SCORE = 0


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag='snake')
            self.squares.append(square)


class Food:
    def __init__(self):

        x = randint(0, int(BG_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = randint(0, int(BG_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag='food')


def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == 'up':
        y -= SPACE_SIZE
    elif direction == 'down':
        y += SPACE_SIZE
    elif direction == 'left':
        x -= SPACE_SIZE
    elif direction == 'right':
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global SCORE
        SCORE += 1

        score_label.config(text='Score:{}'.format(SCORE))

        canvas.delete('food')

        food = Food()

    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        root.after(GAME_SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction

    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction

    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction

    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= BG_WIDTH:
        return True

    elif y < 0 or y >= BG_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)

    canvas.create_text(
        canvas.winfo_width() / 2, canvas.winfo_height() / 2,
            font=('consolas', 70), text='Game Over', fill='red', tag='gameover'
    )


root = Tk()
root.title('Snake Game')
root.resizable(False, False)

score_label = Label(root, text=f'Score: {SCORE}', font=('consolas', 30))
score_label.pack()

canvas = Canvas(root, width=BG_WIDTH, height=BG_HEIGHT, bg=BG_COLOR)
canvas.pack()


root.update()

root_width = root.winfo_width()
root_height = root.winfo_height()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = int((screen_width / 2) - (root_width / 2))
y = int((screen_height / 2) - (root_height / 2))

root.geometry(f"{BG_WIDTH}x{BG_HEIGHT}+{x}+{y}")

root.bind('<Left>', lambda event: change_direction('left'))
root.bind('<Right>', lambda event: change_direction('right'))
root.bind('<Up>', lambda event: change_direction('up'))
root.bind('<Down>', lambda event: change_direction('down'))


direction = 'down'

snake = Snake()
food = Food()

next_turn(snake, food)

root.mainloop()
