# Main.py runs the general structure of the game.  Every individual
# screen exists within its own function and generally within its
# own script.

print("Loading code")

import pygame
pygame.init()

from gamethods import *
from worldgeneration import *
from menumethods import *
globinfo = readglobals()
screen = makescreen()

print("Importing menus")
from mainmenu import main_menu
from about import about_screen
from settings import settings_screen

from cyc import character_select
from cychap import chapter_select
print("Importing game")
from chap1 import run_first_chapter
from chap2 import run_second_chapter
from chap3 import run_third_chapter

print("Loading graphics")

menuGraphics = get_menu_graphics(globinfo['window_width'],globinfo['window_height'])
worldx, worldy, background, nightbackground, wolfGraphics, streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim, streamCurveCoefficients, treeGraphics, treeNightGraphics, treeGreenness, rockGraphics, rockNightGraphics, decorGraphics, decorNightGraphics, decorDynamics, printGraphics, printGraphicsSmall, miscellaneousGraphics, miscellaneousNightGraphics, animalTypes, animalGraphics = getWorldGraphics(globinfo['window_height'])

running = True
while running: # This loop runs as long as the machine does.  It must end if the
    for event in pygame.event.get(): # 'x' button is selection (as shown in code below)
        if event.type == pygame.QUIT:  # If 'x' button selected, end
            running = False # If it is running another function, however, that function can
    main_menu_action = main_menu(screen,menuGraphics) # end with the 'x' and return 'stop'
    if main_menu_action == 'stop': # at any time, ending the loop.
        running = False
    elif main_menu_action == 0:
        if character_select(screen,menuGraphics) == 'stop':
            running = False # Only care if character_select stops, as character choice is kept in file.
        else:
            chapter = chapter_select(screen,menuGraphics)
            if chapter == 'stop':
                running = False
            elif chapter == 0: # First chapter can run once or twice.
                choice = run_first_chapter(screen, worldx, worldy, background, nightbackground, wolfGraphics, streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim, streamCurveCoefficients, treeGraphics, treeNightGraphics, treeGreenness, rockGraphics, rockNightGraphics, decorGraphics, decorNightGraphics, decorDynamics, printGraphics, printGraphicsSmall, miscellaneousGraphics, miscellaneousNightGraphics, animalTypes, animalGraphics)
                if choice == 'stop':
                    running = False
                elif choice == 0: # At the end, the choice is given to:
                    choice = run_first_chapter(screen,worldx, worldy, background, nightbackground, wolfGraphics, streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim, streamCurveCoefficients, treeGraphics, treeNightGraphics, treeGreenness, rockGraphics, rockNightGraphics, decorGraphics, decorNightGraphics, decorDynamics, printGraphics, printGraphicsSmall, miscellaneousGraphics, miscellaneousNightGraphics, animalTypes, animalGraphics, secondyear=True) # stay with pack another year
                    if choice == 0: # (which then gives options to:)
                        chapter = 1 # Move on to the next chapter, or
                    else:
                        pass # return to the main menu.
                elif choice == 1:
                    chapter = 1 # move on to the next chapter, or
                elif choice == 2:
                    pass # Return to the main menu, which is achieved by continuing this while loop.
            if chapter == 1:
                choice = run_second_chapter(screen, worldx, worldy, background, nightbackground, wolfGraphics, streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim, streamCurveCoefficients, treeGraphics, treeNightGraphics, treeGreenness, rockGraphics, rockNightGraphics, decorGraphics, decorNightGraphics, decorDynamics, printGraphics, printGraphicsSmall, miscellaneousGraphics, miscellaneousNightGraphics, animalTypes, animalGraphics)
                if choice == 'stop':
                    running = False
                elif choice == 0:
                    chapter = 2
                elif choice == 1:
                    pass # Return to main menu.
            if chapter == 2:
                victory = run_third_chapter(screen, worldx, worldy, background, nightbackground, wolfGraphics, streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim, streamCurveCoefficients, treeGraphics, treeNightGraphics, treeGreenness, rockGraphics, rockNightGraphics, decorGraphics, decorNightGraphics, decorDynamics, printGraphics, printGraphicsSmall, miscellaneousGraphics, miscellaneousNightGraphics, animalTypes, animalGraphics)
                if victory == 'stop':
                    running = False
                elif victory:
                    print("The player completed the game and deserved a victory animation.")
                else:
                    print("The player lost in the last phase of the game and deserves consolation.")
    elif main_menu_action == 1:
        if about_screen(screen) == 'stop':
            running = False
    elif main_menu_action == 2:
        if settings_screen(screen,menuGraphics) == 'stop':
            running = False
