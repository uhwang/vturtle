import random
import math
from vturtle import *
import libvgl as vgl

device("vturtle.png")
#device("vturtle.pdf")
#device("vturtle.emf")
#device("vturtle.svg")

num_sides = 6
side_length = 70
angle = 360.0 / num_sides 
colors = ['red', 'purple', 'blue', 'green', 'orange', 'yellow']

subplot(4,2,1)
for _ in range(36):
    for _ in range(5):
        forward(200)
        right(144)
    right(10)

subplot(4,2,2)
teleport(-200,-200)
def sierpinski(order, size):
    if order == 0:
        for _ in range(3):
            forward(size)
            left(120)
    else:
        sierpinski(order-1, size/2)
        forward(size/2)
        sierpinski(order-1, size/2)
        backward(size/2)
        left(60)
        forward(size/2)
        right(60)
        sierpinski(order-1, size/2)
        left(60)
        backward(size/2)
        right(60)

sierpinski(5, 400)

subplot(4,2,3)
for x in range(200):
    pencolor(colors[x % 6])
    width(0.005)
    forward(x)
    left(59)

deg=20    
subplot(4,2,4)
for x in range(360//deg):
    circle(100)
    left(deg)

# https://pythonturtle.academy/star-fractal-with-python-and-turtle-tutorial-and-source-code/
    
subplot(4,2,5)
def star(x,y,length,penc,fillc):
    up()
    goto(x,y)
    seth(90)
    fd(length)
    seth(180+36/2)
    L = length*math.sin(36*math.pi/180)/math.sin(54*math.pi/180)
    seth(180+72)
    down()
    fillcolor(fillc)
    pencolor(penc)
    begin_fill()
    for _ in range(5):
        fd(L)
        right(72)
        fd(L)
        left(144)
    end_fill()
    
def star_fractal(x,y,length,penc,fillc,n):
    if n==0:
        star(x,y,length,penc,fillc)
        return
    length2 = length/(1+(math.sin(18*math.pi/180)+1)/math.sin(54*math.pi/180))
    L = length-length2-length2*math.sin(18*math.pi/180)/math.sin(54*math.pi/180)
    for i in range(5):
        star_fractal(x+math.cos((90+i*72)*math.pi/180)*(length-length2),
                    y+math.sin((90+i*72)*math.pi/180)*(length-length2),
                    length2,penc,fillc,n-1) 
star_fractal(0,0,200,'black','blue',3)    

subplot(4,2,6)

def fixed_tree(order, length, angle):
    global c_table
    if order > 0:
        pensize(0.001*length/5)
        pencolor(c_table[order-1])
        fd(length)
        if length <= 15:
            scale = random.random() 
            f_col = vgl.color.hsv(0, scale, 1)
            pencolor(f_col)
            fillcolor(f_col)
            symbol(size=scale*0.01)
        lt(angle)
        fixed_tree(order - 1, length*0.8, 20)
        rt(angle*2)
        fixed_tree(order - 1, length*0.8, 20)
        lt(angle)
        pu()
        fd(-length)
        pd()
        
def draw():
    global c_table
    order = 10
    length = 100
    c_table = vgl.create_color_table(0,240, 0.8, 1, order)
    teleport(0,-200)
    left(90)
    fixed_tree(order, length, 0)

draw()   

subplot(4,2,7)
def draw_fractal_polygon(nvert, edge, level):
    if level > 0:
        ddeg = 360/nvert
        for _ in range(nvert):
            pencolor(colors[level%6])
            pensize(0.001*edge/4)
            fd(edge)
            draw_fractal_polygon(nvert, edge*0.5, level-1)
            bk(edge)
            right(ddeg)
        
def fractal_polygon():
    level =4
    left(90)
    draw_fractal_polygon(5, 130, level)

fractal_polygon()  

subplot(4,2,8)
def draw_hexgram_fractal(nvert, edge, level, dist):
    if level > 0:
        #pensize(0.001*edge/4)
        for i in range(nvert):
            fillcolor('cyan')
            symbol('*7:0.6',size=0.05)
            #pencolor(colors[i])
            rt(120)
            fd(edge)
            fillcolor('yellow')
            symbol('+',size=0.05)
            lt(60)
            fd(edge)
        
def hexagram_fractal():
    dist, edge = 200, 100
    teleport(0,dist)
    left(60)
    draw_hexgram_fractal(6, edge, 1, dist)

hexagram_fractal()  