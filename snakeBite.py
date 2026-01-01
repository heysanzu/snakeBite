import turtle
import time
import random

WIDTH, HEIGHT = 600, 600
DELAY = 0.1

screen = turtle.Screen()
screen.title("Snake Bite - by Sanzu")
screen.bgcolor("AliceBlue")
screen.setup(width=WIDTH, height=HEIGHT)
screen.tracer(0)

# Head
head = turtle.Turtle()
head.shape("square")
head.color("black")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Food
food = turtle.Turtle()
food.shape("circle")
food.color("blue")
food.penup()
food.goto(0, 100)

segments = []

# Score
score = 0
high_score = 0
pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.color("black")
pen.goto(0, HEIGHT//2 - 40)
pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Comic Sans MS", 18, "normal"))

# add credit
credit_pen = turtle.Turtle()
credit_pen.hideturtle()
credit_pen.penup()
credit_pen.color("black")
credit_pen.goto(0, -HEIGHT//2 + 20)
credit_pen.write("Made by Sanzu", align="center", font=("Comic Sans MS", 12, "normal"))

# Game over message
game_over_pen = turtle.Turtle()
game_over_pen.hideturtle()
game_over_pen.penup()
game_over_pen.color("blue")

game_active = True

def update_score():
    pen.clear()
    pen.goto(0, HEIGHT//2 - 40)
    pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Comic Sans MS", 18, "normal"))

def show_game_over():
    game_over_pen.goto(0, 0)
    game_over_pen.write("GAME OVER!\nPress SPACE to restart", align="center", font=("Comic Sans MS", 24, "bold"))

def hide_game_over():
    game_over_pen.clear()

def restart_game():
    global score, delay, game_active
    score = 0
    delay = DELAY
    head.goto(0, 0)
    head.direction = "stop"
    
    for seg in segments:
        seg.goto(1000, 1000)
    segments.clear()
    
    food.goto(0, 100)
    
    update_score()
    hide_game_over()
    game_active = True

def game_over():
    global game_active
    game_active = False
    time.sleep(0.5)
    head.goto(0, 0)
    head.direction = "stop"

    for seg in segments:
        seg.goto(1000, 1000)
    segments.clear()

    show_game_over()

def go_up():
    if head.direction != "down" and game_active:
        head.direction = "up"

def go_down():
    if head.direction != "up" and game_active:
        head.direction = "down"

def go_left():
    if head.direction != "right" and game_active:
        head.direction = "left"

def go_right():
    if head.direction != "left" and game_active:
        head.direction = "right"

def move():
    x, y = head.xcor(), head.ycor()
    if head.direction == "up":
        head.sety(y + 20)
    if head.direction == "down":
        head.sety(y - 20)
    if head.direction == "left":
        head.setx(x - 20)
    if head.direction == "right":
        head.setx(x + 20)

screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")
screen.onkey(go_right, "Right")
screen.onkey(go_up, "w")
screen.onkey(go_down, "s")
screen.onkey(go_left, "a")
screen.onkey(go_right, "d")
screen.onkey(restart_game, "space")

delay = DELAY

while True:
    screen.update()

    if not game_active:
        time.sleep(0.1)
        continue

    # Border collision
    if head.xcor() > WIDTH//2 - 10 or head.xcor() < -WIDTH//2 + 10 or head.ycor() > HEIGHT//2 - 10 or head.ycor() < -HEIGHT//2 + 10:
        game_over()
        continue

    # Food collision
    if head.distance(food) < 20:
        # move food to random spot
        x = random.randint(-WIDTH//2 + 20, WIDTH//2 - 20)
        y = random.randint(-HEIGHT//2 + 20, HEIGHT//2 - 20)
        food.goto(x - x % 20, y - y % 20)

        # add segment
        new_seg = turtle.Turtle()
        new_seg.shape("square")
        new_seg.color("black")
        new_seg.penup()
        segments.append(new_seg)

        score += 1
        if score > high_score:
            high_score = score
        update_score()

        # speed up
        delay = max(0.03, delay - 0.005)

    # Move segments
    for i in range(len(segments)-1, 0, -1):
        x = segments[i-1].xcor()
        y = segments[i-1].ycor()
        segments[i].goto(x, y)
    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    move()

    # Self collision
    for seg in segments:
        if seg.distance(head) < 20:
            game_over()
            break

    time.sleep(delay)

screen.mainloop()