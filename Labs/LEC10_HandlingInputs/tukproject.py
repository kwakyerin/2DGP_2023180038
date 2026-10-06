from pico2d import *

open_canvas()
TUK_GROUND = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')

running=True

def handle_events():

    global running,dir

    event = get_events()
    if event.type == SDL_QUIT:
        running=False
    elif event.type==SDL_KEYDOWN:
        pass
    elif event.type==SDL_KEYUP:
        pass

dir=0

while running:
    clear_canvas()
    TUK_GROUND.draw(400, 300)
    update_canvas()
    handle_events()
    delay(0.05)

close_canvas()