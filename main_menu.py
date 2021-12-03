# This script operates the game's main menu - three buttons ("play", "settings",
# and "about"), about which an indicator is moved by the up and down keys.
# Spacebar will trigger another screen, depending on where the indicator is.

# Currently, those screens are commented out as they are not yet coded.

import pygame
#need the folowing line because we've stored the pictures in a folder and python can't access it without the os.path.join line!
import os

pygame.init()

height = 900 # Set the dimensions of the screen, by which
width = 1200  # everything will be scaled later.
screen = pygame.display.set_mode((width,height))

# Select and size background image
background = pygame.image.load(os.path.join('Assets',"winter_forest_background.jpg")) # Image credit:
background = pygame.transform.scale(background,(width,height)) # Linnaea Mallette,
                                                               # publicdomainpictures.net
# Select and scale three buttons
playbutton = pygame.image.load(os.path.join('Assets',"play_button.jpg"))
playbutton = pygame.transform.scale(playbutton,(int(width/2),int(height/4)))
settingsbutton = pygame.image.load(os.path.join('Assets',"settings_button.jpg"))
settingsbutton = pygame.transform.scale(settingsbutton,(int(width/6),int(height/12)))
aboutbutton = pygame.image.load(os.path.join('Assets',"about_button.jpg"))
aboutbutton = pygame.transform.scale(aboutbutton,(int(width/6),int(height/12)))

# Select and scale an indicator to show what is selected
indicator = pygame.image.load(os.path.join('Assets',"indicator_paw.png"))
indicator = pygame.transform.scale(indicator,(int(height/12),int(height/12)))
# Positions for indicator:  to the right of any of the three buttons
positionslist = [(int(3*width/4),int(height/3)),(int(7*width/12),int(7*height/12)),
    (int(7*width/12),int(3*height/4))]
position = 0 # Current position, indicated by place in positionslist

# Blit background, then buttons, then indicator, and update screen.
def drawscreen():
    screen.blit(background, (0,0))
    screen.blit(playbutton,(int(width/4),int(height/4)))
    screen.blit(settingsbutton,(int(5*width/12),int(7*height/12)))
    screen.blit(aboutbutton,(int(5*width/12),int(3*height/4)))
    screen.blit(indicator,positionslist[position])
    pygame.display.update()

drawscreen()

runningmenu = True


while runningmenu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If 'x' button selected, end
            runningmenu = False
        elif event.type == pygame.KEYDOWN: # For keys up and down, move
            if event.key == pygame.K_UP and position > 0: # indicator.
                position -= 1
                drawscreen()
            elif event.key == pygame.K_DOWN and position < 2:
                position += 1
                drawscreen()
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                if position == 0:
                  import cyc
                  drawscreen()
                    # Launch game!
                elif position == 1:
                    # Open settings
                    import settings
                    drawscreen()
                else:
                    # Open about
                    import about # Reads the file
                    from about import displaygameinfo
                    displaygameinfo(screen) # Displays text to our surface,
                                            # runs loop for about screen.
                    drawscreen() # Return screen to main menu when done