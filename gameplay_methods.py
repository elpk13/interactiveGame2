# Imports and initializations
import pygame
import random
import os
import math
import dialog
from elements import *
import bisect

pygame.init()

#set the parameters for the pygame window
height = 900 # Set the dimensions of the screen, which determines how
width = 1200 # much of the world is shown.
screen = pygame.display.set_mode((width,height))
halfheight = height/2
halfwidth = width/2

# World size determined by dimensions of background image.
background = pygame.image.load(os.path.join('Assets',"map_background.jpg"))
worldx = background.get_width()
worldy = background.get_height()
uppery = worldy - halfheight
upperx = worldx - halfwidth
#print(uppery)
#print(upperx)

worlddata = (worldx,worldy,width,height)

def getCharacter(): # Returns list of framelists for four animations and name.

    settingsfile = open("settings.txt","r") # Retrieve current status of settings
    currentsettings = settingsfile.readlines() # from settings file.
    charid = int(currentsettings[2][0])
    settingsfile.close() # Choose character and name.
    charactername = ['Aspen','Khewa','Mani','Nico','Sparrow','Timber'][charid]

    pframers = [] # Form list of animations.  One for right-walking, one for
    pframels = [] # left-walking, one up, one down.
    pframeus = [] # Each starts with standing and loops from the third frame.
    pframeds = []
    for f in range(1,9):
        frame = pygame.image.load(os.path.join('Animations',charactername,charactername + '_Walking_Right000' + str(f) + '.png'))
        frame = pygame.transform.scale(frame,(int(height*frame.get_width()/(9*frame.get_height())),int(height/9)))
        pframers.append(frame)
        frame = pygame.transform.flip(frame,True,False)
        pframels.append(frame)
        frame = pygame.image.load(os.path.join('Animations',charactername,charactername + '_Walking_Forward000' + str(f) + '.png'))
        frame = pygame.transform.scale(frame,(int(height*frame.get_width()/(9*frame.get_height())),int(height/9)))
        pframeus.append(frame)
        frame = pygame.image.load(os.path.join('Animations',charactername,charactername + '_walking_Away000' + str(f) + '.png'))
        frame = pygame.transform.scale(frame,(int(height*frame.get_width()/(7*frame.get_height())),int(height/7)))
        pframeds.append(frame)

    if charactername == "Mani":
        charactername = "Máni"  # Accent mark not in filename.

    return [pframers,pframels,pframeus,pframeds,charactername]

