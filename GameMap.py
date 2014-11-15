__author__ = 'Zergling'

import pygame
from constants import *
from Player import *

class GameMap:
    def __init__(self):
        global MAP_WIDTH
        global MAP_HEIGHT
        global CELL_SIZE

        self.size = width, height = MAP_WIDTH, MAP_HEIGHT
        #self.parent = parent

        self.bgcolor = (80, 80, 200)
        self.mapcolor = (80, 200, 80)
        self.screen = pygame.display.get_surface()

        self.basemap = pygame.Surface(self.size)
        self.basemap.fill(self.mapcolor)

        #self.player = Player(self)

        num_cells = MAP_WIDTH/CELL_SIZE + MAP_HEIGHT/CELL_SIZE

    def render(self):
        self.screen.fill(self.bgcolor)
        self.screen.blit(self.basemap, [0, 180])

    def update(self, deltat):
        #stuff
        return

    def generate_enemies(self, deltat):
        #stuff
        return




