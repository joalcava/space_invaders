#! /usr/bin/python3

import pygame
import random
import time
from player import Player
from colors import Colors
from bullets import InvaderBullet, PlayerBullet
from invaders import Invader
from heart import Heart


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

    def start(self):
        self.__play_menu()

    def __play_game(self):
        self.glives = pygame.sprite.Group()
        self.gplayer = pygame.sprite.Group()
        self.ginvaders = pygame.sprite.Group()
        self.gbulletplayer = pygame.sprite.Group()
        self.gbulletinvaders = pygame.sprite.Group()

        self.player = Player(20, 10, self.WIDE)
        self.gplayer.add(self.player)
        pos_a = 50
        for y in range(3):
            self.glives.add(Heart((pos_a, self.HEIGHT - (self.HEIGHT * 0.07))))
            pos_a += 50
        pos_b = (10, 100)
        for i in range(10):
            pos_b = (pos_b[0]+60, pos_b[1])
            invader = Invader(pos_b, 4)
            self.ginvaders.add(invader)
        self.player.rect.x = 100
        self.player.rect.y = 500
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
                if len(self.ginvaders.sprites()) > 0:
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
                    return;

            # Colisiones
            cols1 = pygame.sprite.groupcollide(self.gbulletplayer, self.ginvaders, False, True).keys()
            cols2 = pygame.sprite.spritecollide(self.player, self.gbulletinvaders, True)
            for invader in cols1:
                invader.kill()
                last_bullet.kill()

            if len(cols2) > 0:
                self.glives.sprites()[-1].kill()
                if len(self.glives.sprites()) == 0:
                    self.END = True

            self.gplayer.update()
            self.gbulletplayer.update()
            self.gbulletinvaders.update()
            self.ginvaders.update()
            self.SCREEN.fill(Colors.BLACK)
            self.glives.draw(self.SCREEN)
            self.gplayer.draw(self.SCREEN)
            self.gbulletplayer.draw(self.SCREEN)
            self.gbulletinvaders.draw(self.SCREEN)
            self.ginvaders.draw(self.SCREEN)
            pygame.draw.line(self.SCREEN, Colors.WHITE, (0, self.HEIGHT - (self.HEIGHT * 0.1)), (self.WIDE, self.HEIGHT - (self.HEIGHT * 0.1))) 
            pygame.display.flip()
            clock.tick(60)
        return self.__you_died()

    def __you_died(self):
        self.SCREEN.fill(Colors.BLACK)
        font = pygame.font.Font(None, 36)
        text = font.render("Perdiste", 1, Colors.RED)
        textpos = text.get_rect(centerx = self.WIDE/2)
        textpos.y = self.HEIGHT/2
        self.SCREEN.blit(text, textpos)
        pygame.display.flip()
        time.sleep(3)
        self.END = False
        return self.__play_menu()

    def __play_menu(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return self.__play_game()
                if event.type == pygame.QUIT:
                    return;
            self.SCREEN.fill(Colors.BLACK)
            font = pygame.font.Font(None, 36)
            text = font.render("Bienvenido", 1, Colors.WHITE)
            textpos = text.get_rect(centerx = self.WIDE/2)
            textpos.y = 100
            self.SCREEN.blit(text, textpos)
            text2 = font.render("Enter para empezar", 1, Colors.GREEN)
            textpos2 = text.get_rect()
            textpos2.x = 280
            textpos2.y = 300
            self.SCREEN.blit(text2, textpos2)
            pygame.display.flip()
            clock.tick(60)