def getworldgraphics(height): # Where height is the height of the world, used to scale images.
    # Load all graphics for world features.
    bisonImage = pygame.image.load(os.path.join('Assets_poc',"temp_bison_print.png"))
    bisonImage = pygame.transform.scale(bisonImage,(int(height/15),int(height/15)))
    rabbitImage = pygame.image.load(os.path.join('Assets_poc',"rabbit print.png"))
    rabbitImage = pygame.transform.scale(rabbitImage,(int(height/10),int(height/10)))
    deerImage = pygame.image.load(os.path.join('Assets_poc',"deer print.png"))
    deerImage = pygame.transform.scale(deerImage,(int(height/15),int(height/10)))
    printImages = [[bisonImage],[rabbitImage],[deerImage]]
    printTypeCollideBoxes = []
    for imagelist in printImages:
        printTypeCollideBoxes.append((0,0,imagelist[0].get_width(),imagelist[0].get_height()))

    obstacleImages = [[pygame.image.load(os.path.join('Assets',"pine_tree.png")),
    pygame.image.load(os.path.join('Assets',"pine_tree.png")),
    pygame.image.load(os.path.join('Assets',"pine_tree.png"))],[pygame.image.load(os.path.join('Assets',"oak_tree.png")),
    pygame.image.load(os.path.join('Assets',"oak_tree.png")), # Yes, that has to be that way.
    pygame.image.load(os.path.join('Assets',"oak_tree.png"))],
    [pygame.image.load(os.path.join('Assets','farm.png')),
    pygame.image.load(os.path.join('Assets','farm.png')),
    pygame.image.load(os.path.join('Assets','farm.png'))]]
    obstacleNightImages = [[pygame.image.load(os.path.join('Assets',"pine_tree_light.png")),
    pygame.image.load(os.path.join('Assets',"pine_tree_light.png")),
    pygame.image.load(os.path.join('Assets',"pine_tree_light.png"))],
    [pygame.image.load(os.path.join('Assets',"oak_tree_light.png")),
    pygame.image.load(os.path.join('Assets',"oak_tree_light.png")),
    pygame.image.load(os.path.join('Assets',"oak_tree_light.png"))],
    [pygame.image.load(os.path.join('Assets','farm.png')),
    pygame.image.load(os.path.join('Assets','farm.png')),
    pygame.image.load(os.path.join('Assets','farm.png'))]]
    obstacleTypeCollideBoxes = []
    for imagelist in obstacleImages:
        imageh, imagew = imagelist[0].get_height(), imagelist[0].get_width()
        if obstacleImages.index(imagelist) != len(obstacleImages) - 1: # For trees, use these measures.
            obstacleTypeCollideBoxes.append((0.4*imagew,0.8*imageh,0.6*imagew,0.9*imageh))
        else:
            obstacleTypeCollideBoxes.append((0,0,imagew,imageh))
    # Alternative to above, in case we want more tree types and a varying sample.
    #treeTypes = ['oak','pine','birch','ash','walnut','sycamore','tulip']
    #numTreeTypes = random.randint(5,7)
    #treeChoices = random.sample(treeTypes,numTreeTypes)
    #obstacleImages = []
    #obstacleNightImages = []
    #for tree in treeChoices:
#        obstacleImages.append([pygame.image.load(os.path.join('Assets',tree+'_tree.png'))])
#        obstacleNightImage.append([pygame.image.load(os.path.join('Assets',tree+'tree_light.png'))])
    #obstacleImages.append([pygame.image.load(os.path.join('Assets','farm.png'))])
    #obstacleNightImages.append([pygame.image.load(os.path.join('Assets','farm_light.png'))])
    #obstacleTypeCollideBoxes = []
    #for imagelist in obstacleImages:
    #    imageh, imagew = imagelist[0].get_height(), imagelist[0].get_width()
    #    if obstacleImages.index(imagelist) < numTreeChoices: # For trees, use these measures.
    #        obstacleCollideBoxes.append((0.4*imagew,0.8*imageh,0.6*imagew,imageh))
    #    else:
    #        obstacleCollideBoxes.append((0,0,imagew,imageh))

    passableImages = [[pygame.image.load(os.path.join('Assets',"grass1.png")),
    pygame.image.load(os.path.join('Assets',"grass2.png"))],
    [pygame.image.load(os.path.join('Assets','sheep.png')),
    pygame.image.load(os.path.join('Assets','sheep_down.png'))]]
    passableNightImages = passableImages
    # Alternative to above, in case passable objects get night graphics.
    #passableNightImages = [[pygame.image.load(os.path.join('Assets',"grass1_light.png")),
    #pygame.image.load(os.path.join('Assets',"grass2_light.png"))],
    #[pygame.image.load(os.path.join('Assets','sheep_light.png')),
    #pygame.image.load(os.path.join('Assets','sheep_down_light.png'))]]

    return printImages, printTypeCollideBoxes, obstacleImages, obstacleNightImages, obstacleTypeCollideBoxes, passableImages, passableNightImages

def getworldfeatures(worldx,worldy,printImages,obstacleImages,passableImages,worlddata):

    # Locate random array of footprints around the map.
    printData = []
    for i in range(50*len(printImages)):
        printData.append([random.randint(0,len(printImages)-1),(random.randint(0,worldx),random.randint(0,worldy))])
    printData.sort(key=lambda x: x[1][1])
    printTypes = []
    printLocations = []
    for p in printData:
        printTypes.append(p[0])
        printLocations.append(p[1])

