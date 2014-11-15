__author__ = 'Zergling'

import os
import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, level):
        pygame.sprite.Sprite.__init__(self)
        # load the PNG
        #self.image = pygame.image.load(os.path.join('images', 'ball.png'))
        #self.rect = self.image.get_rect()
        #self.rect.topleft = 0, 0

        self.image = pygame.Surface((60, 60))
        # color the surface cyan
        self.image.fill((255, 80, 80))
        self.rect = self.image.get_rect()
        self.rect.move_ip((720, 180))

        self.parent = level
        self.base_speed = 4
        self.speed = [-self.base_speed, 0]
        self.dead = 0

    def update(self):
        self.rect = self.rect.move(self.speed)
        if (self.rect.right < 0):
            self.dead = 1
        return