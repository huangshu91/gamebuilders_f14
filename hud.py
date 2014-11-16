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
        return

    def render_sprite(self):
        progress = int(self.level.get_progress()*100)
        text = self.FONT.render("Progress: "+str(progress)+"%", True, (0, 0, 0))

        self.screen.blit(text, (10, 10))
        return