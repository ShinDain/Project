import turtle as t

size = 20
width = 5
floor = 5

x = 0
y = 0

def draw_sqaure():
    t.setheading(0)
    for i in range(1,4 + 1):
        t.forward(size)
        t.left(90)

def move(x,y):
    t.penup()
    t.goto(x,y)
    t.pendown()

t.speed(0)

count = 0
for i in range(1, floor + 1):
    for i in range(1, width + 1):
        move(count * size + x, y)
        draw_sqaure()
        count += 1
    y += size
    count = 0
    

t.exitonclick()
