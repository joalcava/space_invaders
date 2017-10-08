#/usr/bin/python3

import pygame
import random
from player import Player
from invaders import SmallInvader, BigInvader, HugeInvader
from colors import Colors

ANCHO=800
ALTO=600


if __name__ == '__main__':
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO,ALTO])

    jp = Jugador(50,70)
    general = pygame.sprite.Group()
    general.add(jp)
    jp.rect.x = 100
    jp.rect.y = 100

    rivales = pygame.sprite.Group()
    n = 10
    for i in range(n):
        r = Rival(20,20)
        r.rect.x = random.randrange(10, ANCHO-20)
        r.rect.y = random.randrange(10, ALTO-20)
        rivales.add(r)
        general.add(r)

    ptos = 0
    reloj = pygame.time.Clock()
    fin = False
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    jp.var_x = 5
                    jp.var_y = 0
                if event.key == pygame.K_UP:
                    jp.var_x = 0
                    jp.var_y = -5
                if event.key == pygame.K_DOWN:
                    jp.var_x = 0
                    jp.var_y = 5
                if event.key == pygame.K_LEFT:
                    jp.var_x = -5
                    jp.var_y = 0
                if event.key == pygame.K_SPACE:
                    jp.var_y = 0
                    jp.var_x = 0
            if event.type == pygame.KEYUP:
                jp.var_x = 0
                jp.var_y = 0
            if event.type == pygame.QUIT:
                fin = True

        # gestion de la colision
        ls_col = pygame.sprite.spritecollide(jp, rivales, True)
        for elemento in ls_col:
            ptos += 1
            print ptos

        general.update()
        rivales.update()
        # actualizacion de pantalla
        pantalla.fill(Colors.BLUE)
        general.draw(pantalla)
        pygame.display.flip()
        reloj.tick(40)
