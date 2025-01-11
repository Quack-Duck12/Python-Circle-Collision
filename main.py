import pygame as pg
from random import randint

from scripts.display import *
from scripts.Objects import *
from scripts.utils import *
from scripts.events import *

def main():
    Balls = int(input("Enter Number Of Balls To Initilize With: "))
    Real_Screen, SCREEN_SIZE = CreateDisplay()
    Loop(Real_Screen, SCREEN_SIZE, Balls)

def Loop(Screen, SCREEN_SIZE, Balls):
    FPS = 60
    FPSCLOCK = pg.time.Clock()

    Obj_list: list['circle', 'static'] = []

    Running: bool = True

    VelocityLimit: int = 50
    GridSize: int = 100  

    ActiveForce = 0

    for i in range(Balls):
        RandomMass = randint(5, 100)
        RandomRadius = randint(15, 30)
        RandomPosition = vector2(randint(0 + RandomRadius, SCREEN_SIZE[0] - RandomRadius),
                                 randint(0 + RandomRadius, SCREEN_SIZE[1] - RandomRadius))
        RandomVelocity = vector2(randint(-VelocityLimit, VelocityLimit), randint(-VelocityLimit, VelocityLimit))

        circle1 = circle(RandomPosition, RandomMass, RandomRadius, Velocity=RandomVelocity)
        Obj_list.append(circle1)

    while Running:

        FPSCLOCK.tick(FPS)
        Screen.fill("Black")

        Obj_list, ActiveForce, FPS = Events(Obj_list, ActiveForce, FPS)

        if ActiveForce != 0:
            ApplyActiveForce(ActiveForce, Obj_list, pg.mouse.get_pos())

        CollisionDetection(Obj_list, SCREEN_SIZE)
        for Obj in Obj_list:
            draw(Screen, Obj)
            Obj.Update(SCREEN_SIZE)

        DisplayMenu(Screen, FPS, GridSize, VelocityLimit, len(Obj_list), ActiveForce)

        pg.display.flip()

if __name__ == '__main__':
    main()
