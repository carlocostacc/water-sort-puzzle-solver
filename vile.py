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
    def __init__(self, display):
        pg.sprite.Sprite.__init__(self)
        self.display = display
        self.image_size = 100, 170
        self.img = pg.image.load(os.path.join('images', 'vile.png')).convert_alpha()
        self.img = pg.transform.rotate(self.img, 90)
        self.img_clean = self.img
        self.img = pg.transform.scale(self.img_clean, self.image_size)
        self.img_rect = self.img.get_rect()
        self.colorarr = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        self.selected = False
        #42

    # thsi function takes a number 1 to 4 as argument and returns
    # the y values that corresponds to teh array of the vile
    def vile_seperation_heights(self,pos):
        if pos == 1:
            return self.img_rect.y + 3 * 42, self.img_rect.y + self.img.get_height()
        if pos == 2:
            return self.img_rect.y + 2 * 42, self.img_rect.y + 3 * 42
        if pos == 3:
            return self.img_rect.y + 42, self.img_rect.y + 2 * 42
        if pos == 4:
            return self.img_rect.y, self.img_rect.y + 42


    def part_of_vile_selected(self):
        if pg.mouse.get_pressed(3) == (True, False, False) and \
                self.img_rect.collidepoint(pg.mouse.get_pos()):
            if pg.mouse.get_pos().y > self.vile_seperation_heights(1)[0]\
                    and pg.mouse.get_pos() < self.vile_seperation_heights(1)[1]:
                return 1
            elif pg.mouse.get_pos().y > self.vile_seperation_heights(2)[0]\
                    and pg.mouse.get_pos() < self.vile_seperation_heights(2)[1]:
                return 2
            elif pg.mouse.get_pos().y > self.vile_seperation_heights(3)[0]\
                    and pg.mouse.get_pos() < self.vile_seperation_heights(3)[1]:
                return 3
            elif pg.mouse.get_pos().y > self.vile_seperation_heights(4)[0]\
                    and pg.mouse.get_pos() < self.vile_seperation_heights(4)[1]:
                return 4

# render the lines that seperates the different parts of the viles
# the lines have to be rectangle of width 1 because we can not change the alpha value of a line
    def vile_seperator(self):
        line = 1
        while line < 4:
            pg.draw.rect(self.display, (0, 0, 0),[self.img_rect.x + int(self.img.get_width()/3),
                                                  self.vile_seperation_heights(line)[0], self.img.get_width()/2.9, 1])
            line += 1

#  the isSelected function will highlight the vile that is currently selected
# will be used when transefering water in diffenent viles

    def IsSelected(self):
        if pg.mouse.get_pressed(3) == (True, False, False) and \
                self.img_rect.collidepoint(pg.mouse.get_pos()):
            self.selected = True

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
        print("x pos", self.img.get_rect())

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

#TODO : the functions render color pallet should be handeled by the watersort game class

# render the colors you can use to set up the initial problem
    def render_color_palette(self):

        pass
# lets you add colors to the viles to create the initial conditions of the problem

    def first_color_setup(self):
        self.render_color_palette()
        
        pass

# display the vile and the seperation lines
    def display_vile(self):
        self.img = pg.transform.smoothscale(self.img_clean, self.image_size)
        self.display.blit(self.img, (self.img_rect.x, self.img_rect.y))
        self.vile_seperator()

# TODO: render the seperation lines in the viles
    def update(self, *args, **kwargs):
        self.display_vile()
        # TODO : fix this line of code the getrect function returns 0 for x and y
        # self.img_rect = self.img.get_rect()




# TODO: render the selector
# TODO: make pop up for color selection
# TODO: store color the color selected
# TODO: pass the information to idk yet

class colorselector(pg.sprite.Sprite):
    def __init__(self, dict, display):
        pg.sprite.Sprite.__init__(self)
        self.image_size = 35, 35
        self.colorsamplesize = 20
        # distance from the other selection buttons
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
        self.showcolors = False
        self.close = False

    def isSelected(self):
        if pg.mouse.get_pressed(3) == (True, False, False) and \
                self.img_rect.collidepoint(pg.mouse.get_pos()):
            if not self.selected:
                self.showcolors = True
                self.showColorchoice()
                return True
            if self.selected:

                self.showcolors = False
                return False

    def exit(self):
        if pg.mouse.get_pressed(3) == (True, False, False) and \
                self.img_rect.collidepoint(pg.mouse.get_pos()):
                self.close = not self.close

    # this function shows the different colors you can chose from and returns the value of the color chosen
    # cant get the colors to stay displayed aka the while loop is not working
    # this function should return a number for to give to the vile class
    def showColorchoice(self):
        while self.showcolors:
            self.exit()
            loop = 1
            print(loop)
            pg.draw.rect(self.display, (0,0,0), (20, 20, self.colorsamplesize, self.colorsamplesize))
            for color in self.dict:
                # we have 10 colors so the angle between the each colors must be 36deg
                # figure out the triangle equation for different color placement
                # the pos value must be a rectangle value with the width and height
                # rect = (x,y,w,h)
                # x, y must be calculated but the w and h will remain the same always
                posx = self.img_rect.centerx + cos(self.teta * loop) * self.colorsampledistance
                posy = self.img_rect.centery + sin(self.teta * loop) * self.colorsampledistance
                rectangle = pg.draw.rect(self.display, color, (posx, posy, self.colorsamplesize, self.colorsamplesize))
                loop += 1


# finds the correct position for the render of the selector
# renders in the wrong posistion need to fix

    def selectorpos(self, counter):
        #         will take the position from the vile counter and put its self under the counter
        self.img_rect.x = counter.endofselector(1)
        self.img_rect.y = counter.endofselector(3)

# displays the selector

    def selector_render(self):
        self.display.blit(self.img,(self.img_rect.x, self.img_rect.y))

    def update(self, counter):
        self.selectorpos(counter)
        self.selector_render()
        self.isSelected()

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
            return self.select.selectrect.x + self.select.image.get_width()
        if axis == 2:
            return self.select.selectrect.y + self.select.image.get_height()
        if axis == 3:
            return self.select.selectrect.y
        else:
            print("invalid argument, has ot be 1 or 2")
            return 0

    def get_height(self):
        return 40

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
