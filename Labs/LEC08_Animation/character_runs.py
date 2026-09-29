from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('SamuraiSheet.png')

frame=0

#걷기
def walk_animation():
    print('걷기')
    global frame
    
    character.clip_draw(frame*128,1024,128,128,x,100)
    frame=(frame+1)%8
    pass

#달리기 
def run_animation():
    print('달리기')
    global frame
    
    character.clip_draw(frame*128,896,128,128,x,100)    
    frame=(frame+1)%8
    pass


def attack_animation():
    print('공격')
    global frame

    character.clip_draw(frame*128,512,128,128,x,100)
    frame=(frame+1)%8
    pass


def jump_animation():
    print('점프')
    global frame

    character.clip_draw(frame*128,768,128,128,x,100)
    frame=(frame+1)%8
    pass


for x in range(0, 800, 5):
    clear_canvas()
    grass.draw(400, 30)

    #walk_animation()
    #run_animation()
    #attack_animation()
    jump_animation()

    update_canvas()
    delay(0.05)
    
close_canvas()

