from pico2d import *
import math

open_canvas()

grass = load_image('grass.png')
character = load_image('character.png')

c_x = 400
c_y = 300
radius = 200

angle = 0

while True:
    clear_canvas()

   #grass.draw(400, 30)

    x = c_x + radius * math.cos(math.radians(angle))
    y = c_y + radius * math.sin(math.radians(angle))
    character.draw(x, y)

    update_canvas()

    angle += 1
    if angle >= 360:
        angle = 0

    delay(0.01)

close_canvas()