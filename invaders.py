

"""Este es un modulo
"""

import pygame
from colors import Colors

class Invader(pygame.sprite.Sprite):
    """ """

    __speed = 0
    __scale = (0, 0)
    __delta_x = 0
    __delta_y = 0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([20, 20])
        self.image.fill(Colors.GREEN)
        self.rect=self.image.get_rect()

    def update(self):
        self.rect.y += self.__delta_y
        self.rect.x += self.__delta_x


class SmallInvader(Invader):
    pass

class BigInvader(Invader):
    pass

class HugeInvader(Invader):
    pass