# This script provides a settings screen and updates the
# settings file.

import pygame

def settings_screen(screen,menuGraphics):
    # The positions that the indicators can take and the locations of the buttons
    # are found from geometry, such that the indicators move in equal increments
    # along the lengths of the slider bars, which have nice proportions.
    window_width, window_height = screen.get_width(), screen.get_height()
    positionslist1 = [] # Set up positions for indicators along label bars.
    positionslist2 = []
    for x in range(1,10):
        positionslist1.append((int(window_width/4+x*window_width/20 - window_height/24),int(window_height/2 - window_height/24)))
        positionslist2.append((int(window_width/4+x*window_width/20 - window_height/24),int(5*window_height/6 - window_height/24)))
    #positionslist3 = [(int(7*width/9),int(height/3)),(int(7*width/9),int(2*height/3))]

    position1 = 0 # Current position, indicated by place in positionslist
    position2 = 0
    position3 = 0 # pos3 indicates active indicator between the two.

    # Similar to draw_main_menu
    def draw_settings_screen(screen,menuGraphics,window_width,window_height):
        screen.blit(menuGraphics['background'], (0,0))
        screen.blit(menuGraphics['sound'],(int(window_width/4),int(window_height/3)))
        screen.blit(menuGraphics['narration'],(int(window_width/4),int(2*window_height/3)))
        screen.blit(menuGraphics['indicator'],positionslist1[position1])
        screen.blit(menuGraphics['indicator2'],positionslist2[position2])
        pygame.display.update()

    settingsfile = open("settings.txt","r") # Retrieve current status of settings
    currentsettings = settingsfile.readlines() # from settings file.
    position1 = int(currentsettings[0][0])
    position2 = int(currentsettings[1][0])
    otherinfo = currentsettings[2:] # Not to be edited by settings, as such,
     # must be returned when file is rewritten.
    settingsfile.close()

    def updatesettingsfile(): # A function to pass the positions to the settings
        settingsfile = open("settings.txt","w") # status file.
        settingsfile.write(str(position1)+"\n"+str(position2)+"\n")
        for lines in otherinfo:
            settingsfile.write(lines)
        settingsfile.close()

    draw_settings_screen(screen,menuGraphics,window_width,window_height)
    runsettings = True
    while runsettings: # Run normally until player hits space.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If 'x' button selected, end
                return 'stop'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and position3 == 1: # pos 3 reflects
                    position3 = 0                               # active indicator
                elif event.key == pygame.K_DOWN and position3 == 0:
                    position3 = 1
                elif event.key == pygame.K_LEFT:
                    if position3 == 0:
                        if position1 > 0:
                            position1 -= 1
                    elif position3 == 1:
                        if position2 > 0:
                            position2 -= 1
                    draw_settings_screen(screen,menuGraphics,window_width,window_height)
                elif event.key == pygame.K_RIGHT:
                    if position3 == 0:
                        if position1 < len(positionslist1):
                            position1 += 1
                    elif position3 == 1:
                        if position2 < len(positionslist2):
                            position2 += 1
                    draw_settings_screen(screen,menuGraphics,window_width,window_height)
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    updatesettingsfile()
                    runsettings = False