# Populate the world with arbitrary obstacles of assorted types and sizes.
    obstacleData = []
    for i in range(100):
        obstacleData.append([random.randint(0,len(obstacleImages)-2),(random.randint(0,worldx),random.randint(0,worldy)),0])
        obstacleData[-1][2] = random.randint(0,len(obstacleImages[obstacleData[-1][0]])-1)
    farmPic = obstacleImages[-1][0]
    farmLocation = random.choice([(0,0),
    (worldx-farmPic.get_width(),0),(0,worldy-farmPic.get_height()),
    (worldx-farmPic.get_width(),worldy-farmPic.get_height())])
    obstacleData.append([len(obstacleImages)-1,farmLocation,0])
    obstacleData.sort(key=lambda x: x[1][1])
    obstacleTypes = []
    obstacleLocations = []
    obstacleOffsets = []
    for o in obstacleData:
        obstacleTypes.append(o[0])
        obstacleLocations.append(o[1])
        obstacleOffsets.append(o[2])

    passableData = []
    for i in range(200):
        passableData.append([random.randint(0,len(passableImages)-2),(random.randint(0,worldx),random.randint(0,worldy)),0])
        passableData[-1][2] = random.randint(0,len(passableImages[passableData[-1][0]])-1)
    farmrectangle = (0.5,0.3,0.9,0.9)
    sheepPen = (farmLocation[0]+farmrectangle[0]*farmPic.get_width(),
    farmLocation[1]+farmrectangle[1]*farmPic.get_height(),
    (farmrectangle[2]-farmrectangle[0])*farmPic.get_width(),
    (farmrectangle[3]-farmrectangle[1])*farmPic.get_height())
    for i in range(5):
        passableData.append([len(passableImages)-1,(int(sheepPen[0]+random.random()*sheepPen[2]),int(sheepPen[1]+random.random()*sheepPen[3])),0])
        passableData[-1][2] = random.randint(0,len(passableImages[passableData[-1][0]])-1)
    passableData.sort(key=lambda x: x[1][1])
    passableTypes = []
    passableLocations = []
    passableOffsets = []
    for p in passableData:
        passableTypes.append(p[0])
        passableLocations.append(p[1])
        passableOffsets.append(p[2])

    return obstacleTypes, obstacleLocations, obstacleOffsets, printTypes, printLocations, passableTypes, passableLocations, passableOffsets, sheepPen

# When player is nearby, the sheep are shuffled around within the sheep pen.
def moveSheep(passableTypes,passableLocations,passableOffsets,sheepPen):
    # ideal use: passableTypes, passableLocations, passableOffsets = moveSheep(passableTypes, passableLocations, passableOffsets, sheepPen)
    sheepType = max(passableTypes) # easier than passing the image list and getting its length - 1
    for e in range(len(passableTypes)):
        if passableTypes[e] == sheepType:
            newsheepx = passableLocations[e][0] + random.random()*10 - 5
            newsheepy = passableLocations[e][1] + random.random()*10 - 5
            if sheepPen[0] < newsheepx < sheepPen[0] + sheepPen[2]:
                passableLocations[e][0] = newsheepx
            if sheepPen[1] < newsheepx < sheepPen[0] + sheepPen[3]:
                passableLocations[e][1] = newsheepy
            if random.random() > 0.8:
                passableOffsets[e] = random.randint(0,1)
    return passableTypes, passableLocations, passableOffsets

# For moving the player, this function determines whether any point is within
# an obstacle's blit box.  For multiple barriers, consider passing a list argument
# containing a list of tuples which are lists of coordinates and the object corresponding
# to each list.
def posok(x,y,obstacleLocations,obstacleTypes,obstacleTypeCollideBoxes,worlddata):
    #worlddata = (worldx,worldy,width,height)
    if not ( worlddata[2] / 2 < x and x < worlddata[0] - worlddata[2] / 2 ) :
        return False
    if not ( worlddata[3] / 2 < y and y < worlddata[1] - worlddata[3] / 2 ) :
        return False
    for ob in range(len(obstacleLocations)):
        if obstacleTypeCollideBoxes[obstacleTypes[ob]][0] < x - obstacleLocations[ob][0] < obstacleTypeCollideBoxes[obstacleTypes[ob]][2] and obstacleTypeCollideBoxes[obstacleTypes[ob]][1] < y - obstacleLocations[ob][1] < obstacleTypeCollideBoxes[obstacleTypes[ob]][3]:
            return False
    else:
        return True

