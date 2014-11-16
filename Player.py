__author__ = 'Zergling'

import pygame
import pyganim
from constants import *

class Player(pygame.sprite.Sprite):
    # constructor for this class
    def __init__(self, level):
        global ATTACK_RATE
        # call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # create 50px by 50px surface
        self.image = pygame.Surface((40, 60))
        # color the surface cyan
        self.image.fill((0, 205, 205))
        self.rect = self.image.get_rect()
        self.speed = [0, 0]

        self.agil = 6
        self.knockback = 30
        self.damage = 10

        self.dead = False

        self.parent = level
        self.screen = pygame.display.get_surface()

        self.is_attacking = False
        self.attack_timer = 0.0
        self.attack_counter = 0
        self.atk_rate = ATTACK_RATE

        self.anim = pyganim.PygAnimation([('images/player_walk1.png', 0.2), ('images/player_walk2.png', 0.2),
            ('images/player_walk3.png', 0.2), ('images/player_walk4.png', 0.2)])
        self.anim.set_colorkey((0, 0, 0))
        self.anim.play()

        self.atk_anim = pyganim.PygAnimation([('images/player_attack1.png', 0.05), ('images/player_attack2.png', 0.1),
            ('images/player_attack3.png', 0.1), ('images/player_attack4.png', 0.05)])
        #self.atk_anim.scale2x()
        self.atk_anim.loop = False
        self.atk_anim.set_colorkey((0,0,0))

        self.dust_sprite = pygame.image.load('images/dustball.png').convert_alpha()

        self.atk_range = 90

    def left(self):
        self.speed[0] -= self.agil

    def right(self):
        self.speed[0] += self.agil

    def up(self):
        self.speed[1] -= self.agil

    def down(self):
        self.speed[1] += self.agil

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

    def render_sprite(self):
        self.anim.blit(self.screen, self.rect.topleft)
        #if (self.attacking == True):
        self.atk_anim.blit(self.screen, self.rect.topleft)
        if self.is_attacking:
            pygame.draw.circle(self.screen, (255, 0, 0), self.rect.center, 40, 1)

        if self.speed[0] != 0 or self.speed[1] != 0:
            loc = [0, 0]
            loc[0] = self.rect.bottomleft[0]
            loc[1] = self.rect.bottomleft[1] - 10

            self.screen.blit(self.dust_sprite, loc)

    def get_pos(self):
        return self.rect.center

    def update(self, deltat):
        if (self.dead):
            return

        self.attack_timer -= (deltat/1000.0)

        if self.atk_anim.isFinished():
            self.is_attacking = False
        self.move()

    def attack(self):
        global ATTACK_RATE
        if (self.attack_timer > 0 or self.parent.gameover == True):
            return

        self.atk_anim.play()
        self.attack_counter += 1
        self.is_attacking = True
        self.attack_timer = self.atk_rate