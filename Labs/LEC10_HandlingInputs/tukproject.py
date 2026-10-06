from pico2d import *

open_canvas()
TUK_GROUND = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')

running=True

def handle_events():

    global running,dir

    events=get_events()
    for event in events:
        if event.type==SDL_Quit:
            running=False
        elif event.type==SDL_KEYDOWN and event.key==SDLK_ESCAPE:
            running=False
    pass

while running:
    clear_canvas()
    TUK_GROUND.draw(400, 300)
    update_canvas()
    handle_events()
    delay(0.05)
    pass


close_canvas()