def printCol(x,y,printLocations,printTypes,printTypeCollideBoxes):
    for ob in range(len(printLocations)):
        if printTypeCollideBoxes[printTypes[ob]][0] < x - printLocations[ob][0] < printTypeCollideBoxes[printTypes[ob]][2] and printTypeCollideBoxes[printTypes[ob]][1] < y - printLocations[ob][1] < printTypeCollideBoxes[printTypes[ob]][3]:
            return ob + 1 #Evaluates to True no matter what.
    else:
        return False

def isNight(frames):
    if (frames % 600) > 300:
        return True
    return False

# This function contains code that was in drawscreen() but only needs to run at the beginning.
def prepgraphics(printLocations,printTypes,printImages,obstacleLocations,obstacleTypes,obstacleImages,obstacleNightImages,obstacleOffsets,passableLocations,passableTypes,passableImages,passableNightImages,passableOffsets):

    allImageLists = printImages + obstacleImages + passableImages
    allNightImages = printImages + obstacleNightImages + passableNightImages
    allTypeOffsetRanges = []
    for imagelist in allImageLists:
        allTypeOffsetRanges.append(len(imagelist))

    allLocations = printLocations + obstacleLocations + passableLocations
    allTypes = printTypes + [] # Yes, that has to be that way; else they alias.
    typenumbuffer = len(printImages)
    for it in obstacleTypes:
        allTypes.append(it+typenumbuffer)
    typenumbuffer += len(obstacleImages)
    for it in passableTypes:
        allTypes.append(it+typenumbuffer)
    allOffsets = [0]*len(printTypes) + obstacleOffsets + passableOffsets
    allYs = []
    for y in range(len(allLocations)):
        allYs.append(allLocations[y][1] + allImageLists[allTypes[y]][0].get_height())

    allWorldData = []
    for a in range(len(allLocations)):
        allWorldData.append([allTypes[a],allLocations[a],allOffsets[a],allYs[a]])
    allWorldData.sort(key=lambda x:x[3])
    for a in range(len(allWorldData)):
        allTypes[a] = allWorldData[a][0]
        allLocations[a] = allWorldData[a][1]
        allOffsets[a] = allWorldData[a][2]
        allYs[a] = allWorldData[a][3]

    return allImageLists, allNightImages, allTypeOffsetRanges, allLocations, allTypes, allOffsets, allYs
    # allImageLists is a list of lists of animation frames, one list for every object, in order by type (prints, then obstacles, then passables)
    # allNightImages is the same for night versions
    # allTypeOffsetRanges gives the length of the animation of each type of object
    # allLocations is a list of tuples giving the location of the UPPER LEFT corner of every object's blit box.
    # allTypes is a list of numbers indicating what type of object each in allLocations is.
    # allY's is the y-coordinate of the BOTTOM of each object, used to find blit order.

