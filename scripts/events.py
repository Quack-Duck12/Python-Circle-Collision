import pygame as pg
from random import randint

from .utils import vector2
from .Objects import *

pg.init()

def Events(Program):

    mousepos = pg.mouse.get_pos()

    for event in pg.event.get():

        if event.type == pg.QUIT:
            pg.quit()
            exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                exit()

            if event.key == pg.K_TAB:
                DeleteList = list()
                for Obj in Program.Obj_Set: 
                    if type(Obj) == static:
                        DeleteList.append(Obj)
                for Obj in DeleteList:
                    Program.Obj_Set.remove(Obj)

            if event.key == pg.K_LEFT:
                Program.ActiveForce = 1

            if event.key == pg.K_RIGHT:
                Program.ActiveForce = -1

            if event.key == pg.K_DOWN:
                Program.ActiveForce = 0

            if event.key == pg.K_a:
                Program.VelocityLimit += 5
            if event.key == pg.K_d:
                Program.VelocityLimit -= 5
            if event.key == pg.K_SPACE:
                Program.DoUpdate = not Program.DoUpdate


        if event.type == pg.MOUSEBUTTONDOWN:

            if event.button == 1:
                GatherAll(Program, mousepos)

            if event.button == 6:
                Program.ActiveForce = -1

            if event.button == 7:
                Program.ActiveForce = 1
                
            if event.button == 3:
                mousepos = pg.mouse.get_pos()
                Static = static(vector2(mousepos[0], mousepos[1]), 1000, 15,)
                Program.Obj_Set.add(Static)

        if event.type == pg.MOUSEBUTTONUP:

            if event.button == 6 or event.button == 7:
                Program.ActiveForce = 0 

        if event.type == pg.MOUSEWHEEL:
            if event.y > 0:
                Program.FPS += 1
            if event.y < 0:
                Program.FPS -= 1
    
        if event.type == pg.VIDEORESIZE:
            from .utils import Grids
            Program.SCREEN = pg.display.set_mode(size=(event.w, event.h), flags=pg.RESIZABLE)
            Program.SCREENSIZE = (event.w, event.h)
            Program.GridSize, Program.InitilizedDict = Grids(Program)

    return Program.Obj_Set