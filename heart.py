#! /usr/bin/python3

import pygame
from colors import Colors


class Heart(pygame.sprite.Sprite):
    
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = self.load_image("heart.png")
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def load_image(self, name, colorkey=None):
        image = pygame.image.load(name)
        image = image.convert_alpha()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()

