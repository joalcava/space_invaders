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
        # Groups
        glives = pygame.sprite.Group()
        gplayer = pygame.sprite.Group()
        ginvaders = pygame.sprite.Group()
        gbulletplayer = pygame.sprite.Group()
        gbulletinvaders = pygame.sprite.Group()

        #Player
        player = Player(20, 10, self.WIDE)
        gplayer.add(player)
        player.rect.x = 100
        player.rect.y = 500

        # Lives
        pos_a = 50
        for y in range(3):
            glives.add(Heart((pos_a, self.HEIGHT - (self.HEIGHT * 0.07))))
            pos_a += 50

        # Invaders
        pos_b = (10, 100)
        for i in range(10):
            pos_b = (pos_b[0]+60, pos_b[1])
            invader = Invader(pos_b, 4)
            ginvaders.add(invader)

        # Bullets
        last_bullet = PlayerBullet((self.WIDE, self.HEIGHT), (self.WIDE, self.HEIGHT))
        last_invader_bullet = InvaderBullet((self.WIDE, self.HEIGHT), (self.WIDE, self.HEIGHT))

        # Aux vars
        clock = pygame.time.Clock()
        wait_time = None
        start = None

        # Game
        while not self.END:
            if len(ginvaders.sprites()) == 0:
                return self.__you_win()
            if wait_time == None:
                wait_time = random.uniform(0.5, 2)
                start = pygame.time.get_ticks()
            elapsed_time = (pygame.time.get_ticks()-start)/1000
            if elapsed_time > wait_time:
                if len(ginvaders.sprites()) > 0:
                    rand = random.randint(0, len(ginvaders.sprites()) -1)
                    x_pos = ginvaders.sprites()[rand].rect.x
                    y_pos = ginvaders.sprites()[rand].rect.y
                    last_invader_bullet = InvaderBullet((x_pos, y_pos), (self.WIDE, self.HEIGHT))
                    gbulletinvaders.add(last_invader_bullet)
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
                        gbulletplayer.add(last_bullet)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        player.step = 0
                if event.type == pygame.QUIT:
                    return;

            # Colisiones
            pygame.sprite.groupcollide(gbulletplayer, ginvaders, True, True)

            cols2 = pygame.sprite.spritecollide(player, gbulletinvaders, True)
            if len(cols2) > 0:
                glives.sprites()[-1].kill()
                if len(glives.sprites()) == 0:
                    self.END = True

            gplayer.update()
            gbulletplayer.update()
            gbulletinvaders.update()
            ginvaders.update()
            self.SCREEN.fill(Colors.BLACK)
            glives.draw(self.SCREEN)
            gplayer.draw(self.SCREEN)
            gbulletplayer.draw(self.SCREEN)
            gbulletinvaders.draw(self.SCREEN)
            ginvaders.draw(self.SCREEN)
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
        time.sleep(2)
        self.END = False
        return self.__play_menu()

    def __you_win(self):
        self.SCREEN.fill(Colors.BLACK)
        font = pygame.font.Font(None, 36)
        text = font.render("¡Ganaste!", 1, Colors.GREEN)
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
