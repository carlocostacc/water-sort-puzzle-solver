import pygame as pg
from vile import Vile, number_of_vile_counter
from settings import *
import os
import operator


class Water_sort(pg.sprite.Sprite):

    def __init__(self, numberofviles):
        pg.sprite.Sprite.__init__(self)
        self.numberofviles = numberofviles
        self.vilesarray = []
        for i in range(numberofviles):
            self.vilesarray.append(Vile())

        self.colordict = {
            0: "empty",
            1: "red",
            2: "cyan",
            3: "purple",
            4: "orange",
            5: "grey",
            6: "pink",
            7: "green",
            8: "blue",
            9: "neon_green",
            10: "yellow"
        }

    def vile_render(self, vilecounter, display):
        (gapx, gapy) = (0,0)
        buffer = vilecounter.endofselector(1) + 20
        height_buffer = vilecounter.endofselector(2) + 30
        temp_number_of_viles_in_a_row = self.numberofviles
        row = 1
        image = self.vilesarray[0].img
        print((width - 2 * buffer) % (image.get_width()*temp_number_of_viles_in_a_row) // temp_number_of_viles_in_a_row - 1\
                > 30 * (temp_number_of_viles_in_a_row - 1))
        while (width - 2 * buffer) % (image.get_width()*temp_number_of_viles_in_a_row) // temp_number_of_viles_in_a_row - 1\
                > 30 * (temp_number_of_viles_in_a_row - 1):
            temp_number_of_viles_in_a_row //= 2
            row += 1

        gapx = (width - 2 * buffer) % (image.get_width() * temp_number_of_viles_in_a_row) // (
                temp_number_of_viles_in_a_row - 1)
        gapy = (height - 2 * height_buffer) % (image.get_height() * row) // row
        print(row)
        for y in range(row):
            for x in range(temp_number_of_viles_in_a_row):

                self.vilesarray[(y+1) * temp_number_of_viles_in_a_row + x].img_rect.x = buffer + gapx * x + x *\
                                                self.vilesarray[y * temp_number_of_viles_in_a_row + x].img.get_width()
                self.vilesarray[ (y+1) * temp_number_of_viles_in_a_row + x].img_rect.y = height_buffer + gapy * y +\
                                            y * self.vilesarray[y * temp_number_of_viles_in_a_row + x].img.get_height()
        if self.numberofviles%2==1 :
            self.vilesarray[]



    def add_color_to_vile(self,vile, color):
        for x in range(4):
            if self.vilesarray[vile, x] == 0:
                self.vilesarray[vile, x] = color
                break
            if x == 3 and self.vilesarray[vile, x] != 0:
                print("vile is full")


    def is_empty(self, vile):
        if self.vilesarray[vile, 0] == 0:
            return True
        else:
            return False


    def is_full(self, vile):
        if self.vilesarray[vile, 3] != 0:
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

    def update(self, display, selector):
        self.vile_render(selector, display)
        for i in self.vilesarray:
            i.img = pg.transform.smoothscale(i.img_clean, i.image_size)
            display.blit(i.img, (i.img_rect.x, i.img_rect.y))