__author__ = 'Zergling'

import pygame
from constants import *

class Player(pygame.sprite.Sprite):
    # constructor for this class
    def __init__(self, level):
        # call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # create 50px by 50px surface
        self.image = pygame.Surface((60, 60))
        # color the surface cyan
        self.image.fill((0, 205, 205))
        self.rect = self.image.get_rect()
        self.speed = [0, 0]

        self.parent = level

        self.attacking = 0
        self.attack_timer = 0.0

    def left(self):
        self.speed[0] -= 8

    def right(self):
        self.speed[0] += 8

    def up(self):
        self.speed[1] -= 8

    def down(self):
        self.speed[1] += 8

    def move(self):
        # move the rect by the displacement ("speed")
        self.rect = self.rect.move(self.speed)

        global MAP_WIDTH
        global MAP_HEIGHT

        if (self.rect.left < 0):
            self.rect.left = 0
        if (self.rect.right > MAP_WIDTH):
            self.rect.right = MAP_WIDTH
        if (self.rect.top < 0 + 180):
            self.rect.top = 0 + 180
        if (self.rect.bottom > MAP_HEIGHT + 180):
            self.rect.bottom = MAP_HEIGHT + 180

    def update(self, deltat):
        self.attack_timer -= (deltat/1000)

    def attack(self):
        #stuff
        return