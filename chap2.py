# Chapter 1
# Featuring a young wolf who is new to the world.

from worldgeneration import *
from gamethods import *
import random
import dialog
import pygame


def run_second_chapter(screen, worldx, worldy, background, nightbackground, wolfGraphics, streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim, streamCurveCoefficients, treeGraphics, treeNightGraphics, treeGreenness, rockGraphics, rockNightGraphics, decorGraphics, decorNightGraphics, decorDynamics, printGraphics, printGraphicsSmall, miscellaneousGraphics, miscellaneousNightGraphics, animalTypes, animalGraphics):
    globinfo = readglobals()
    window_width = globinfo['window_width']
    window_height = globinfo['window_height']

    # Make a world for this chapter.
    chapterworld = generateWorld(worldx,worldy,window_width,window_height,background, nightbackground, streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim, streamCurveCoefficients, treeGraphics, treeNightGraphics, treeGreenness, rockGraphics, rockNightGraphics, decorGraphics, decorNightGraphics, decorDynamics, printGraphicsSmall, miscellaneousGraphics, miscellaneousNightGraphics, animalGraphics)
    ybaselist = getYbaselist(chapterworld.objectsofheight)

    charname, framelists = getCharacterData(wolfGraphics)

    inchapter = True
    metworldedge = False
    metprey = False
    metpredator = False
    metignore = False
    metperson = False

    foundnewpack = False

    playerx = random.randint(0,worldx)
    playery = random.randint(0,worldy)
    while not (posok(playerx,playery,chapterworld.obstacles) and posinworld(playerx,playery,worldx,worldy,window_width,window_height)):
        playerx = random.randint(0,worldx)
        playery = random.randint(0,worldy)

    currentmode = 0
    currentframe = 0

    health = 100
    writeHealth(health)
    timelapsed = 0
    night = False
    frame_time = globinfo['frame_time']

    drawScreen(screen,window_width,window_height,framelists,playerx,playery,chapterworld,ybaselist,timelapsed,night,health,currentmode,currentframe)
    dialog.akela(screen,"This is the second phase.")

    while inchapter:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If 'x' button selected, end
                return 'stop'
        pressed = pygame.key.get_pressed() # This method of movement checking
        newposx = playerx                  # considers all keys which may be
        newposy = playery                  # pressed at the end of a tick/frame.
        if pressed[pygame.K_RIGHT]:
            newposx += 1
        if pressed[pygame.K_LEFT]:
            newposx -= 1
        if pressed[pygame.K_UP]:
            newposy -= 1
        if pressed[pygame.K_DOWN]:
            newposy += 1
        if pressed[pygame.K_RETURN]:
            speed = 40
        else:
            speed = 10
        # Newpos variables currently indicate only the direction of motion as a
        # vector of variable magnitude.
        dist = ((newposx-playerx)**2 + (newposy-playery)**2) ** 0.5
        if dist > 0:
            newposx = playerx + (newposx - playerx)*speed/dist
            newposy = playery + (newposy - playery)*speed/dist
        # Newpos variables now indicate the desired position of the player in the
        # next frame.
            if newposx > playerx:   # When choosing the direction to face the
                currentmode = 0     # player, left and right are prioritized for
            elif newposx < playerx: # diagonals, as in the Champion Island game.
                currentmode = 1
            elif newposy > playery:
                currentmode = 2
            elif newposy < playery:
                currentmode = 3
        if posok(newposx,newposy,chapterworld.obstacles) and posinworld(newposx,newposy,worldx,worldy,window_width,window_height):
            playerx,playery = newposx,newposy # Player position changes;
        elif metworldedge == False and not posinworld(newposx,newposy,worldx,worldy,window_width,window_height):
            metworldedge = True
            dialog.akela(screen,"The map background is only so big.")
        # Newpos variables now reflect current position.
        doesCol = intCol(newposx,newposy,chapterworld.interactives)
        if doesCol:
            if isinstance(doesCol,Print):
                foundnewpack = True
                animal = doesCol.animal
                dialog.akela(screen,"Looks like you've found some tracks!")
                guesses = [animal]
                guesses.extend(random.sample(list(printGraphics),3))
                if guesses.count(animal) > 1:
                    guesses.remove(animal)
                random.shuffle(guesses)
                correctans = guesses.index(animal)
                specguess = dialog.dialog(screen,"What kind of tracks are these?",guesses,printGraphics[animal])
                if specguess == correctans:
                    dialog.akela(screen,"Very good!")
                else:
                    dialog.akela(screen,"Actually, those are "+animal+" tracks.")
                actions = ['hunt','ignore it','run away']
                actguess = dialog.dialog(screen,"What do you do when you see "+animal+" tracks?",actions,printGraphics[animal])
                if actguess == animalTypes[animal]:
                    dialog.akela(screen,"That's right!")
                else:
                    dialog.akela(screen,"When you see "+animal+" tracks, you should "+actions[animalTypes[animal]]+".")
                if animalTypes[animal] == 0:
                    refusehunt = dialog.dialog(screen,"Ready to hunt?",['Yes','No'],printGraphics[animal]) # Pick better image?
                    if refusehunt:
                        dialog.akela(screen,"Okay, but be sure to let me know if you find another track.")
                    else:
                        dialog.akela(screen,"Then let's go hunt together!")
                        metprey = True
                        # Connect the hunting mini-game here!!!!
                elif animalTypes[animal] == 1:
                    metignore = True
                else:
                    metpredator = True
                doesCol.xpos = -1000
                drawScreen(screen,window_width,window_height,framelists,playerx,playery,chapterworld,ybaselist,timelapsed,night,health,currentmode,currentframe)
            elif isinstance(intCol,list): # Code for other interactives - like the den - go here.
                pass

        if dist > 0: # If player moves, update animation frame in list.
            if currentframe != len(framelists[currentmode]) - 1:
                currentframe += 1
            else:
                currentframe = 2 # Reset to third frame to loop
        else:
            currentframe = 0 # If player doesn't move, return to standing.

        drawScreen(screen,window_width,window_height,framelists,playerx,playery,chapterworld,ybaselist,timelapsed,night,health,currentmode,currentframe)
        pygame.time.delay(frame_time)
        timelapsed += 1
        if timelapsed == 20: # Should be 2400 ticks per year.  Set to 20 for testing.
            inchapter = False
        elif timelapsed % 600 == 0:
            night = False
        elif timelapsed % 300 == 0:
            night = True
        if foundnewpack:
            dialog.akela(screen,"I see you've found a new pack!  I wish you well in your endeavors.")
            return dialog.dialog(screen,"What would you like to do now?",['Lead my new pack!','Return to the main menu'])
    dialog.akela(screen,"Winter came, and you did not find a new pack.  It seems you will be a lone wolf forever.")
    return 1
