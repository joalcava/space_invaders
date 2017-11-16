#! /usr/bin/python3

import random
import time
import pygame
pygame.display.set_mode((800,600))

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
        # Groups
        g_lives = pygame.sprite.Group()
        g_player = pygame.sprite.Group()
        g_allinvaders = pygame.sprite.Group()
        g_bulletplayer = pygame.sprite.Group()
        g_bulletinvaders = pygame.sprite.Group()

        #Player
        player = Player(20, 10, self.WIDE)
        player.rect.x = 100
        player.rect.y = 500
        g_player.add(player)

        # Lives
        pos = 50
        for i in range(3):
            g_lives.add(Heart((pos, self.HEIGHT - (self.HEIGHT * 0.07))))
            pos += 50

        # Invaders line 1
        pos = (0, 10)
        for i in range(10):
            invader = Invader(1, pos)
            pos = (pos[0]+50, pos[1])
            g_allinvaders.add(invader)

        # Invaders line 2
        pos = (0, 50)
        for i in range(10):
            invader = Invader(2, pos)
            pos = (pos[0]+50, pos[1])
            g_allinvaders.add(invader)

        # Invaders line 3
        pos = (0, 90)
        for i in range(10):
            invader = Invader(2, pos)
            pos = (pos[0]+50, pos[1])
            g_allinvaders.add(invader)

        # Invaders line 4
        pos = (0, 130)
        for i in range(10):
            invader = Invader(3, pos)
            pos = (pos[0]+50, pos[1])
            g_allinvaders.add(invader)


        # Bullets
        last_bullet = PlayerBullet((self.WIDE, self.HEIGHT), (self.WIDE, self.HEIGHT))
        last_invader_bullet = InvaderBullet((self.WIDE, self.HEIGHT), (self.WIDE, self.HEIGHT))

        # Aux vars
        clock = pygame.time.Clock()
        wait_time = None
        start = None

        # Game
        while not self.END:
            current_time = pygame.time.get_ticks()
            if len(g_allinvaders.sprites()) == 0:
                return self.__you_win()
            if wait_time == None:
                wait_time = random.uniform(0.5, 2)
                start = pygame.time.get_ticks()
            elapsed_time = (pygame.time.get_ticks()-start)/1000
            if elapsed_time > wait_time:
                if len(g_allinvaders.sprites()) > 0:
                    rand = random.randint(0, len(g_allinvaders.sprites()) -1)
                    x_pos = g_allinvaders.sprites()[rand].rect.x
                    y_pos = g_allinvaders.sprites()[rand].rect.y
                    last_invader_bullet = InvaderBullet((x_pos, y_pos), (self.WIDE, self.HEIGHT))
                    g_bulletinvaders.add(last_invader_bullet)
                    wait_time = None

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        player.move_right(2)
                    if event.key == pygame.K_LEFT:
                        player.move_left(2)
                    if event.key == pygame.K_SPACE:
                        pos = (player.rect.x, player.rect.y)
                        last_bullet = PlayerBullet(pos, (self.WIDE, self.HEIGHT))
                        g_bulletplayer.add(last_bullet)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        player.step = 0
                if event.type == pygame.QUIT:
                    return;

            # Colisiones
            pygame.sprite.groupcollide(g_bulletplayer, g_allinvaders, True, True)

            cols2 = pygame.sprite.spritecollide(player, g_bulletinvaders, True)
            if len(cols2) > 0:
                g_lives.sprites()[-1].kill()
                if len(g_lives.sprites()) == 0:
                    self.END = True

            g_player.update()
            g_bulletplayer.update()
            g_bulletinvaders.update()
            g_allinvaders.update(current_time)
            self.SCREEN.fill(Colors.BLACK)
            g_lives.draw(self.SCREEN)
            g_player.draw(self.SCREEN)
            g_bulletplayer.draw(self.SCREEN)
            g_bulletinvaders.draw(self.SCREEN)
            g_allinvaders.draw(self.SCREEN)
            pygame.draw.line(self.SCREEN, Colors.WHITE, (0, self.HEIGHT - (self.HEIGHT * 0.1)), (self.WIDE, self.HEIGHT - (self.HEIGHT * 0.1))) 
            pygame.display.flip()
            clock.tick(60)
        return self.__you_died()

    def __you_died(self):
        self.SCREEN.fill(Colors.BLACK)
        font = pygame.font.Font(None, 36)
        text = font.render("PERDISTE", 1, Colors.RED)
        textpos = text.get_rect(centerx = self.WIDE/2)
        textpos.y = self.HEIGHT/2
        self.SCREEN.blit(text, textpos)
        pygame.display.flip()
        time.sleep(2)
        self.END = False
        return self.__play_menu()

    def __you_win(self):
        self.SCREEN.fill(Colors.BLACK)
        font = pygame.font.Font(None, 36)
        text = font.render("¡GANASTE!", 1, Colors.GREEN)
        textpos = text.get_rect(centerx = self.WIDE/2)
        textpos.y = self.HEIGHT/2
        self.SCREEN.blit(text, textpos)
        pygame.display.flip()
        time.sleep(2)
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
