import turtle as t

def move(x,y):
    t.penup()
    t.goto(x,y)
    t.pendown()

def draw_siot(x,y,starty,size):
    move(x,y)
    t.setheading(-120)
    t.forward(size * 1.2)
    t.penup()
    t.goto(x,y)
    t.pendown()
    t.setheading(-60)
    t.forward(size * 1.2)
    if (y < starty):
        return x + size * 2, starty
    else:
        return x, y

def draw_nieun(x,y,starty,size):
    move(x,y)
    t.setheading(-90)
    t.forward(size * 0.5)
    t.left(90)
    t.forward(size)
    if (y < starty):
        return x + size * 2, starty
    else:
        return x, y

def draw_digeud(x,y,starty,size):
    move(x + size * 0.8,y)
    t.setheading(180)
    t.forward(size * 1.2)
    t.left(90)
    t.forward(size)
    t.left(90)
    t.forward(size * 1.2)
    if (y < starty):
        return x + size * 2, starty
    else:
        return x, y

def draw_ieung(x,y,starty,size):
    move(x + size * 0.5,y)
    t.setheading(180)
    t.circle(50)
    if (y < starty):
        return x + size * 2, starty
    else:
        return x, y
    
def draw_ah(x,y,size):
    move(x + size, y)
    t.setheading(-90)
    t.forward(size * 1.5)
    t.left(180)
    t.forward(size * 0.7)
    t.setheading(0)
    t.forward(size)
    return y - size * 2
    
def draw_i(x,y,size):
    move(x + size * 1.2,y)
    t.setheading(-90)
    t.forward(size * 1.5)
    return y - size * 2

def draw_none(x, y,starty, size):
    if (y < starty):
        return x + size * 2, starty
    else:
        return x, y

x = -300
y = 200
starty = y
size = 100

x, y = draw_siot(x,y,starty,size)
y = draw_i(x,y,size)
x, y = draw_nieun(x,y,starty,size)
x, y = draw_digeud(x,y,starty,size)
y = draw_ah(x,y,size)
x, y = draw_none(x,y,starty, size)
x, y = draw_ieung(x,y,starty,size)
y = draw_i(x,y,size)
x, y = draw_nieun(x,y,starty,size)

t.exitonclick()
