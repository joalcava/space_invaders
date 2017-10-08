import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, an, al):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([an,al])
        self.image.fill(BLANCO)
        self.rect=self.image.get_rect()
        self.var_x=0
        self.var_y=0

    def update(self):
        self.rect.x+=self.var_x
        self.rect.y+=self.var_y