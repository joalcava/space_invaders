#! /usr/bin/python3

"""Este es un modulo
"""

import pygame
import math
from colors import Colors
IMAGES = {
        11: pygame.image.load('invader1.1.png').convert_alpha(),
        12: pygame.image.load('invader1.2.png').convert_alpha(),
        21: pygame.image.load('invader2.1.png').convert_alpha(),
        22: pygame.image.load('invader2.2.png').convert_alpha(),
        31: pygame.image.load('invader3.1.png').convert_alpha(),
        32: pygame.image.load('invader3.2.png').convert_alpha()
    }

class Invader(pygame.sprite.Sprite):
    """ """

    speed = 700
    current_step = 0
    steps = 20
    time = pygame.time.get_ticks()
    direction = 1
    current_image = 0


    def __init__(self, t, pos, is_corner = False, is_front = False):
        pygame.sprite.Sprite.__init__(self)
        self.images = list()
        if t == 1:
            self.images.append(pygame.transform.scale(IMAGES[11], (40, 35)))
            self.images.append(pygame.transform.scale(IMAGES[12], (40, 35)))
        elif t == 2:
            self.images.append(pygame.transform.scale(IMAGES[21], (40, 35)))
            self.images.append(pygame.transform.scale(IMAGES[22], (40, 35)))
        elif t == 3:
            self.images.append(pygame.transform.scale(IMAGES[31], (40, 35)))
            self.images.append(pygame.transform.scale(IMAGES[32], (40, 35)))

        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.is_corner = is_corner
        self.is_front = is_front
        
    def do_h_move(self):
        if self.direction > 0:
            self.rect.x += 15
        else:
            self.rect.x -= 15
        self.current_step += 1
        self.current_image = int(not(bool(self.current_image)))

    def do_v_move(self):
        self.rect.y += 35
        self.current_step = 1
        self.direction = self.direction * -1
        self.current_image = int(not(bool(self.current_image)))

    def update(self, current_time):
        if current_time - self.time > self.speed:
            self.time = pygame.time.get_ticks()
            self.image = self.images[self.current_image]
            if self.current_step < self.steps:
                self.do_h_move()
            else:
                self.do_v_move()