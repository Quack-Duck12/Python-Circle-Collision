import pygame as pg
from random import randint

from .utils import vector2
from .Objects import *

pg.init()

def Events(Obj_list: list['circle', 'static'], ActiveForce, FPS):

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
                for index, Obj in enumerate(Obj_list): 
                    if type(Obj) == static:
                        DeleteList.append(index)
                for index, ObjIndex in enumerate(DeleteList):
                    Obj_list.pop(ObjIndex - index)

            if event.key == pg.K_LEFT:
                print(True)
                ActiveForce = 1

            if event.key == pg.K_RIGHT:
                ActiveForce = -1

            if event.key == pg.K_DOWN:
                ActiveForce = 0

        if event.type == pg.MOUSEBUTTONDOWN:

            if event.button == 1:
                Obj_list = GatherAll(Obj_list, mousepos)

            if event.button == 6:
                ActiveForce = -1

            if event.button == 7:
                ActiveForce = 1
                
            if event.button == 3:
                mousepos = pg.mouse.get_pos()
                Static = static(vector2(mousepos[0], mousepos[1]), 1000, 15,)
                Obj_list.append(Static)

        if event.type == pg.MOUSEBUTTONUP:

            if event.button == 6 or event.button == 7:
                ActiveForce = 0 

        if event.type == pg.MOUSEWHEEL:
            if event.y > 0:
                FPS += 1
            if event.y < 0:
                FPS -= 1

    EventResoultion = (Obj_list, ActiveForce, FPS)
    
    return EventResoultion

    