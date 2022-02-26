import turtle
import time


class Score(turtle.Turtle):
    def __init__(self, shape: str, color: str, startx: int, starty: int) -> None:
        super().__init__(shape)
        self.speed(0)
        self.color(color)
        self.penup()
        self.hideturtle()
        self.goto(startx, starty)
        self.score_a = 0
        self.score_b = 0
        self.print_msg("score")

    def increment_score(self, player: str) -> None:
        if player=="a": self.score_a += 1
        if player=="b": self.score_b += 1

    def check_winner(self):
        if self.score_a == 10: return "Congratulations! Player A wins."
        if self.score_b == 10: return "Congratulations! Player B wins."
        return False # if there is no winner

    def print_msg(self, category: str, winner: str = ""):
        self.clear()
        if category == "score":
            self.write(f"Player A: {self.score_a} | Player B: {self.score_b}", align="center", font=("Courier", 24, "normal"))
        if category == "winner":
            self.write(winner, align="center", font = ("Courier", 24, "normal"))


class Paddle(turtle.Turtle):
    def __init__(self, shape: str, color: str, startx: int, starty: int, dx: int, dy: int) -> None:
        super().__init__(shape)
        self.speed(speed=0)  # Turn's off animations
        self.color(color)
        self.penup()
        self.goto(startx, starty)
        self.dx = dx
        self.dy = dy
        self.shapesize(5, 1)

    def moveup(self) -> None:
        y = self.ycor()
        y += self.dy
        if y > 250: self.sety(250)
        else: self.sety(y)
    
    def movedown(self) -> None:
        y = self.ycor()
        y -= self.dy
        if y < -250: self.sety(-250)
        else: self.sety(y)


class Ball(turtle.Turtle):
    def __init__(self, shape: str, color: str, startx: int, starty: int, dx, dy) -> None:
        super().__init__(shape)
        self.speed(0)
        self.color(color)
        self.penup()
        self.goto(startx, starty)
        self.dx = dx
        self.dy = dy
    
    def move(self):
        self.setx(self.xcor() + self.dx)
        self.sety(self.ycor() + self.dy)

    def invert_direction(self, step: str):
        if step == "dx": self.dx *= -1
        if step == "dy": self.dy *= -1

    def check_cor(self) -> None:
        if self.ycor() > 290:
            self.sety(290)
            self.invert_direction("dy")
        elif self.ycor() < -290:
            self.sety(-290)
            self.invert_direction("dy")
        if self.xcor() > 350:
            self.goto(0,0)
            self.invert_direction("dx")
            score.increment_score("a")
        elif self.xcor() < -350:
            self.goto(0,0)
            self.invert_direction("dx")
            score.increment_score("b")

wn = turtle.Screen()
wn.title("Pong")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

paddle_a = Paddle("square", "white", -350, 0, 0, 10)
paddle_b = Paddle("square", "white", 350, 0, 0, 10)
ball = Ball("square", "white", 0, 0, 5, 5)
score = Score("square", "white", 0, 260)

wn.listen()
wn.onkeypress(paddle_a.moveup, "w")
wn.onkeypress(paddle_a.movedown, "s")
wn.onkeypress(paddle_b.moveup, "Up")
wn.onkeypress(paddle_b.movedown, "Down")

while True:
    wn.update()
    ball.move()
    ball.check_cor()
    is_winner = score.check_winner()
    if is_winner:
        score.print_msg("winner", is_winner)
        time.sleep(10)
        break
    score.print_msg("score")
    if ball.xcor() < -340 and paddle_a.ycor() + 50 > ball.ycor() and ball.ycor() > paddle_a.ycor() - 50:
        ball.invert_direction('dx')
    elif ball.xcor() > 340 and paddle_b.ycor() + 50 > ball.ycor() and ball.ycor() > paddle_b.ycor() - 50:
        ball.invert_direction('dx')
    # due to lack of animation and inconsistency of CPU speed, we see the speed of pong/ball increasing/decreasing
    # to resolve this issue related to the pong/ball speed can be due to your CPU.
    time.sleep(1/60)