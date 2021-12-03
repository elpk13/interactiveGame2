# Imports and initializations
import pygame
import random
import os
import math
import dialog
from elements import *
import bisect
from enum import Enum
from classes import *

pygame.init()

# The readglobals() method produces a dictionary of the global
# values found in globals.txt.  This allows us to label the
# values in the file.
def readglobals():
    globalinfo = { }
    globefile = open("globals.txt")
    for eachline in globefile.readlines()[1:]:
        param, val, comm = eachline.split('|')
        param, val = param.strip(), val.strip()
        if 'int' in comm:
            globalinfo[param] = int(val)
        elif 'float' in comm:
            globalinfo[param] = float(val)
        else:
            globalinfo[param] = val
    globefile.close()
    return globalinfo

def makescreen(): # Makes a screen per size in globals.txt
    return pygame.display.set_mode((readglobals()['window_width'],readglobals()['window_height']))

# A helper method for drawScreen.
def drawStream(screen,stream,playerx,playery,window_width,window_height,time,night,scroll=True,leftx=0,topy=0):
    for segment in stream:
        if abs(segment.xpos - playerx) < window_width and abs(segment.ypos - playery) < window_height:
            if night:
                appearance = segment.nightappearance[time % len(segment.nightappearance)]
            else:
                appearance = segment.appearance[time % len(segment.appearance)]
            if scroll:
                screen.blit(appearance,(int(segment.xpos-playerx+window_width/2),int(segment.ypos-playery+window_height/2)))
            else:
                screen.blit(appearance,(segment.xpos-leftx,segment.ypos-topy))

def getYbaselist(objectlist): # Because I can't use a key in bisect, I have to use
    ybaselist = [] # this function to tell what is in front of and behind the
    for obj in objectlist: # player.  This is fixed in Python 3.10, but pygame
        ybaselist.append(obj.ybase) # isn't.
    return ybaselist

# Method to draw the game screen for a given world, window, character,
# location, and all other information.
def drawScreen(screen,width,height,characterappearance,playerx,playery,world,ybaselist,time,night,health,currentmode,currentframe):
    ybaselist = getYbaselist(world.objectsofheight) # Recalculate each time?  Oh well.

    # Get player, use to find which objects to blit above and below.
    playerimage = characterappearance[currentmode][currentframe]
    ydiff = playerimage.get_height()//2
    firstob = bisect.bisect(ybaselist,playery+ydiff-height)
    middleob = bisect.bisect(ybaselist,playery+ydiff)
    lastob = bisect.bisect(ybaselist,playery+ydiff+height)
    # Blit correct background
    if night:
        screen.blit(world.nightbackground,(0,0),(int(playerx-width/2),int(playery-height/2),width,height))
    else:
        screen.blit(world.background,(0,0),(int(playerx-width/2),int(playery-height/2),width,height))
    # Everything else takes night as a variable.
    for stream in world.streams:
        drawStream(screen,stream,playerx,playery,width,height,time,night)
    for o in range(firstob,middleob):
        if playerx - width < world.objectsofheight[o].xpos < playerx + width:
            world.objectsofheight[o].draw(screen,playerx,playery,width,height,night,time)
    screen.blit(playerimage,(int(width/2-playerimage.get_width()/2),int(height/2-playerimage.get_height()/2)))
    for o in range(middleob,lastob):
        if playerx - width < world.objectsofheight[o].xpos < playerx + width:
            world.objectsofheight[o].draw(screen,playerx,playery,width,height,night,time)
    # Health bar
    healthBarRect = pygame.Rect(int(5*width/6 - height/24),int(11*height/12),int(width*health/600),int(height/24))
    healthBarOutline = pygame.Rect(int(5*width/6 - height/24 - width/300),int(11*height/12 - width/300),int(width/6 + width/150),int(height/24 + width/150))
    pygame.draw.rect(screen,(255,255,255),healthBarOutline)
    pygame.draw.rect(screen,(255,0,0),healthBarRect)
    # Only drawScreen() can update the display.
    pygame.display.update()

# Deprecated methods from testing
#def drawForest(screen,forest,playerx,playery,window_width,window_height,time):
#    currentmode = treemode(time)
#    currentframe = time % 7
#    for everytree in forest:
#        if everytree.xpos + everytree.width + window_width/2 > playerx and everytree.xpos - window_width/2 < playerx and everytree.ypos - window_height/2 < playery and everytree.ybase + window_height/2 > playery:
#            if everytree.evergreen:
#                screen.blit(everytree.appearance[currentmode % 2][currentframe],(int(everytree.xpos-playerx+window_width/2),int(everytree.ypos-playery+window_height/2)))
#            else:
#                screen.blit(everytree.appearance[currentmode][currentframe],(int(everytree.xpos-playerx+window_width/2),int(everytree.ypos-playery+window_height/2)))
#
# When player is nearby, the sheep are shuffled around within the sheep pen.

# Posok() has become two functions - posinworld() lets Akela warn the player
# about leaving the pack's territory; posok() is just for obstacles.

def posinworld(x,y,worldx,worldy,window_width,window_height):
    if window_width/2 < x < worldx - window_width/2 and window_height/2 < y < worldy - window_height/2:
        return True
    return False

def posok(x,y,obstacles):
    for ob in obstacles:
        if ob.collidesat(x,y):
            return False
    else:
        return True

def intCol(x,y,interactives):
    for ob in interactives:
        if ob.covers(x,y):
            return ob # The object that triggers the collision is returned.
    else:
        return False

#def drawscreen_bare(screen,window_width,window_height,background,playerx,playery,framelists,currentmode,currentframe,streams,forests,time):
#    screen.blit(background,(0,0),(int(playerx-window_width/2),int(playery-window_height/2),window_width,window_height))
#    for stream in streams:
#        drawStream(screen,stream,playerx,playery,window_width,window_height,time)
#    for forest in forests:
#        drawForest(screen,forest,playerx,playery,window_width,window_height,time)
#
#    playerimage = framelists[currentmode][currentframe]
#    screen.blit(playerimage,(window_width//2-playerimage.get_width()//2,window_height//2-playerimage.get_height()//2))
#    pygame.display.update()

# The following functions retrieve and set the health value to and from
# the settings file.
def readHealth():
    settingsfile = open("settings.txt","r")
    health = int(settingsfile.readlines()[3])
    settingsfile.close()
    return health

def writeHealth(health):
    settingsfile = open("settings.txt","r")
    sets = settingsfile.readlines()
    settingsfile.close()
    sets[3] = ''.join([str(health),"\n"])
    settingsfile = open("settings.txt","w")
    settingsfile.writelines(sets)
    settingsfile.close()

def getCharacterData(wolfGraphics):
    settingsfile = open("settings.txt","r") # Retrieve current status of settings
    currentsettings = settingsfile.readlines() # from settings file.
    charid = int(currentsettings[2][0])
    settingsfile.close() # Choose character and name.
    charname = ['Aspen','Khewa','Máni','Nico','Sparrow','Timber'][charid]
    charappearance = wolfGraphics[charname]
    return charname, charappearance

def addAnimal(world, animalGraphics):
    x, y = random.randint(0,world.width), random.randint(0,world.height)
    while not posok(x, y, world.obstacles):
        x, y = random.randint(0,world.width), random.randint(0,world.height)
    appearance = animalGraphics['rabbit']
    newAnimal = Animal(x,y,appearance[0].get_width(),appearance[0].get_height(),appearance,'rabbit',5)
    world.animals.append(newAnimal)
    world.objectsofheight.append(newAnimal)
    world.interactives.append(newAnimal)
