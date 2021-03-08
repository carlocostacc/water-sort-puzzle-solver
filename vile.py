# to change the color of the vile selection use the dectionnary to output tuple
# the tuple output is used to render the rectangles for the color selector
# use tuple to do color cursor
# the output selection interface shows the different available colors ina  circlce
# the action of clicking on the colored square selects the color
# to be put in the different viles
# this is the function of the vile selector
# wait for an input of the user to say that the selection and position of the colors of the viles
# check if only 2 viles are empty
# if less say we need at least 2
# to remember to add animations for the openeing and closing of the color selector


import pygame as pg
import os
import operator
from math import cos, sin
from pygame.locals import *




class Vile(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_size = 100, 170
        self.img = pg.image.load(os.path.join('images', 'vile.png')).convert_alpha()
        self.img = pg.transform.rotate(self.img, 90)
        self.img_clean = self.img
        self.img = pg.transform.scale(self.img_clean, self.image_size)
        self.img_rect = self.img.get_rect()
        self.colorarr = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]

    def isEmpty(self):
        if self.colorarr[0] == (0, 0, 0):
            return True
        else:
            return False

    def isFull(self):
        if self.colorarr[3] != 0:
            return True
        else:
            return False

    def vile_draw(self, position):
        self.img.rect = position

    def addcolor(self, color):
        if self.isFull():
            print("cant add color vile is full")
        else:
            pos = 0
            for x in self.colorarr:
                if x == (0, 0, 0):
                    self.colorarr[pos] = color
                    break
                pos += 1



class colorselector(pg.sprite.Sprite):
    def __init__(self, dict, display):
        pg.sprite.Sprite.__init__(self, dict, display)
        self.image_size = 30, 30
        self.colorsamplesize = 20
        self.colorsampledistance = 40
        self.display = display
        self.img = pg.image.load(os.path.join('images', 'selector.png')).convert_alpha()
        self.img_clean = self.img
        self.img = pg.transform.scale(self.img_clean, self.image_size)
        self.img_rect = self.img.get_rect()
        self.dict = dict
        self.selected = False
        self.selectedcolor = 0
        self.teta = 36

    def isSelected(self):
        if pg.mouse.get_pressed(3) == (True, False, False) and \
                self.img_rect.collidepoint(pg.mouse.get_pos()):
            if not self.selected:
                self.selected = True
                return True
            else:
                self.selected = False
                return False

    # this function shows the different colors you can chose from and returns the value of the color chosen
    def showColorchoice(self):
        if self.isSelected():
            loop = 1
            for color in self.dict:
                #           we have 10 colors so the angle between the each colors must be 36deg
                #           figure out the triangle equation for different color placement
                #           the pos value must be a rectangle value with the width and height
                #           rect = (x,y,w,h)
                #           x, y must be calculated but the w and h will remain the same always
                posx = self.img_rect.centerx + cos(self.teta * loop) * self.colorsampledistance
                posy = self.img_rect.centery + sin(self.teta * loop) * self.colorsampledistance
                rectangle = pg.draw.rect(self.display, color, (posx, posy, self.colorsamplesize, self.colorsamplesize))
                loop += 1
                if pg.mouse.get_pressed(3) == (True, False, False) and \
                        rectangle.collidepoint(pg.mouse.get_pos()):
                    return color
                else:
                    return (0, 0, 0)

    def selectorpos(self, counter):
        #         will take the position from the vile counter and put its self under the counter
        self.img_rect.x = counter.x
        self.img_rect.y = counter.y + counter.get_height() + 50

    def update(self, counter):
        self.selectorpos(counter)
        self.showColorchoice()


