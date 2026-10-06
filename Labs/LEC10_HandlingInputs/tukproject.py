from pico2d import *

open_canvas()

TUK_GROUND = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')

running = True
x = 800 // 2
frame = 0
dir=0

def handle_events():
    global running,dir

    global x

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            running = False

        elif event.type==SDL_KEYDOWN:
                    if event.key==SDLK_RIGHT:
                        dir+=1
                    elif event.key==SDLK_LEFT:
                        dir-=1
                    elif event.key==SDLK_ESCAPE:
                        running=False
        elif event.type==SDL_KEYUP:
                    pass                  


while running:
    clear_canvas()
    TUK_GROUND.draw(400, 300)
    character.clip_draw(frame*100,100,100,100,x,90)
    update_canvas()
    handle_events()
    frame = (frame + 1) % 8
    x+=dir*5
    delay(0.05)

close_canvas()