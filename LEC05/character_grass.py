from pico2d import *

open_canvas()
grass=load_image('grass.png')
character=load_image('character.png')

x=0

while x<800:
    clear_canvas()   #여기서부터 update_canvad까지 게임렌더링
    grass.draw(400,30)
    character.draw(x,90)
    update_canvas()
    x+=2  #game로직
    delay(0.01)

close_canvas()    