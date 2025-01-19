import pygame as pg
from random import randint
from functools import cache

from scripts.display import *
from scripts.Objects import *
from scripts.utils import *
from scripts.events import *

class Program():

    def __init__(self, Balls: int):

        self.Balls = Balls
        self.SCREEN, self.SCREENSIZE = CreateDisplay()

        self.FPS = 60
        self.FPSCLOCK = pg.time.Clock()

        self.Obj_Set: set[circle, static] = set()

        self.VelocityLimit: int = 25
        self.MaxRadius: int = 15
        self.ActiveForce = 0

        self.GridSize = Grids(self)

        self.DoUpdate = True

        for _ in range(self.Balls):
            RandomMass = randint(5, 100)
            RandomRadius = randint(1, self.MaxRadius)
            RandomPosition = vector2(randint(0 + RandomRadius, self.SCREENSIZE[0] - RandomRadius),
                                    randint(0 + RandomRadius, self.SCREENSIZE[1] - RandomRadius))
            RandomVelocity = vector2(randint(self.VelocityLimit * -1, self.VelocityLimit), randint(self.VelocityLimit * -1, self.VelocityLimit))

            circle1 = circle(RandomPosition, RandomMass, RandomRadius, Velocity=RandomVelocity)
            self.Obj_Set.add(circle1)
        #self.Obj_Set.add(circle(vector2(self.SCREENSIZE[0] //2, self.SCREENSIZE[1]//2), Mass=5, Radius=10, Colour=(255,255,255), Velocity=vector2(0 , 0)))

    @cache
    def Run(self):

        global Program
        Program = self

        while True:

            delta = Program.FPSCLOCK.tick(Program.FPS)
            Program.SCREEN.fill("Black")

            Program.Obj_Set = Events(Program)

            if Program.ActiveForce != 0:
                ApplyActiveForce(Program, pg.mouse.get_pos())

            if Program.DoUpdate:
                for Obj in Program.Obj_Set:
                    Obj.MaxVelocity(Program.VelocityLimit)
                    Obj.Update(Program.SCREENSIZE)

                CollisionDetection(Program)
            draw(Program.SCREEN, Program.Obj_Set)

            DisplayMenu(Program.SCREEN, Program.FPS, Program.GridSize, Program.VelocityLimit, len(Program.Obj_Set), Program.ActiveForce, delta)

            pg.display.flip()

def main():
    Balls = int(input("Enter Number Of Circle TO Initilze with: "))
    Instance = Program(Balls)
    Instance.Run()

if __name__ == '__main__': main()
