import tkinter as tk
import random

# Constants
WIDTH, HEIGHT = 600, 400
SNAKE_SIZE = 10
BASE_SPEED = 100  # Initial speed
SPEED_INCREMENT = 10  # Speed increase per food eaten

# Initialize variables
snake = [(50, 50), (40, 50), (30, 50)]
food = (200, 200)
direction = 'Right'
new_direction = ''
score = 0
speed = BASE_SPEED  # Initial speed

# Functions
def move():
    global direction, new_direction, snake, food, score, speed
    if new_direction:
        direction = new_direction

    # Move the snake
    head_x, head_y = snake[0]
    if direction == 'Right':
        new_head = (head_x + SNAKE_SIZE, head_y)
    elif direction == 'Left':
        new_head = (head_x - SNAKE_SIZE, head_y)
    elif direction == 'Up':
        new_head = (head_x, head_y - SNAKE_SIZE)
    elif direction == 'Down':
        new_head = (head_x, head_y + SNAKE_SIZE)

    snake = [new_head] + snake

    # Check for collisions
    if snake[0] == food:
        score += 10
        generate_food()
        speed -= SPEED_INCREMENT
    else:
        snake.pop()

    # Check for collisions with the wall
    if (
        snake[0][0] < 0
        or snake[0][0] >= WIDTH
        or snake[0][1] < 0
        or snake[0][1] >= HEIGHT
    ):
        game_over()
        return

    # Check for collisions with itself
    if len(snake) > 1 and snake[0] in snake[1:]:
        game_over()
        return

    canvas.delete('all')
    draw_snake()
    draw_food()
    draw_score()
    canvas.after(speed, move)

def draw_snake():
    for segment in snake:
        x, y = segment
        canvas.create_rectangle(
            x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill='green'
        )

def draw_food():
    x, y = food
    canvas.create_oval(
        x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill='red', outline='red'
    )

def draw_score():
    canvas.create_text(10, 10, text=f'Score: {score}', anchor='nw')

def generate_food():
    global food
    x = random.randint(0, (WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
    y = random.randint(0, (HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
    food = (x, y)

def on_key_press(event):
    global new_direction
    key = event.keysym
    if key in ('Right', 'Left', 'Up', 'Down'):
        if (
            (key == 'Right' and direction != 'Left')
            or (key == 'Left' and direction != 'Right')
            or (key == 'Up' and direction != 'Down')
            or (key == 'Down' and direction != 'Up')
        ):
            new_direction = key

def game_over():
    canvas.delete('all')
    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2,
        text=f'Game Over! Score: {score}',
        font=('Helvetica', 20),
        fill='red',
        anchor='center',
    )

# Create the main window
root = tk.Tk()
root.title('Snake Game')

# Create the canvas
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

# Bind key events
root.bind('<KeyPress>', on_key_press)

# Start the game
move()

root.mainloop()
