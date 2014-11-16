__author__ = 'Zergling'

import pygame
import sys
import math
from random import randint
from constants import *
from Player import *
from Enemy import *
from Item import *
from hud import *

def get_dist_pe(player, enemy):
    p_loc = player.get_pos()
    e_loc = enemy.get_pos()
    #print e_loc
   # print p_loc
    return math.sqrt(math.pow(p_loc[0] - e_loc[0], 2) + math.pow(p_loc[1] - e_loc[1], 2))

class GameMap:
    def __init__(self, parent, gen):
        global MAP_WIDTH
        global MAP_HEIGHT
        global CELL_SIZE

        self.size = width, height = MAP_WIDTH, MAP_HEIGHT
        self.parent = parent
        self.gameover = False

        self.bgcolor = (135, 206, 250)
        self.mapcolor = (154, 205, 50)
        self.screen = pygame.display.get_surface()

        self.basemap = pygame.Surface(self.size, pygame.SRCALPHA)
        self.basemap.fill(self.mapcolor)

        self.hud = hud(self, parent)

        self.item_timer = 0
        self.timer = 0
        self.progress = 0.0

        self.player = Player(self)

        self.sprite_list = pygame.sprite.Group()
        #self.sprite_list.add(self.player)

        self.enemy_list = []
        self.dead_list = []
        self.item_list = []

        self.generation = gen


    def render(self):
        self.screen.fill(self.bgcolor)
        self.screen.blit(self.basemap, [0, 180])

        #self.sprite_list.draw(self.screen)
        self.player.render_sprite()
        for en in self.enemy_list:
            en.render_sprite()

        for it in self.item_list:
            it.render_sprite()

        self.hud.render_sprite()

    def update(self, deltat):
        global INIT_SPAWN_RATE
        global INIT_ITEM_RATE

        self.timer += deltat/1000.0
        self.item_timer += deltat/1000.0
        self.progress += deltat/1000.0

        if self.gameover == True:
            return

        self.player.update(deltat)

        for en in self.enemy_list:
            en.update(deltat)
            dist = get_dist_pe(self.player, en)
            if (self.player.is_attacking and dist < self.player.atk_range):
                en.get_hit(self.player)
            if (en.dead == True):
                self.enemy_list.remove(en)
                self.sprite_list.remove(en)
            if (dist < 40):
                self.gameover = True

        for it in self.item_list:
            it.update(deltat)
            dist = get_dist_pe(self.player, it)
            if (dist < 40):
                it.dead = True
                self.parent.next_items.append(it.type)
            if (it.dead == True):
                self.item_list.remove(it)

        if (self.timer > INIT_SPAWN_RATE):
            self.timer = 0
            self.generate_enemies()

        if (self.item_timer > INIT_ITEM_RATE):
            self.item_timer = 0
            self.generate_items()

    # def remove_corpse(self):
    #     for en in self.dead_list:
    #         self.enemy_list.remove

    def generate_items(self):
        global ITEMS
        global NUM_ITEMS
        ind = randint(0, NUM_ITEMS-1)
        newitem = Item(self, ITEMS[ind])
        initial_y = randint(0, 240)
        initial_y -= 120
        newitem.move_pos(y = initial_y)

        self.item_list.append(newitem)

    def generate_enemies(self):
        newenemy = Enemy(self, "none")

        initial_y = randint(0, 240)
        initial_y -= 120
        newenemy.move_pos(y = initial_y)

        self.enemy_list.append(newenemy)
        self.sprite_list.add(newenemy)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.left()
                elif event.key == pygame.K_RIGHT:
                    self.player.right()
                elif event.key == pygame.K_UP:
                    self.player.up()
                elif event.key == pygame.K_DOWN:
                    self.player.down()
                elif event.key == pygame.K_z:
                    if(self.gameover == True):
                        self.parent.restart = True
                    self.player.attack()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.right()
                elif event.key == pygame.K_RIGHT:
                    self.player.left()
                elif event.key == pygame.K_UP:
                    self.player.down()
                elif event.key == pygame.K_DOWN:
                    self.player.up()

    def handle_nextgen(self, items):
        for it in items:
            if it == "coins":
                self.player.agil += 1
            elif it == "skull":
                self.player.knockback += 5
            elif it == "health":
                self.player.damage += 2
            elif it == "sword":
                self.player.atk_rate -= 0.1
                if (self.player.atk_rate < 0.2):
                    self.player.atk_rate = 0.2

    def get_progress(self):
        global LEVEL_LENGTH
        return self.progress/LEVEL_LENGTH
