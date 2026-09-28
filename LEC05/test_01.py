from pico2d import *

open_canvas()

character = load_image('character.png')

x = 20
y = 40

while True:

    while x < 500:
        clear_canvas()
        character.draw(x, y)
        update_canvas()

        x += 2
        delay(0.01)

    while y < 400:
        clear_canvas()
        character.draw(x, y)
        update_canvas()

        y += 2
        delay(0.01)

    while x > 20:
        clear_canvas()
        character.draw(x, y)
        update_canvas()

        x -= 2
        delay(0.01)

    while y > 40:
        clear_canvas()
        character.draw(x, y)
        update_canvas()

        y -= 2
        delay(0.01)

close_canvas()