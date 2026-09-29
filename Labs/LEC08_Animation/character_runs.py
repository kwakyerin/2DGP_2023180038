from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('SamuraiSheet.png')

frame=0

#걷기 함수 추가
def walk_animation():
    print('걷기')
    pass

def run_animation():
    print('달리기')
    pass

def jump_animation():
    print('점프')
    pass

def attack_animation():
    print('공격')
    pass

for x in range(0, 800, 5):
    clear_canvas()
    grass.draw(400, 30)

    walk_animation()
    run_animation()
    jump_animation()
    attack_animation()

    update_canvas()
    
close_canvas()

