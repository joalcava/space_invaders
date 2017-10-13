#! /usr/bin/python3

"""Este es un modulo
"""

import pygame
import math
from colors import Colors

class Invader(pygame.sprite.Sprite):
    """ """

    __speed = 100
    __temp = 0
    __scale = (1, 1)
    __max_steps = 7
    __x_init = 10
    __y_init = 1
    __current_step = 0
    __steps_right = 1
    __steps_left = 1

    def __init__(self, pos, max_steps):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30, 10])
        self.image.fill(Colors.WHITE)
        self.rect = self.image.get_rect()
        self.__max_steps = max_steps
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.__x_init = pos[0]
        self.__y_init = pos[1]

    def update(self):
        if self.__temp == self.__speed:
            self.__temp = 0
            if self.__steps_right <= self.__max_steps:
                self.rect.x += 30
                self.__steps_right += 1
            elif self.__steps_left <= self.__max_steps:
                self.rect.x -= 30
                self.__steps_left += 1
            else:
                self.__steps_right = 1
                self.__steps_left = 1
                self.__temp = self.__speed
        else:
            self.__temp += 1


class SmallInvader(Invader):
    pass

class BigInvader(Invader):
    pass

class HugeInvader(Invader):
    pass