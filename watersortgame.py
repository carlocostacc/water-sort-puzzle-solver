import pygame as pg
from vile import Vile, colorselector
from settings import *
import os
import operator


class Water_sort(pg.sprite.Sprite):

    def __init__(self, numberofvilescounter, display):
        pg.sprite.Sprite.__init__(self)
        self.numberofvilesocunter = numberofvilescounter
        self.numberofviles = self.numberofvilesocunter.counter
        self.vilesarray = []
        self.color_sample_arr = []
        self.color_selected = 0
        self.mouse = (0, 0)
        for i in range(self.numberofviles):
            self.vilesarray.append(Vile(display))

        self.colordict = colordict
        self.display = display
# calculates the positions of the viles
    def vile_render(self, vilecounter ):
        (gapx, gapy) = (0, 0)
        buffer = vilecounter.endofselector(1) + 20
        height_buffer = vilecounter.endofselector(2) + 30
        temp_number_of_viles_in_a_row = self.numberofviles
        row = 1
        image = self.vilesarray[0].img

        gapx = (width - 2 * buffer) % (image.get_width() * temp_number_of_viles_in_a_row) // (
                temp_number_of_viles_in_a_row - 1)

        gapy = (height - 2 * height_buffer) % (image.get_height() * row) // row

        if buffer + gapx * temp_number_of_viles_in_a_row + temp_number_of_viles_in_a_row *\
                self.vilesarray[0].img.get_width() > width:
            temp_number_of_viles_in_a_row = temp_number_of_viles_in_a_row // 2
            row += 1

        pos = 0
        temprow = 0

        for x in self.vilesarray:

            if pos % temp_number_of_viles_in_a_row == 0:
                temprow += 1
                pos = 0

            x.img_rect.x = buffer + gapx * pos + pos * x.img.get_width()
            x.img_rect.y = height_buffer + gapy * temprow + temprow * x.img.get_height()
            pos += 1

# displays the viles on the screen
# TODO: the rendering of the viles should handeled in the vile class not in the game class
    def vile_display(self):
        for i in self.vilesarray:
            i.update()

    # render the colors you can use to set up the initial problem
    def render_color_palette(self):
        # take the information in the colorvalue dict and render the diffferent colors under the play button
        # the rectangles are too long and not enough space between them
        for color in colorvalues:
            pg.draw.rect(self.display, colorvalues[color], [(20 * color)*1.5 + 15, 70, 20, 20])
            if len(self.color_sample_arr) < 12:
                self.color_sample_arr.append([(20 * color)*1.5 + 15, 70, 20, 20])


    # lets you add colors to the viles to create the initial conditions of the problem
    def mouse_is_touching_the_rect(self, x, y, w, h):
        mousex, mousey = pg.mouse.get_pos()
        if x <= mousex <= x + w and y <= mousey <= y + h and pg.mouse.get_pressed(3) == (True, False, False):
            return True
        else:
            return False


    def search(self, target, list):
        for x in range(len(list)):
            if tuple(list[x]) == target:
                return x



    def first_color_setup(self):
        # must change the while to a while that will determine if the vile are in the setup phase or not
        # once the colors are displayed find a way to store the color selected
        self.render_color_palette()
        cond = False
        for x in self.color_sample_arr:
            (xz, y, w, h) = x
            if self.mouse_is_touching_the_rect(xz, y, w, h):
                self.color_selected = self.search((xz, y, w, h), self.color_sample_arr)
                cond = True

        self.display_selected_color(cond)
        # returns the position of the index of the color from the color dict
    def display_selected_color(self, condition):
        if condition:
            self.mouse_pos()

            pg.draw.rect(self.display, colorvalues[self.color_selected],
                         [self.mouse[0] - 10, self.mouse[1] - 10, 20, 20])

    def mouse_pos(self):
        self.mouse = pg.mouse.get_pos()
        print(self.mouse)

# to be worked on
    def colorselected(self):
        if self.colorselector.showColorchoice() != (0,0,0):
            color = self.colorselector.showColorchoice()
            while self.colorselector.isSelected():
                x, y = pg.mouse.get_pos()
                pg.draw.rect(self.display, color, (x, y, 20, 20))
                for vile in self.vilesarray:
                    if pg.mouse.get_pressed(3) == (True, False, False) and vile.img.collidepoint(pg.mouse.get_pos()):
                        vile.addcolor(color)
# not finished
    def add_color_to_vile(self, vile, color):
        for x in range(4):
            if self.vilesarray[vile, x] == 0:
                self.vilesarray[vile, x] = color
                break
            if x == 3 and self.vilesarray[vile, x] != 0:
                print("vile is full")

# checks if the vile is empty or not
# TODO : the watergame sort class should ask the vile class to return
#  a boolean value on weather the vile is empty or not
    def is_empty(self, vile):
        if vile.isEmpty():
            return True
        else:
            return False

# checks if the viles is full or not
# returns boolean

    def is_full(self, vile):
        if vile.isFull():
            return True
        else:
            return False


    def fill_vile(self, vile1, vile2):
        if self.is_empty(vile2):
            for c in range(3, 0, -1):
                if self.vilesarray[vile1, c] != 0:
                    self.vilesarray[vile2, 0] = self.vilesarray[vile1, c]
                    self.vilesarray[vile1, c] = 0
        elif self.is_full(vile2):
            print("vile is full")
        else:
            count = 1
            for x in range(4):
                if self.vilesarray[vile2, x] == 0:

                    # x is the first empty position of the target vile

                    for c in range(3, 0, -1):

                        # c is the color on top of the vile we are trying to pour

                        if self.vilesarray[vile1, c] != 0:
                            if self.vilesarray[vile2, x - 1] == self.vilesarray[vile1, c]:

                                # we need to know how many units of water we need to poor
                                # we can do a for loop to count the number of units of the same color there are

                                for d in range(c, 0, -1):
                                    if self.vilesarray[vile1, d] == self.vilesarray[vile1, c]:
                                        count = count + 1

                                # count variable is the number of units of liquid we can poor in vile 2
                                # we now need to know how many units of liquid we can actually poor in vile 2
                                # since we know the first position that is equal to 0 for vile2 we can do 4 - x

                                for z in range(4 - x):
                                    if z <= count:
                                        # we can not exeed the limit of count because count
                                        # represents the number of units of the same color in vile1

                                        self.vilesarray[vile2, x + z] = self.vilesarray[vile1, c - z]
                                        self.vilesarray[vile1, c - z] = 0
                                break
                    break

    def update(self, selector):
        self.vile_render(selector)
        self.vile_display()
        self.mouse_pos()

# =======================================================================
#                                SOLVER
# =======================================================================
# how to make the solver i have no idea