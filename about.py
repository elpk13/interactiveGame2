# This script runs the 'about' page that can be accessed from the main menu.

# Imports
import pygame
from dialog import bliterate

# This function does the work of placing the text.  It is a function
# so that the surface on which things must be drawn, screen, can be
# passed to it from main_menu.py.  The argument and the item sent to
# it share the name 'screen'.
def about_screen(screen):

    # Choose background colors and text colors.
    BACKGROUND_COLOR = (240,232,223)
    TEXT_COLOR = (77,34,16)
    # Also in the pallette used to draw wolves:
    # (196, 190, 78)
    # (98, 94, 77)
    # (228, 228, 228)
    # (135, 111, 91)

    # Open and read file of text to display.
    gameinfofile = open("about.txt","r")
    gameinfo = gameinfofile.read()
    gameinfofile.close()

    # Size and place a large mid-screen rectangle.
    recleft, recwidth, recdown, recheight = int(screen.get_width()/4),int(screen.get_width()/8),int(screen.get_width()*0.5),int(screen.get_height()*0.75)
    mainrectangle = pygame.Rect(recleft, recwidth, recdown, recheight)
    pygame.draw.rect(screen,BACKGROUND_COLOR,mainrectangle)

    # Place the text of 'about.txt' within the rectangle.
    myfont = pygame.font.SysFont('constantia',24)
    bliterate(screen,gameinfo,recleft,recwidth,recdown,height=recheight,buffer=20,font=myfont,color=TEXT_COLOR)
    # Bliterate function takes care of line and paragraph breaks.  See dialog.py.

    pygame.display.update()

    aboutscreen = True
    while aboutscreen:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and ( event.key == pygame.K_SPACE or event.key == pygame.K_RETURN ):
                aboutscreen = False
            elif event.type == pygame.QUIT:
                return 'stop'
