import pygame as pg

pg.init()

def CreateDisplay():
    Info = pg.display.Info()
    SCREEN_SIZE: tuple = (Info.current_w, Info.current_h)
    #SCREEN_SIZE = (500,300)
    del Info

    Real_Screen = pg.display.set_mode(SCREEN_SIZE, vsync=True, flags=pg.RESIZABLE)

    return Real_Screen, SCREEN_SIZE

def DisplayMenu(Screen, FPS, GridSize, VelocityLimit, num_objects, ActiveForce):
    font = pg.font.Font(None, 40)
    menu_text = f"FPS: {FPS} | Grid Size: {GridSize} | Velocity Limit: {VelocityLimit} | Circles: {num_objects}"
    if ActiveForce in (1, -1): menu_text = menu_text + f" | ActiveForce: {ActiveForce}"
    text_surface = font.render(menu_text, True, (255, 255, 255))
    Screen.blit(text_surface, (10, 10))