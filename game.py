#! /usr/bin/python3

import random
import time
import pygame

pygame.display.set_mode((800, 600))

from player import Player
from colors import Colors
from bullets import InvaderBullet, PlayerBullet
from heart import Heart
from invaders import Invader
from invaders_group import InvadersGroup
from block import Blocker


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
        self.level = 1
        self.bullet_cadence = 2
        self.sounds = {}
        for sound_name in ["shoot", "invaderkilled", "playerexplosion"]:
            self.sounds[sound_name] = pygame.mixer.Sound("sounds/{}.wav".format(sound_name))
            self.sounds[sound_name].set_volume(0.2)

    def start(self):
        self.__play_menu()

    def __play_game(self):
        # Groups
        g_lives = pygame.sprite.Group()
        g_player = pygame.sprite.Group()
        g_all_invaders = InvadersGroup(rows=4)
        g_bullet_player = pygame.sprite.Group()
        g_bullet_invaders = pygame.sprite.Group()
        g_all_sprites = pygame.sprite.Group()
        g_blockers = pygame.sprite.Group()


        # Player
        player = Player(self.WIDE)
        player.rect.x, player.rect.y = 100, 500
        g_player.add(player)
        g_all_sprites.add(player)

        # Lives
        g_lives.add(Heart((50, self.HEIGHT - (self.HEIGHT * 0.07))))
        g_lives.add(Heart((100, self.HEIGHT - (self.HEIGHT * 0.07))))
        g_lives.add(Heart((150, self.HEIGHT - (self.HEIGHT * 0.07))))
        g_all_sprites.add(g_lives.sprites())

        # Blockers
        all_blockers = pygame.sprite.Group(
            self.make_blockers(0), self.make_blockers(1), self.make_blockers(2), self.make_blockers(3))
        g_all_sprites.add(all_blockers)
        # Aux vars
        clock = pygame.time.Clock()
        wait_time = None
        start = None

        self.__configure_level()

        # Game
        while not self.END:
            if len(g_all_invaders.sprites()) == 0:
                return self.__you_win()

            # Invaders bullets
            current_time = pygame.time.get_ticks()
            if wait_time is None:
                wait_time = random.uniform(0.5, self.bullet_cadence)
                start = pygame.time.get_ticks()
            elapsed_time = (current_time - start) / 1000
            if elapsed_time > wait_time:
                if len(g_all_invaders.sprites()) > 0:
                    rand = random.randint(0, len(g_all_invaders.sprites()) - 1)
                    x_pos = g_all_invaders.sprites()[rand].rect.x
                    y_pos = g_all_invaders.sprites()[rand].rect.y
                    last_invader_bullet = InvaderBullet((x_pos, y_pos), (self.WIDE, self.HEIGHT))
                    g_bullet_invaders.add(last_invader_bullet)
                    g_all_sprites.add(last_invader_bullet)
                    wait_time = None

            # Keys
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        player.move_right(2)
                    if event.key == pygame.K_LEFT:
                        player.move_left(2)
                    if event.key == pygame.K_SPACE:
                        # Player bullet
                        pos = (player.rect.x, player.rect.y)
                        if len(g_bullet_player.sprites()) == 0:
                            last_player_bullet = PlayerBullet((pos[0]+17, pos[1]), (self.WIDE, self.HEIGHT))
                            self.sounds["shoot"].play()
                            g_bullet_player.add(last_player_bullet)
                            g_all_sprites.add(last_player_bullet)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        player.step = 0
                if event.type == pygame.QUIT:
                    return

            # Collisions
            has_collide = len(pygame.sprite.groupcollide(g_bullet_player, g_all_invaders, True, True)) > 0
            if has_collide:
                self.sounds["invaderkilled"].play()

            has_collide = len(pygame.sprite.spritecollide(player, g_bullet_invaders, True)) > 0
            if has_collide:
                self.sounds["playerexplosion"].play()
                g_lives.sprites()[-1].kill()
                if len(g_lives.sprites()) == 0:
                    self.END = True

            has_collide = len(pygame.sprite.spritecollide(player, g_all_invaders, True)) > 0
            if has_collide:
                return self.__you_died()

            pygame.sprite.groupcollide(g_bullet_player, all_blockers, True, True)
            pygame.sprite.groupcollide(g_bullet_invaders, all_blockers, True, True)
            pygame.sprite.groupcollide(g_all_invaders, all_blockers, False, True)

            g_all_sprites.update()
            g_all_invaders.update(current_time)
            self.SCREEN.fill(Colors.BLACK)
            g_all_sprites.draw(self.SCREEN)
            g_all_invaders.draw(self.SCREEN)
            pygame.draw.line(self.SCREEN, Colors.WHITE, (0, self.HEIGHT - (self.HEIGHT * 0.1)),
                             (self.WIDE, self.HEIGHT - (self.HEIGHT * 0.1)))
            pygame.display.flip()
            clock.tick(60)
        return self.__you_died()

    def __configure_level(self):
        if self.level == 1:
            pass
        else:
            self.bullet_cadence -= 0.3
            Invader.speed -= 70
            InvadersGroup.speed_decadence += 0.1

    def __you_died(self):
        self.SCREEN.fill(Colors.BLACK)
        font = pygame.font.Font(None, 36)
        text = font.render("PERDISTE", 1, Colors.RED)
        textpos = text.get_rect(centerx=self.WIDE / 2)
        textpos.y = self.HEIGHT / 2
        self.SCREEN.blit(text, textpos)
        pygame.display.flip()
        time.sleep(2)
        self.END = False
        return self.__play_menu()

    def __you_win(self):
        self.SCREEN.fill(Colors.BLACK)
        font = pygame.font.Font(None, 36)
        text = font.render("¡GANASTE!", 1, Colors.GREEN)
        text_pos = text.get_rect(centerx=self.WIDE / 2)
        text_pos.y = self.HEIGHT / 2
        self.SCREEN.blit(text, text_pos)
        pygame.display.flip()
        time.sleep(2)
        self.END = False
        self.level += 1
        return self.__next_level()

    def __next_level(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return self.__play_game()
                if event.type == pygame.QUIT:
                    return
            self.SCREEN.fill(Colors.BLACK)
            font = pygame.font.Font(None, 36)
            text = font.render("Siguiente nivel: " + str(self.level), 1, Colors.GREEN)
            textpos = text.get_rect(centerx=self.WIDE / 2)
            textpos.y = 100
            self.SCREEN.blit(text, textpos)
            text2 = font.render("Enter para empezar", 1, Colors.GREEN)
            textpos2 = text.get_rect()
            textpos2.x = 280
            textpos2.y = 300
            self.SCREEN.blit(text2, textpos2)
            pygame.display.flip()
            clock.tick(60)

    def __play_menu(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return self.__play_game()
                if event.type == pygame.QUIT:
                    return
            self.SCREEN.fill(Colors.BLACK)
            font = pygame.font.Font(None, 36)
            text = font.render("Bienvenido", 1, Colors.WHITE)
            textpos = text.get_rect(centerx=self.WIDE / 2)
            textpos.y = 100
            self.SCREEN.blit(text, textpos)
            text2 = font.render("Enter para empezar", 1, Colors.GREEN)
            textpos2 = text.get_rect()
            textpos2.x = 280
            textpos2.y = 300
            self.SCREEN.blit(text2, textpos2)
            pygame.display.flip()
            clock.tick(60)

    def make_blockers(self, number):
        g_blockers = pygame.sprite.Group()
        for row in range(4):
            for column in range(9):
                blocker = Blocker(10, Colors.GREEN, row, column)
                blocker.rect.x = 50 + (200 * number) + (column * blocker.width)
                blocker.rect.y = 450 + (row * blocker.height)
                g_blockers.add(blocker)
        return g_blockers
