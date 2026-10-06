from pico2d import *

open_canvas()
TUK_GROUND = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')

running=True

def handle_events():
    pass

while running:
    clear_canvas()
    TUK_GROUND.draw(400, 300)
    update_canvas()
    handle_events()
    delay(0.05)
    pass


close_canvas()