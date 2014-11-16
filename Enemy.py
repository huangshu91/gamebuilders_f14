__author__ = 'Zergling'

import os
import pygame
from constants import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, level, type):
        pygame.sprite.Sprite.__init__(self)
        # load the PNG
        #self.image = pygame.image.load(os.path.join('images', 'ball.png'))
        #self.rect = self.image.get_rect()
        #self.rect.topleft = 0, 0

        self.image = pygame.Surface((60, 60))
        self.size = width, height = 60, 60

        self.image_sprite = pygame.image.load('images/enemy_bird.png')
        self.image_sprite.set_colorkey((0,0,0))

        self.screen = pygame.display.get_surface()

        self.pos = [30, 30]
        # color the surface cyan
        self.image.fill((255, 80, 80))
        self.rect = self.image.get_rect()

        self.rect.move_ip((960 - 30, 180+150-30))
        self.pos[0] = 960 - 30
        self.pos[1] = 180 + 150 - 30

        self.parent = level
        self.base_speed = 4
        self.speed = [-self.base_speed, 0]
        self.dead = False
        self.attack_counter = 0

        self.dec_knockback = 10
        self.hp = 20


        self.type = type

    def get_hit(self, player):
        if (self.attack_counter == player.attack_counter):
            return

        self.attack_counter = player.attack_counter

        self.hp -= player.damage
        if (self.hp <= 0):
            self.dead = True
            return

        pos = player.get_pos()
        if pos[0] < self.rect.left:
            self.move_pos(x = (player.knockback - self.dec_knockback))
        elif pos[0] > self.rect.right:
            self.move_pos(x = -(player.knockback - self.dec_knockback))
        elif pos[1] < self.rect.top:
            self.move_pos(y = (player.knockback - self.dec_knockback))
        elif pos[1] > self.rect.bottom:
            self.move_pos(y = -(player.knockback - self.dec_knockback))

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

    def get_halfsize(self):
        return self.size[0]/2

    def get_pos(self):
        return self.rect.center

    def set_pos(self, new_loc):
        self.rect.move_ip(new_loc)

    def move_pos(self, x = 0, y = 0):
        self.rect.move_ip(x, y)

    def render_sprite(self):
        self.screen.blit(self.image_sprite, self.rect.topleft)

    def update(self, deltat):
        self.rect = self.rect.move(self.speed)
        if (self.rect.right < 0):
            self.dead = True
        return