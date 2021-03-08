import pygame as pg
import sys
from vile import *
from settings import *
from watersortgame import Water_sort
pg.init()
screen = pg.display.set_mode((size), pg.RESIZABLE)
numberofvilescounter = number_of_vile_counter()
numberofvilescounter.setpos((60, 20))
initialized = False



while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()
        screen.fill(white)
        numberofvilescounter.update(screen)


        if play:
            if numberofvilescounter.isselected():
                initialized = True
                numberofviles = numberofvilescounter.counter
                game = Water_sort(numberofviles)

            if initialized:
                game.update(screen, numberofvilescounter)
    pg.display.flip()
e = "WHENTHERESNOTHINGTOPLAYCODEPYTHON"
print(len(e))
# WHEN THERE'S NOTHING TO PLAY, CODE PYTHON
# FINAL EASTER EGG