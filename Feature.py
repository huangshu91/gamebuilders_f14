__author__ = 'Zergling'

import pygame
from constants import *

class Feature:
    def __init__(self, level, type):
        self.size = width, height = 40, 40
        self.image = pygame.Surface(self.size)

        self.image_sprite = pygame.image.load('images/'+ type + '.png').convert_alpha()

        self.screen = pygame.display.get_surface()

        self.dead = False

        self.pos = [30, 30]
        # color the surface cyan
        self.image.fill((255, 80, 80))
        self.rect = self.image.get_rect()

        #self.rect.move_ip((960 - 30, 180+150-30))
        #self.pos[0] = 960 - 30
        #self.pos[1] = 180 + 150 - 30

        self.parent = level
        self.base_speed = 4
        if (type == "parallax_cloud_back"):
            self.base_speed = 2
        self.speed = [-self.base_speed, 0]
        self.dead = False

        self.type = type

    def get_pos(self):
        return self.rect.center

    def move_pos(self, x = 0, y = 0):
        self.rect.move_ip(x, y)

    def render_sprite(self):
        self.screen.blit(self.image_sprite, self.rect.topleft)

    def update(self, deltat):
        self.rect = self.rect.move(self.speed)
        if (self.rect.right < 0):
            self.dead = True
        return