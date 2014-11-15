import pygame
import sys
import os
from constants import *
from Player import *
from Enemy import *
from GameMap import *
from menu import *

def event_loop():
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
    level = GameMap()
    
    # initialize the player and the enemy
    player = Player(level)
    enemy = Enemy(level)
    enemy_list = []

    enemy_list.append(enemy)

    # create a sprite group for the player and enemy
    # so we can draw to the screen
    sprite_list = pygame.sprite.Group()
    sprite_list.add(player)
    sprite_list.add(enemy)

    # create a sprite group for enemies only to detect collisions
    #enemy_list = pygame.sprite.Group()
    #enemy_list.add(enemy)

    # main game loop
    while 1:
        # handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.left()
                elif event.key == pygame.K_RIGHT:
                    player.right()
                elif event.key == pygame.K_UP:
                    player.up()
                elif event.key == pygame.K_DOWN:
                    player.down()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.right()
                elif event.key == pygame.K_RIGHT:
                    player.left()
                elif event.key == pygame.K_UP:
                    player.down()
                elif event.key == pygame.K_DOWN:
                    player.up()

        level.update(deltat)

        # call the move function for the player
        player.update(deltat)
        player.move()

        # check player bounds
        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.right > screen_width:
            player.rect.right = screen_width
        if player.rect.top < 0:
            player.rect.top = 0
        if player.rect.bottom > screen_height:
            player.rect.bottom = screen_height

        # reverse the movement direction if enemy goes out of bounds
        #if enemy.rect.left < 0 or enemy.rect.right > screen_width:
        #    enemy_speed[0] = -enemy_speed[0]
        #if enemy.rect.top < 0 or enemy.rect.bottom > screen_height:
        #    enemy_speed[1] = -enemy_speed[1]

        # another way to move rects
        #enemy.rect.x += enemy_speed[0]
        #enemy.rect.y += enemy_speed[1]

        # detect all collisions between the player and enemy
        # but don't remove enemy after collisions
        # increment score if there was a collision
        #if pygame.sprite.spritecollide(player, enemy_list, False):
        #    score += 1

        # black background
        #screen.fill((0, 0, 0))
        level.render()

        for en in enemy_list:
            en.update()

        # set up the score text
        #text = basicFont.render('Score: %d' % score, True, (255, 255, 255))
        #textRect = text.get_rect()
        #textRect.centerx = screen_rect.centerx
        #textRect.centery = screen_rect.centery
        
        # draw the text onto the surface
        #screen.blit(text, textRect)

        # draw the player and enemy sprites to the screen
        sprite_list.draw(screen)

        # update the screen
        pygame.display.flip()

        # limit to 60 FPS
        deltat = clock.tick(60)

def main():
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
                 [('Start Game',   1, None),
                  ('Other Option', 2, None),
                  ('Exit',         3, None)])
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
            pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
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
                event_loop()
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

if __name__ == '__main__':
    main()