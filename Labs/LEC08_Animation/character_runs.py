from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('SamuraiSheet.png')

frame=0

#걷기
def walk_animation():
    print('걷기')
    global frame

for r in range(5):
    for frame in range(8):

      clear_canvas()
    
      character.clip_draw(frame*128,1024,128,128,400,300,170,170)
      frame=(frame+1)%8

      update_canvas()
      delay(0.05)
    pass

#달리기 
def run_animation():
    print('달리기')
    global frame

for r in range(5):
    for frame in range(8):

      clear_canvas()
    
      character.clip_draw(frame*128,1024,128,128,400,300,170,170)
      frame=(frame+1)%8

      update_canvas()
      delay(0.05)
    pass

#공격
def attack_animation():
    print('공격')
    global frame

for r in range(5):
    for frame in range(8):

      clear_canvas()
    
      character.clip_draw(frame*128,1024,128,128,400,300,170,170)
      frame=(frame+1)%8

      update_canvas()
      delay(0.05)
    pass

#점프
def jump_animation():
    print('점프')
    global frame

for r in range(5):
    for frame in range(8):

      clear_canvas()
    
      character.clip_draw(frame*128,1024,128,128,400,300,170,170)
      frame=(frame+1)%8

      update_canvas()
      delay(0.05)
    pass


while True:
    #walk_animation()
    #delay(1)

    #run_animation()
    #delay(1)

    jump_animation()
    #delay(1)

    #attack_animation()
    #delay(1)
    
close_canvas()