class number_of_vile_counter(pg.sprite.Sprite):
    def __init__(self):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (58, 255, 58)
        pg.sprite.Sprite.__init__(self)

        class Selector(pg.sprite.Sprite):
            def __init__(self):
                pg.sprite.Sprite.__init__(self)
                self.selectbuttonsize = (20, 20)
                self.selected = False
                self.image = pg.image.load(os.path.join('images', 'select.png')).convert_alpha()
                self.image_clean = self.image.copy()
                self.image = pg.transform.smoothscale(self.image_clean, self.selectbuttonsize)
                self.selectrect = self.image.get_rect()

        self.select = Selector()

        self.arrowsize = (30, 20)
        self.arrowup = pg.image.load(os.path.join('images', 'arrow_up.png')).convert()
        self.arrowdown = pg.image.load(os.path.join('images', 'arrow_up.png')).convert()
        self.arrowdown = pg.transform.rotate(self.arrowup, 180)
        self.arrowup = pg.transform.smoothscale(self.arrowup, self.arrowsize)
        self.arrowdown = pg.transform.smoothscale(self.arrowdown, self.arrowsize)
        self.arrowup_rect = self.arrowup.get_rect()
        self.arrowdown_rect = self.arrowdown.get_rect()
        self.counter = 0
        self.font = pg.font.Font('freesansbold.ttf', 30)
        self.text = self.font.render(str(self.counter), True, self.black, self.green)
        self.textrect = self.text.get_rect()

    def endofselector(self, axis):
        if axis == 1:
            return self.select.image.get_rect().x + self.select.image.get_width()
        if axis == 2:
            return self.select.image.get_rect().y + self.select.image.get_height()
        else:
            print("invalid argument, has ot be 1 or 2")
            return 0

    def setpos(self, pos):
        self.textrect.x, self.textrect.y = pos
        end_of_text_box = self.textrect.x + self.text.get_width(), \
                          self.textrect.y
        end_of_arrow_up = self.arrowup.get_size()
        final = tuple(map(operator.add, end_of_arrow_up, end_of_text_box))
        final = tuple(map(operator.sub, final, (self.arrowup.get_width(), 0)))
        self.arrowup_rect.x, self.arrowup_rect.y = end_of_text_box
        self.arrowdown_rect.x, self.arrowdown_rect.y = final
        self.select.selectbuttonsize = 2 * self.arrowup.get_height(), 2 * self.arrowup.get_height()
        self.select.image = pg.transform.smoothscale(self.select.image_clean, self.select.selectbuttonsize)
        self.select.selectrect = self.select.image.get_rect()
        self.select.selectrect.x = self.arrowup_rect.x + 20
        self.select.selectrect.y = self.arrowup_rect.y

    def getarrowsize(self):
        textboxdim = self.text.get_height()
        self.arrowsize = int(textboxdim / 2 * 4 / 3), int(textboxdim / 2)
        self.arrowup = pg.transform.smoothscale(self.arrowup, self.arrowsize)
        self.arrowdown = pg.transform.smoothscale(self.arrowdown, self.arrowsize)

    def repositiontextbox(self):
        self.textrect.x = self.arrowup_rect.x - self.text.get_width()

    def isselected(self):

        if pg.mouse.get_pressed(3) == (True, False, False) and \
                self.select.selectrect.collidepoint(pg.mouse.get_pos()):
            if self.counter > 2:
                if self.select.selected == False:
                    self.select.selected = True
                    print(self.select.selected)
                    return True
                else:
                    self.select.selected = False
                    print(self.select.selected)
                    return False
            else:
                print("have to select more than 2")

    def counter_conrol(self):
        # check if the mouse has clicked on the up arrow or the down arrow
        # if clicked on up increment counter and add a vile
        if pg.mouse.get_pressed(3) == (True, False, False) and self.arrowup_rect.collidepoint(pg.mouse.get_pos()):
            self.counter = self.counter + 1

        if pg.mouse.get_pressed(3) == (True, False, False) and self.arrowdown_rect.collidepoint(pg.mouse.get_pos()):
            self.counter = self.counter - 1
            if self.counter < 0:
                self.counter = 0

    def update(self, display):
        self.counter_conrol()
        self.repositiontextbox()
        self.getarrowsize()
        self.text = self.font.render(str(self.counter), True, self.black, self.green)
        display.blit(self.text, self.textrect)
        display.blit(self.arrowup, self.arrowup_rect)
        display.blit(self.arrowdown, self.arrowdown_rect)
        display.blit(self.select.image, self.select.selectrect)
