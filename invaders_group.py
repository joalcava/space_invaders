#! /usr/bin/python3

import pygame
from invaders import Invader


class InvadersGroup(pygame.sprite.Group):

    last_left_col = 1
    last_right_col = 10
    speed_decadence = 1.3

    def __init__(self, rows):
        pygame.sprite.Group.__init__(self)

        screen_pos = (-10, 50)
        for row in range(1, rows + 1):
            can_shoot = False
            if row == 1:
                _type = 1
            elif row == rows:
                _type = 3
                can_shoot = True
            else:
                _type = 2

            for col in range(1, 11):
                pygame.sprite.Group.add(self,
                    Invader(_type, screen_pos, (row, col), can_shoot))
                screen_pos = (screen_pos[0] + 50, screen_pos[1])
            screen_pos = (-10, screen_pos[1] + 40)

    def update(self, current_time):
        if current_time - Invader.time > Invader.speed:
            pygame.sprite.Group.update(self)
            if Invader.current_step < Invader.steps:
                Invader.current_step += 1
            else:
                Invader.current_step = 1
                Invader.direction = Invader.direction * -1
                Invader.speed = Invader.speed / InvadersGroup.speed_decadence
            Invader.time = pygame.time.get_ticks()
            Invader.current_image = int(not (bool(Invader.current_image)))
        self.check_column_deletion()

    def check_column_deletion(self):
        still_left_columns = False
        still_right_columns = False
        sprites = pygame.sprite.Group.sprites(self)

        # To right
        if Invader.direction == 1:
            for sprite in sprites:
                if sprite.is_right_border is True:
                    still_right_columns = True
                    break
            if still_right_columns is False:
                tempr = self.last_right_col
                self.check_last_right_column()
                if tempr != self.last_right_col:
                    diff = tempr - self.last_right_col
                    print(diff)
                    Invader.steps += (diff * 5)
        # To left
        else:
            for sprite in sprites:
                if sprite.is_left_border is True:
                    still_left_columns = True
                    break
            if still_left_columns is False:
                templ = self.last_left_col
                self.check_last_left_column()
                if templ != self.last_left_col:
                    diff = self.last_left_col - templ
                    print(diff)
                    Invader.steps += (diff * 5)

    def check_last_left_column(self):
        sprites = pygame.sprite.Group.sprites(self)
        if len(sprites) == 0: return
        for sprite in sprites:
            if sprite.pos[1] == self.last_left_col:
                return
        self.last_left_col += 1
        return self.check_last_left_column()

    def check_last_right_column(self):
        sprites = pygame.sprite.Group.sprites(self)
        if len(sprites) == 0: return
        for sprite in sprites:
            if sprite.pos[1] == self.last_right_col:
                return
        self.last_right_col -= 1
        return self.check_last_right_column()
