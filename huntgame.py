# Chapter 1
# Featuring a young wolf who is new to the world.

from worldgeneration import *
from gamethods import *
import random
import dialog

import pygame
pygame.init()

# Currently, this function is called at the bottom of the script, so that the
# script can run for itself.

def run_hunting_game(screen,borders,huntworld,time,night,framelists,wolfGraphics,training=False): # All in function, so can run from other screen.
    globinfo = readglobals() # We will soon add screen, etc. to function arguments
    window_width = globinfo['window_width']
    window_height = globinfo['window_height']

    # Below is the getWorldGraphics function.  Ideally, this would only run once,
    # and not repeat for every chapter.  Move into arguments called to run_first_chapter()
    # when we get a chance.
    ybaselist = getYbaselist(huntworld.objectsofheight)

    playerx = int((borders[0]+borders[1])/2)
    playery = int((borders[2]+borders[3])/2)

    currentmode = 0
    currentframe = 0

    health = readHealth()
    timelapsed = time
    frame_time = globinfo['frame_time']

    packkills = []

    drawHuntScreen(screen,window_width,window_height,framelists,playerx,playery,borders,huntworld,ybaselist,timelapsed,night,health,currentmode,currentframe)

    if training:
        dialog.akela(screen,"Look for, and catch, the prey.  Remember, you can hold the select key to run.")
        dialog.dialog(screen,"Akela",["Prey looks like this:"],huntworld.animals[0].appearance[0][0])

    while True: # End the loop by returning something
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If 'x' button selected, end
                inchapter = False
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
        if dist > 0: # If player moves, update animation frame in list.
            if currentframe != len(framelists[currentmode]) - 1:
                currentframe += 1
            else:
                currentframe = 2 # Reset to third frame to loop
        else:
            currentframe = 0 # If player doesn't move, return to standing.

        if posok(newposx,newposy,huntworld.obstacles):
            playerx,playery = newposx,newposy # Player position changes;

        # Hunt runs until only wolves remain in area.  Player does not need to
        # kill every prey animal but does need to meet / eat meat from / each.
        if not (borders[0] < playerx < borders[1] and borders[2] < playery < borders[3]):
            if training:
                dialog.akela(screen,"You won't catch anything if you run off like that.")
            writeHealth(health)
            return 'player left'
        doesCol = intCol(newposx,newposy,huntworld.interactives)
        if doesCol:
            if isinstance(doesCol,Animal): # Should always be true.
                if isinstance(doesCol,Rabbit):  # If the player catches a rabbit, instant kill.
                    huntworld.animals.remove(doesCol)
                    huntworld.interactives.remove(doesCol)
                    huntworld.objectsofheight.remove(doesCol)
                    if training:
                        dialog.akela(screen,"You've caught a rabbit!  Enjoy your meal.")
                    packkills.append(doesCol)
                elif isinstance(doesCol,Deer): # For deer - slow kill
                    doesCol.health -= 45
                    doesCol.speed = doesCol.health*doesCol.maxspeed//100
                    if doesCol.dead:
                        huntworld.animals.remove(doesCol)
                        huntworld.interactives.remove(doesCol)
                        huntworld.objectsofheight.remove(doesCol)
                        if training:
                            dialog.akela(screen,"We've killed a deer!  Enjoy the meal.")
                        packkills.append(doesCol)
                elif isinstance(doesCol,Bison): # For bison - rapid death
                    health -= 80
            elif isinstance(intCol,list): # Code for other interactives - like the den - go here.
                pass
        if health <= 0:
            return 'player died' # If player dies, end so immediately.

        drawHuntScreen(screen,window_width,window_height,framelists,playerx,playery,borders,huntworld,ybaselist,timelapsed,night,health,currentmode,currentframe)
        pygame.time.delay(frame_time)
        timelapsed += 1
        huntworld.turn()

        preyalldead = True
        preyingame = False
        for eachanimal in huntworld.animals:
            if isinstance(eachanimal,Wolf):
                pass
            else:
                if eachanimal.health <= 0:
                    if training:
                        dialog.akela(screen,f"Great!  The pack killed a {eachanimal.species}!")
                    huntworld.animals.remove(eachanimal)
                    huntworld.interactives.remove(eachanimal)
                    huntworld.objectsofheight.remove(eachanimal)
                    packkills.append(eachanimal)
                elif not (borders[0] < eachanimal.xpos < borders[1] and borders[2] < eachanimal.ypos < borders[3]):
                    preyalldead = False
                    if training:
                        dialog.akela(screen,f"It looks like one {eachanimal.species} escaped.")
                    huntworld.animals.remove(eachanimal)
                    huntworld.interactives.remove(eachanimal)
                    huntworld.objectsofheight.remove(eachanimal)
                else:
                    preyalldead = False
                    preyingame = True
        if preyalldead:
            if training:
                dialog.akela(screen,"Another successful hunt!")
            for scavengeable in packkills:
                health += scavengeable.maxstrength / (len(huntworld.animals)+1)
            if health > 100:
                health = 100
            writeHealth(health)
            return 'success'
        elif not preyingame:
            if training:
                dialog.akela(screen,"We'll catch some next time.")
            for scavengeable in packkills:
                health += scavengeable.maxstrength / (len(huntworld.animals)+1)
            if health > 100:
                health = 100
            writeHealth(health)
            return 'prey escaped'
