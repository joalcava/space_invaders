#! /usr/bin/python3

import pygame
import random
from player import Player
from colors import Colors
from bullets import InvaderBullet, PlayerBullet
from invaders import Invader


class SpaceInvaders():

    WIDE = 800
    HEIGHT = 600
    SCREEN = None
    END = False
    EXIT = False

    def __init__(self):
        pygame.init()
        self.SCREEN = pygame.display.set_mode([self.WIDE, self.HEIGHT])
        self.SCREEN.fill(Colors.BLACK)

        self.gplayer = pygame.sprite.Group()
        self.ginvaders = pygame.sprite.Group()
        self.gbulletplayer = pygame.sprite.Group()
        self.gbulletinvaders = pygame.sprite.Group()

        self.player = Player(20, 10, self.WIDE)
        self.gplayer.add(self.player)
        pos = (10, 100)
        for i in range(10):
            pos = (pos[0]+60, pos[1])
            invader = Invader(pos, 4)
            self.ginvaders.add(invader)


    def start(self):
        self.player.rect.x = 100
        self.player.rect.y = 500
        self.__play_game()


    def __play_game(self):
        clock = pygame.time.Clock()
        last_bullet = PlayerBullet((self.WIDE, self.HEIGHT), (self.WIDE, self.HEIGHT))
        last_invader_bullet = InvaderBullet((self.WIDE, self.HEIGHT), (self.WIDE, self.HEIGHT))
        wait_time = None
        start = None
        while not self.END:
            
            if wait_time == None:
                wait_time = random.uniform(0.5, 2)
                start = pygame.time.get_ticks()
            elapsed_time = (pygame.time.get_ticks()-start)/1000
            if elapsed_time > wait_time:
                if len(self.ginvaders.sprites())-1  > 0:
                    rand = random.randint(0, len(self.ginvaders.sprites()) -1)
                    x_pos = self.ginvaders.sprites()[rand].rect.x
                    y_pos = self.ginvaders.sprites()[rand].rect.y
                    last_invader_bullet = InvaderBullet((x_pos, y_pos), (self.WIDE, self.HEIGHT))
                    self.gbulletinvaders.add(last_invader_bullet)
                    wait_time = None

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.player.move_right(2)
                    if event.key == pygame.K_LEFT:
                        self.player.move_left(2)
                    if event.key == pygame.K_SPACE:
                        pos = (self.player.rect.x, self.player.rect.y)
                        last_bullet = PlayerBullet(pos, (self.WIDE, self.HEIGHT))
                        self.gbulletplayer.add(last_bullet)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        self.player.step = 0
                if event.type == pygame.QUIT:
                    self.END = True

            # Colisiones
            cols1 = pygame.sprite.spritecollide(last_bullet, self.ginvaders, True)
            cols2 = pygame.sprite.spritecollide(last_invader_bullet, self.gplayer, False)
            for invader in cols1:
                invader.kill()
                last_bullet.kill()
            for i in cols2:
                print('you died')

            self.gplayer.update()
            self.gbulletplayer.update()
            self.gbulletinvaders.update()
            self.ginvaders.update()
            self.SCREEN.fill(Colors.BLACK)
            self.gplayer.draw(self.SCREEN)
            self.gbulletplayer.draw(self.SCREEN)
            self.gbulletinvaders.draw(self.SCREEN)
            self.ginvaders.draw(self.SCREEN)
            pygame.display.flip()
            clock.tick(60)


    def __play_menu(self):
        pass