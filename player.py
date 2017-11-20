#! /usr/bin/python3

import pygame
from colors import Colors

player_img = pygame.image.load('player.png').convert_alpha()


class Player(pygame.sprite.Sprite):
    
    def __init__(self, screen_wide):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (35, 30))
        self.rect = self.image.get_rect()
        self.screen_wide = screen_wide
        self.step = 0

    def move_left(self, step):
        self.step = -step

    def move_right(self, step):
        self.step = step
    
    def update(self):
        if self.rect.x < 10:
            self.rect.x = 10
        elif self.rect.x > self.screen_wide-10:
            self.rect.x = self.screen_wide-10
        else:
            self.rect.x += self.step
