#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shuheng Huang'

import pygame
from constants import *

class hud():
    def __init__(self, level, parent):
        self.FONT = pygame.font.SysFont('Calibri', 25, False, False)
        self.parent = parent
        self.level = level
        self.screen = pygame.display.get_surface()

        self.heart_sprite = pygame.image.load('images/health.png').convert_alpha()
        self.coin_sprite = pygame.image.load('images/coins.png').convert_alpha()
        self.skull_sprite = pygame.image.load('images/skull.png').convert_alpha()
        self.sword_sprite = pygame.image.load('images/sword.png').convert_alpha()

    def render_sprite(self):
        progress = int(self.level.get_progress()*100)
        text = self.FONT.render("Progress: "+str(progress)+"%", True, (0, 0, 0))

        cur_items = self.parent.cur_items
        cur_text = "Current: " + "       x"+str(cur_items.count("health"))
        cur_text += "       x"+str(cur_items.count("coins"))
        cur_text += "       x"+str(cur_items.count("skull"))
        cur_text += "       x"+str(cur_items.count("sword"))

        current_text = self.FONT.render(cur_text, True, (0, 0, 0))

        next_items = self.parent.next_items
        next_text = "Next: " + "            x"+str(next_items.count("health"))
        next_text += "       x"+str(next_items.count("coins"))
        next_text += "       x"+str(next_items.count("skull"))
        next_text += "       x"+str(next_items.count("sword"))

        nextgen_text = self.FONT.render(next_text, True, (0, 0, 0))

        gen_text = self.FONT.render("Generation: "+str(self.level.gen), True, (0, 0, 0))

        self.screen.blit(text, (10, 10))
        self.screen.blit(gen_text, (10, 40))
        self.screen.blit(current_text, (10, 70))
        self.screen.blit(nextgen_text, (10, 120))

        self.screen.blit(self.heart_sprite, (100, 60))
        self.screen.blit(self.coin_sprite, (160, 60))
        self.screen.blit(self.skull_sprite, (230, 60))
        self.screen.blit(self.sword_sprite, (300, 60))

        self.screen.blit(self.heart_sprite, (100, 110))
        self.screen.blit(self.coin_sprite, (160, 110))
        self.screen.blit(self.skull_sprite, (230, 110))
        self.screen.blit(self.sword_sprite, (300, 110))