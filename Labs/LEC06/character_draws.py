# 실습 과제 진행
import math

from pico2d import *

#맨 처음 해야할 일은
open_canvas(800,600)
character = load_image('character.png')

def move_circle():
    print("circle")
    # 캐릭터 이미지 표시

    for degree in range(360):
        theta=math.radians(degree)
        x=400+200*math.cos(theta)
        y=300+200*math.sin(theta)

        clear_canvas()
        character.draw(x,y)
        update_canvas()
        delay(0.1)
    pass

def draw_top():
    print('top')
    pass

def draw_left():
    print('left')
    pass

def draw_bottom():
    print('bottom')
    pass

def draw_right():
    print('right')
    pass

#고수는 함수 호출을 먼저 한다
def move_rectangle():
    print("rectangle")
    draw_top()
    draw_left()
    draw_bottom()
    draw_right()
    pass

def move_triangle():
    print("triangle")
    pass

while True:
    move_circle()
    move_rectangle()
    move_triangle()
pass

delay(1)
close_canvas()