# This script operates the game's main menu - three buttons ("play", "settings",
# and "about"), about which an indicator is moved by the up and down keys.
# Spacebar will trigger another screen, depending on where the indicator is.

# The main menu function returns the player's choice - to play the game, to view the
# about screen, or to edit the settings screen.  Input to it is the screen and all
# needed graphics, loaded in advance.

import pygame

def main_menu(screen,menuGraphics):
    # The positions of the indicator and the buttons, as well as the size of the
    # buttons, are all determined by the window dimensions such that they take
    # nice proportions.  These were chosen for nice geometry and their results
    # are as shown in the screens themselves.
    window_width, window_height = screen.get_width(), screen.get_height()
    positionslist = [(int(3*window_width/4),int(window_height/3)),(int(7*window_width/12),int(7*window_height/12)),
        (int(7*window_width/12),int(3*window_height/4))]
    position = 0 # Current position, indicated by place in positionslist

    # This sub-function drawns the main menu screen over the previous,
    # everytime an indicator moves.
    def draw_main_menu(screen,menuGraphics,window_width,window_height):
        screen.blit(menuGraphics['background'], (0,0)) # Blit background, then buttons, then indicator.
        screen.blit(menuGraphics['play'],(int(window_width/4),int(window_height/4)))
        screen.blit(menuGraphics['about'],(int(5*window_width/12),int(7*window_height/12)))
        screen.blit(menuGraphics['settings'],(int(5*window_width/12),int(3*window_height/4)))
        screen.blit(menuGraphics['indicator'],positionslist[position])
        pygame.display.update()

    draw_main_menu(screen,menuGraphics,window_width,window_height)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If 'x' button selected, end
                return 'stop'
            elif event.type == pygame.KEYDOWN: # For keys up and down, move
                if event.key == pygame.K_UP and position > 0: # indicator.
                    position -= 1
                    draw_main_menu(screen,menuGraphics,window_width,window_height)
                elif event.key == pygame.K_DOWN and position < 2:
                    position += 1
                    draw_main_menu(screen,menuGraphics,window_width,window_height)
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return position
