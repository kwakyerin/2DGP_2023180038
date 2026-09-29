from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('SamuraiSheet.png')

frame=0

for x in range(0, 800, 5):
    clear_canvas()
    grass.draw(400, 30)
    update_canvas()
    
close_canvas()