# The familiar drawscreen method places the relevant part of the background
# over the screen, then superlays obstacles, then places the relevant frame
# of the player.
def drawscreen(screen,height,width,background,timelapsed,playerx,playery,allImageLists,allNightImages,allTypeOffsetRanges,allLocations,allYs,allTypes,allOffsets,framelists,currentmode,currentframe,health):
    screen.blit(background,(0,0),(int(playerx-width/2),int(playery-height/2),width,height))
    playerimage = framelists[currentmode][currentframe]
    ydiff = playerimage.get_height()/2

    firstob = bisect.bisect(allYs,playery+ydiff-height/2-200)
    middleob = bisect.bisect(allYs,playery+ydiff)
    lastob = bisect.bisect(allYs,playery+ydiff+height/2+200) - 1 # Arbitrary extension to keep things from disappearing at bottom.

    if isNight(timelapsed):
        for ob in range(firstob,middleob):
            screen.blit(allNightImages[allTypes[ob]][(timelapsed+allOffsets[ob])%allTypeOffsetRanges[allTypes[ob]]], (int(allLocations[ob][0]-playerx+width/2),int(allLocations[ob][1]-playery+height/2)))
        screen.blit(playerimage,(int(width/2-playerimage.get_width()/2),int(height/2-playerimage.get_height()/2)))
        for ob in range(middleob,lastob):
            screen.blit(allNightImages[allTypes[ob]][(timelapsed+allOffsets[ob])%allTypeOffsetRanges[allTypes[ob]]], (int(allLocations[ob][0]-playerx+width/2),int(allLocations[ob][1]-playery+height/2)))
    else:
        for ob in range(firstob,middleob):
            screen.blit(allImageLists[allTypes[ob]][(timelapsed+allOffsets[ob])%allTypeOffsetRanges[allTypes[ob]]], (int(allLocations[ob][0]-playerx+width/2),int(allLocations[ob][1]-playery+height/2)))
        screen.blit(playerimage,(int(width/2-playerimage.get_width()/2),int(height/2-playerimage.get_height()/2)))
        for ob in range(middleob,lastob):
            screen.blit(allImageLists[allTypes[ob]][(timelapsed+allOffsets[ob])%allTypeOffsetRanges[allTypes[ob]]], (int(allLocations[ob][0]-playerx+width/2),int(allLocations[ob][1]-playery+height/2)))

    healthBarRect = pygame.Rect(int(5*width/6 - height/24),int(11*height/12),int(width*health/600),int(height/24))
    healthBarOutline = pygame.Rect(int(5*width/6 - height/24 - width/300),int(11*height/12 - width/300),int(width/6 + width/150),int(height/24 + width/150))
    pygame.draw.rect(screen,(255,255,255),healthBarOutline)
    pygame.draw.rect(screen,(255,0,0),healthBarRect)
    pygame.display.update()

# The following functions retrieve and set the health value to and from
# the settings file.
def readHealth():
    settingsfile = open("settings.txt","r")
    health = int(settingsfile.readlines()[3])
    settingsfile.close()
    return health

def writeHealth():
    settingsfile = open("settings.txt","r")
    sets = settingsfile.readlines()
    settingsfile.close()
    sets[3] = ''.join([str(health),"\n"])
    settingsfile = open("settings.txt","w")
    settingsfile.writelines(sets)
    settingsfile.close()

# Get character

framelists = getCharacter()
# The current frame in any list is stored in the list current frames.
# Currentmode refers to which direction the player is depicted facing.
currentframe = 0
currentmode = 0

hoofprint = 0
pos_hoofprint_visited = {}

# Retrieve graphics.
printImages, printTypeCollideBoxes, obstacleImages, obstacleNightImages, obstacleTypeCollideBoxes, passableImages, passableNightImages = getworldgraphics(height)
# Generate world.
obstacleTypes, obstacleLocations, obstacleOffsets, printTypes, printLocations, passableTypes, passableLocations, passableOffsets, sheepPen = getworldfeatures(worldx,worldy,printImages,obstacleImages,passableImages,worlddata)
# Prepare world to be drawn.
allImageLists, allNightImages, allTypeOffsetRanges, allLocations, allTypes, allOffsets, allYs = prepgraphics(printLocations,printTypes,printImages,obstacleLocations,obstacleTypes,obstacleImages,obstacleNightImages,obstacleOffsets,passableLocations,passableTypes,passableImages,passableNightImages,passableOffsets)
# Pick random point where player starts.  Assume dimensions of map are greater
# than screen, else an error will occur.  Move the player to an acceptable
# position before starting.
playerx = random.randint(width/2,worldx-width/2)
playery = random.randint(height/2,worldy-height/2)
while not posok(playerx,playery,obstacleLocations,obstacleTypes,obstacleTypeCollideBoxes,worlddata):
    playerx = random.randint(width/2,worldx-width/2)
    playery = random.randint(height/2,worldy-height/2)
