import pygame
import sys
import os
from constants import *
from Player import *
from Enemy import *
from GameMap import *
from menu import *


class GameEngine:

    def event_loop(self):
        # get the pygame screen and create some local vars
        screen = pygame.display.get_surface()
        screen_rect = screen.get_rect()
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        # set up font
        basicFont = pygame.font.SysFont(None, 48)
        # initialize a clock
        clock = pygame.time.Clock()
        # initialize the score counter
        score = 0
        deltat = 0
        # initialize the enemy speed
        enemy_speed = [6, 6]

        # initialize the game map
        self.gen = 0
        self.restart = False
        self.level = GameMap(self, self.gen)
        self.next_items = []

        # main game loop
        while 1:
            if (self.restart == True):
                self.reset_map()

            self.level.handle_input()
            self.level.update(deltat)
            self.level.render()

            # set up the score text
            text = basicFont.render('Game Over?', True, (255, 0, 0))
            textRect = text.get_rect()
            textRect.centerx = screen_rect.centerx
            textRect.centery = screen_rect.centery

            # draw the text onto the surface
            if (self.level.gameover == True):
                screen.blit(text, textRect)

            # update the screen
            pygame.display.flip()

            # limit to 60 FPS
            deltat = clock.tick(60)

    def reset_map(self):
        self.gen += 1
        self.restart = False
        self.level = GameMap(self, self.gen)
        self.level.handle_nextgen(self.next_items)

    def run(self):
        # initialize pygame
        pygame.init()

        global SCREEN_HEIGHT
        global SCREEN_WIDTH
        # create the window
        size = width, height = SCREEN_WIDTH, SCREEN_HEIGHT
        screen = pygame.display.set_mode(size)

        # set the window title
        pygame.display.set_caption("Example Framework")

        # create the menu
        menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                     [('Start Game', 1, None),
                      ('Other Option', 2, None),
                      ('Exit', 3, None)])
        # center the menu
        menu.set_center(True, True)
        menu.set_alignment('center', 'center')

        # state variables for the finite state machine menu
        state = 0
        prev_state = 1

        # ignore mouse and only update certain rects for efficiency
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        rect_list = []

        while 1:
            # check if the state has changed, if it has, then post a user event to
            # the queue to force the menu to be shown at least once
            if prev_state != state:
                pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key=0))
                prev_state = state

            # get the next event
            e = pygame.event.wait()

            # update the menu
            if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
                if state == 0:
                    # "default" state
                    rect_list, state = menu.update(e, state)
                elif state == 1:
                    # start the game
                    self.event_loop()
                elif state == 2:
                    # just to demonstrate how to make other options
                    pygame.display.set_caption("y u touch this")
                    state = 0
                else:
                    # exit the game and program
                    pygame.quit()
                    sys.exit()

                # quit if the user closes the window
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # update the screen
                pygame.display.update(rect_list)


def main():
    ge = GameEngine()
    ge.run()


if __name__ == '__main__':
    main()