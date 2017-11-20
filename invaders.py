#! /usr/bin/python3

"""Este es un modulo
"""

import pygame

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

    steps = 32
    time = pygame.time.get_ticks()
    direction = 1
    current_image = 0
    speed = 650
    current_step = 0

    def __init__(self, _type, screen_pos, pos, can_shoot=False):
        pygame.sprite.Sprite.__init__(self)
        self.images = list()
        if _type == 1:
            self.images.append(pygame.transform.scale(IMAGES[11], (40, 35)))
            self.images.append(pygame.transform.scale(IMAGES[12], (40, 35)))
        elif _type == 2:
            self.images.append(pygame.transform.scale(IMAGES[21], (40, 35)))
            self.images.append(pygame.transform.scale(IMAGES[22], (40, 35)))
        elif _type == 3:
            self.images.append(pygame.transform.scale(IMAGES[31], (40, 35)))
            self.images.append(pygame.transform.scale(IMAGES[32], (40, 35)))

        self.image = self.images[Invader.current_image]
        self.rect = self.image.get_rect()
        self.rect.x = screen_pos[0]
        self.rect.y = screen_pos[1]
        self.is_front = can_shoot
        self.pos = pos
        self.is_right_border = False
        self.is_left_border = False

        if pos[1] == 1:
            self.is_left_border = True
        if pos[1] == 10:
            self.is_right_border = True

    def do_h_move(self):
        if Invader.direction > 0:
            self.rect.x += 10
        else:
            self.rect.x -= 10

    def do_v_move(self):
        self.rect.y += 40

    def update(self):
        self.image = self.images[self.current_image]
        if Invader.current_step < Invader.steps:
            self.do_h_move()
        else:
            self.do_v_move()