speed = 10 # pixels by which player moves in a frame
frametime = 100 # milliseconds of each frame

runninggame = True
timelapsed = 0 # frames, ticks, tenths of a second
health = readHealth() # In the first game, this should read "health = 100"

drawscreen(screen,height,width,background,timelapsed,playerx,playery,allImageLists,allNightImages,allTypeOffsetRanges,allLocations,allYs,allTypes,allOffsets,framelists,currentmode,currentframe,health)

while runninggame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If 'x' button selected, end
            runninggame = False
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
    if posok(newposx,newposy,obstacleLocations,obstacleTypes,obstacleTypeCollideBoxes,worlddata):
        playerx,playery = newposx,newposy # Player position changes;
    # Newpos variables now reflect current position.
    col = printCol(newposx,newposy,printLocations,printTypes,printTypeCollideBoxes)
    if col:
        allLocations[allLocations.index(printLocations[col-1])] = (0,-100) # If col, relocate the print in both lists
        printLocations[col-1] = (0,-100) # to where it won't blit.
        resp = dialog.dialog(screen,"What would you like to do about the print that was found?",['Howl for the pack - Group Hunt','Hunt alone','Run Away','Ignore'],printImages[printTypes[col-1]][0])
        if resp == 0:
            # Pack hunt
            # Let's go hunt do do do do do do do, let's go hunt do do do do do do do
            drawscreen(screen,height,width,background,timelapsed,playerx,playery,allImageLists,allNightImages,allTypeOffsetRanges,allLocations,allYs,allTypes,allOffsets,framelists,currentmode,currentframe,health)
        elif resp == 1:
            # Solo hunt - import cyc here?
            # Let's go hunt do do do do do do do, let's go hunt!
            drawscreen(screen,height,width,background,timelapsed,playerx,playery,allImageLists,allNightImages,allTypeOffsetRanges,allLocations,allYs,allTypes,allOffsets,framelists,currentmode,currentframe,health)
        elif resp == 2:
            # Run away do do do do do do do ...
            drawscreen(screen,height,width,background,timelapsed,playerx,playery,allImageLists,allNightImages,allTypeOffsetRanges,allLocations,allYs,allTypes,allOffsets,framelists,currentmode,currentframe,health)
        else:
            drawscreen(screen,height,width,background,timelapsed,playerx,playery,allImageLists,allNightImages,allTypeOffsetRanges,allLocations,allYs,allTypes,allOffsets,framelists,currentmode,currentframe,health)
    if dist > 0: # If player moves, update animation frame in list.
        if currentframe != len(framelists[currentmode]) - 1:
            currentframe += 1
        else:
            currentframe = 2 # Reset to third frame to loop
    else:
        currentframe = 0 # If player doesn't move, return to

# Fix moveSheep() before uncommenting belove lines.
#    if timelapsed % 3 == 0 and (farmLocation[0] - playerx) ** 2 + (farmLocation[1] - playery) ** 2 < height ** 2 + width ** 2:
#        moveSheep() # If player is near farm, move the sheep.
    pygame.time.delay(frametime)
    timelapsed += 1
    if timelapsed % 600 == 0:
        background = pygame.image.load(os.path.join('Assets','map_background.jpg'))
    elif timelapsed % 300 == 0:  # 'Light' refers to the dark version, because the function
        background = pygame.image.load(os.path.join('Assets','map_background_light.jpg'))
    drawscreen(screen,height,width,background,timelapsed,playerx,playery,allImageLists,allNightImages,allTypeOffsetRanges,allLocations,allYs,allTypes,allOffsets,framelists,currentmode,currentframe,health)
