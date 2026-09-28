import math
from pico2d import *

open_canvas(800, 600)
character = load_image('character.png')

def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.01)

def move_circle():
    print('circle')

    for degree in range(360):
        theta = math.radians(degree)

        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)

        draw_character(x, y)


def move_rectangle():
    print('rectangle')

    for x in range(750, 49, -5):
        draw_character(x, 550)

    for y in range(550, 49, -5):
        draw_character(50, y)

    for x in range(50, 751, 5):
        draw_character(x, 50)

    for y in range(50, 551, 5):
        draw_character(750, y)      


def move_triangle():
    for x in range(100, 701, 5):
        draw_character(x, 100)

    x0, y0 = 700, 100
    x1, y1 = 400, 500

    n = 100

    for step in range(n + 1):
        t = step / n

        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t

        draw_character(x, y)

    x0, y0 = 400, 500
    x1, y1 = 100, 100

    for step in range(n + 1):
        t = step / n

        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t

        draw_character(x, y)

while True:
    #move_circle()
    #move_rectangle()
    move_triangle()