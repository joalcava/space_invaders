#! /usr/bin/python3

import pygame
from colors import Colors

class InvaderBullet(pygame.sprite.Sprite):
    
    def __init__(self, pos, screen_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([4, 15])
        self.image.fill(Colors.WHITE)
        self.rect = self.image.get_rect()
        self.screen_h = screen_size[1]
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = 9

    def update(self):
        if self.rect.y < self.screen_h:
            self.rect.y += self.speed
        else:
            self.kill()

class PlayerBullet(pygame.sprite.Sprite):

    def __init__(self, pos, screen_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([4, 15])
        self.image.fill(Colors.GREEN)
        self.rect = self.image.get_rect()
        self.screen_h = screen_size
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = 9

    def update(self):
        if self.rect.y > 0:
            self.rect.y -= self.speed
        else:
            self.kill()
