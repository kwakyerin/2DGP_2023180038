# 실습 과제 진행
#고수는 함수 호출을 먼저 한다
import math

from pico2d import *

#맨 처음 해야할 일은
open_canvas(800,600)
character = load_image('character.png')

#캐릭터 그리기
def draw_character(x, y):
    clear_canvas()
    character.draw(x,y)
    update_canvas()
    delay(0.01)

#원 움직이기(원 운동)    
def move_circle():
    print("circle")
    # 캐릭터 이미지 표시

    for degree in range(360):
        theta=math.radians(degree)
        x=400+200*math.cos(theta)
        y=300+200*math.sin(theta)

        draw_character(x, y)
    pass

#윗변
def draw_top():
    print('top')
    for x in range(750,49,-5):
        draw_character(x,550)
    pass

#왼쪽변
def draw_left():
    print('left')
    for y in range(550,49,-5):
        draw_character(50,y)
    pass

#아랫변
def draw_bottom():
    print('bottom')
    for x in range(50,751,5):
        draw_character(x,50)
    pass

#오른쪽변
def draw_right():
    print('right')
    for y in range(50,551,5):
        draw_character(750,y)
    pass

#사각운동
def move_rectangle():
    print("rectangle")
    draw_top()
    draw_left()
    draw_bottom()
    draw_right()
    pass

#아래변(a에서 b)
def draw_triangle_one():
    print('one')
    for x in range(100,701,5):
        draw_character(x,100)
    pass

#오른쪽변(b에서 c)
def draw_triangle_two():
    print('two')

    x0,y0=700,100
    x1,y1=400,500

    n=100

    for step in range(n + 1):
        t = step / n
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t

        draw_character(x, y)
    pass

#왼쪽변(c에서 a)
def draw_triangle_three():
    print('three')

    x0,y0=400,500
    x1,y1=100,100

    n=100

    for step in range(n + 1):
        t = step / n
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t

        draw_character(x, y)
    pass

#삼각운동
def move_triangle():
    print("triangle")
    draw_triangle_one()
    draw_triangle_two()
    draw_triangle_three()
    pass

#세 운동 모두 반복(무한사이클)
while True:
    move_circle()
    move_rectangle()
    move_triangle()
