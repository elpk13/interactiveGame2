# Imports and initializations
import pygame
import random
import os
import math
import dialog
from elements import *

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

# Load all player-related images.
# Player images go into four lists:  a list of right-moving frames, left-moving,
# up-moving, and down-moving.  Each can be any length.  First frame should be
# a balanced look for player, looping begins at third.
settingsfile = open("settings.txt","r") # Retrieve current status of settings
currentsettings = settingsfile.readlines() # from settings file.
charid = int(currentsettings[2][0])
settingsfile.close()
charactername = ['Aspen','Khewa','Mani','Nico','Sparrow','Timber'][charid]

# Load character graphics.  Commented lines can be uncommented when files are
# ready.  Currently, only playable character is Mani.
pframers = []
pframels = []
pframeus = []
pframeds = []
for f in range(1,9):
    charactername = 'Nico'
    frame = pygame.image.load(os.path.join('Animations',charactername + '_Walking_Right000' + str(f) + '.png'))
    frame = pygame.transform.scale(frame,(int(height*frame.get_width()/(9*frame.get_height())),int(height/9)))
    pframers.append(frame)
    frame = pygame.transform.flip(frame,True,False)
    pframels.append(frame)
    frame = pygame.image.load(os.path.join('Animations',charactername + '_Walking_Forward000' + str(f) + '.png'))
    frame = pygame.transform.scale(frame,(int(height*frame.get_width()/(9*frame.get_height())),int(height/9)))
    pframeus.append(frame)
    frame = pygame.image.load(os.path.join('Animations',charactername + '_walking_Away000' + str(f) + '.png'))
    frame = pygame.transform.scale(frame,(int(height*frame.get_width()/(7*frame.get_height())),int(height/7)))
    pframeds.append(frame)

    
# The current frame in any list is stored in the list current frames.
# Currentmode refers to which direction the player is depicted facing.
framelists = [pframers,pframels,pframeus,pframeds]
currentframe = 0
currentmode = 0

if charactername == "Mani":
    charactername = "Máni"  # Don't change until files are loaded.

hoofprint = 0
pos_hoofprint_visited = {}

# Load animal print images and locate 50 of each throghout the map.
bisonImage = pygame.image.load(os.path.join('Assets_poc',"temp_bison_print.png"))
bisonImage = pygame.transform.scale(bisonImage,(int(height/15),int(height/15)))
bisonPrints = []
for i in range(50):
    bisonPrints.append((random.randint(0,worldx),random.randint(0,worldy)))
bisonPrints.sort(key=lambda x : x[1])

rabbitImage = pygame.image.load(os.path.join('Assets_poc',"rabbit print.png"))
rabbitImage = pygame.transform.scale(rabbitImage,(int(height/10),int(height/10)))
rabbitPrints = []
for i in range(50):
    rabbitPrints.append((random.randint(0,worldx),random.randint(0,worldy)))
rabbitPrints.sort(key=lambda x : x[1])

deerImage = pygame.image.load(os.path.join('Assets_poc',"deer print.png"))
deerImage = pygame.transform.scale(deerImage,(int(height/15),int(height/10)))
deerPrints = []
for i in range(50):
    deerPrints.append((random.randint(0,worldx),random.randint(0,worldy)))
deerPrints.sort(key=lambda x : x[1])

# Populate the world with arbitrary obstacles of assorted types and sizes.
obstacleImages = [pygame.image.load(os.path.join('Assets',"pine_tree.png")),
pygame.image.load(os.path.join('Assets',"oak_tree.png"))]
obstacleNightImages = [pygame.image.load(os.path.join('Assets',"pine_tree_light.png")),
pygame.image.load(os.path.join('Assets',"oak_tree_light.png"))]
obstacleLocations = []
obstacleTypes = []
for i in range(100):
    obstacleLocations.append((random.randint(0,worldx),random.randint(0,worldy)))
    obstacleTypes.append(random.randint(0,len(obstacleImages)-1))
def takey(tup): # Sort list of obstacles so that they blit from top to bottom.
    return tup[1]
obstacleLocations.sort(key=takey)

grassImages = [pygame.image.load(os.path.join('Assets',"grass1.png")),
pygame.image.load(os.path.join('Assets',"grass2.png"))]
grassLocations = []
grassOffsets = []
for i in range(200):
    grassLocations.append((random.randint(0,worldx),random.randint(0,worldy)))
    grassOffsets.append(random.randint(0,len(grassImages)))

# Add a farm to some corner of the world.
farmPic = pygame.image.load(os.path.join('Assets','farm.png'))
sheepPics = [pygame.image.load(os.path.join('Assets','sheep.png')),
pygame.image.load(os.path.join('Assets','sheep_down.png'))]
farmLocation = random.choice([(0,0,farmPic.get_width(),farmPic.get_height()),
(worldx-farmPic.get_width(),0,worldx,farmPic.get_height()),
(0,worldy-farmPic.get_height(),farmPic.get_width(),worldy),
(worldx-farmPic.get_width(),worldy-farmPic.get_height(),worldx,worldy)])
#print(farmLocation)
farmrectangle = (0.5,0.3,0.9,0.9)
# farmrectangle refers to the portion of the image in which sheep may blit
# their upper lefts; sheepPen is the left, down, width, and height of the
# equivalent region on the map itself.
sheepPen = (farmLocation[0]+farmrectangle[0]*farmPic.get_width(),
farmLocation[1]+farmrectangle[1]*farmPic.get_height(),
(farmrectangle[2]-farmrectangle[0])*farmPic.get_width(),
(farmrectangle[3]-farmrectangle[1])*farmPic.get_height())
sheepStates = []
for i in range(5):
    sheepStates.append([random.random(),random.random(),random.randint(0,1)])

# When player is nearby, the sheep are shuffled around within the sheep pen.
def moveSheep():
    for eachSheep in sheepStates:
        newsheepx = eachSheep[0] + random.random()/10 - 0.05
        newsheepy = eachSheep[1] + random.random()/20 - 0.025
        if 0 < newsheepx < 1:
            eachSheep[0] = newsheepx
        if 0 < newsheepy < 1:
            eachSheep[1] = newsheepy
        if random.random() > 0.8:
            eachSheep[2] = random.randint(0,1)

# For moving the player, this function determines whether any point is within
# an obstacle's blit box.  For multiple barriers, consider passing a list argument
# containing a list of tuples which are lists of coordinates and the object corresponding
# to each list.
def posok(x,y):
    for ob in range(len(obstacleLocations)):
        if abs(x-obstacleLocations[ob][0]) < obstacleImages[obstacleTypes[ob]].get_width()/2 and abs(y-obstacleLocations[ob][1]) < obstacleImages[obstacleTypes[ob]].get_height()/2:
            return False
    for bis in bisonPrints:
        if abs(x-bis[0]) < bisonImage.get_width()/2 and abs(y-bis[1]) < bisonImage.get_height()/2:
            if bis not in pos_hoofprint_visited:
                pos_hoofprint_visited[bis] = True
            return bis
    if x > farmLocation[0] and x < farmLocation[2] and y > farmLocation[1] and y < farmLocation[3]:
        return False
    if(x<halfwidth or x>upperx):
        return False
    elif(y<halfheight or y>uppery):
        return False
    else:
        return (x,y)

def isNight(frames):
    if (frames % 600) > 300:
        return True
    return False

# The familiar drawscreen method places the relevant part of the background
# over the screen, then superlays obstacles, then places the relevant frame
# of the player.
def drawscreen():
    screen.blit(background,(0,0),(int(playerx-width/2),int(playery-height/2),width,height))
    if isNight(timelapsed):
        for ob in range(len(obstacleLocations)):
            screen.blit(obstacleNightImages[obstacleTypes[ob]], (int(obstacleLocations[ob][0]-playerx+width/2-obstacleNightImages[obstacleTypes[ob]].get_width()/2),int(obstacleLocations[ob][1]-playery+height/2-obstacleNightImages[obstacleTypes[ob]].get_height()/2)))
    else:
        for ob in range(len(obstacleLocations)):
            screen.blit(obstacleImages[obstacleTypes[ob]], (int(obstacleLocations[ob][0]-playerx+width/2-obstacleImages[obstacleTypes[ob]].get_width()/2),int(obstacleLocations[ob][1]-playery+height/2-obstacleImages[obstacleTypes[ob]].get_height()/2)))
    for bison in bisonPrints:
        screen.blit(bisonImage, (int(bison[0]-playerx+width/2-bisonImage.get_width()/20),int(bison[1]-playery+height/2-bisonImage.get_height()/20)))
    for rabbit in rabbitPrints:
        screen.blit(rabbitImage, (int(rabbit[0]-playerx+width/2-rabbitImage.get_width()/20),int(rabbit[1]-playery+height/2-rabbitImage.get_height()/20)))
    for deer in deerPrints:
        screen.blit(deerImage, (int(deer[0]-playerx+width/2-deerImage.get_width()/20),int(deer[1]-playery+height/2-deerImage.get_height()/20)))
    for ob in range(len(obstacleLocations)):
        screen.blit(obstacleImages[obstacleTypes[ob]], (int(obstacleLocations[ob][0]-playerx+width/2-obstacleImages[obstacleTypes[ob]].get_width()/2),int(obstacleLocations[ob][1]-playery+height/2-obstacleImages[obstacleTypes[ob]].get_height()/2)))
    for gra in range(len(grassLocations)):
        screen.blit(grassImages[(timelapsed + grassOffsets[gra]) % len(grassImages)],(int(grassLocations[gra][0]-playerx+width/2),int(grassLocations[gra][1]-playery+height/2)))
    screen.blit(farmPic,(int(farmLocation[0]-playerx+width/2),int(farmLocation[1]-playery+height/2)))
    for sheep in sheepStates:
        screen.blit(sheepPics[sheep[2]],(int(sheepPen[0]+sheepPen[2]*sheep[0]-playerx+width/2),int(sheepPen[1]+sheepPen[3]*sheep[1]-playery+height/2)))

    playerimage = framelists[currentmode][currentframe]
    screen.blit(playerimage,(int(width/2-playerimage.get_width()/2),int(height/2-playerimage.get_height()/2)))
    healthBarRect = pygame.Rect(int(5*width/6 - height/24),int(11*height/12),int(width*health/600),int(height/24))
    healthBarOutline = pygame.Rect(int(5*width/6 - height/24 - width/300),int(11*height/12 - width/300),int(width/6 + width/150),int(height/24 + width/150))
    pygame.draw.rect(screen,(255,255,255),healthBarOutline)
    pygame.draw.rect(screen,(255,0,0),healthBarRect)
    pygame.display.update()

# Pick random point where player starts.  Assume dimensions of map are greater
# than screen, else an error will occur.  Move the player to an acceptable
# position before starting.
playerx = random.randint(width/2,worldx-width/2)
playery = random.randint(height/2,worldy-height/2)
while not posok(playerx,playery):
    playerx = random.randint(width/2,worldx-width/2)
    playery = random.randint(height/2,worldy-height/2)

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
#    this line shows up as an error on my computer?
#    sets[3] = join(str(health),"\n")
    settingsfile = open("settings.txt","w")
    settingsfile.writelines(sets)
    settingsfile.close()

speed = 10 # pixels by which player moves in a frame
frametime = 100 # milliseconds of each frame

runninggame = True
timelapsed = 0 # frames, ticks, tenths of a second
health = readHealth() # In the first game, this should read "health = 100"

drawscreen()

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
    global resp
    resp = 3

    obj = posok(newposx,newposy) # returns a (x,y) coordinate if a collision occurred, else None
    if obj:
        if newposx > playerx:   # When choosing the direction to face the
            currentmode = 0     # player, left and right are prioritized for
        elif newposx < playerx: # diagonals, as in the Champion Island game.
            currentmode = 1
        elif newposy > playery:
            currentmode = 2
        elif newposy < playery:
            currentmode = 3
        playerx,playery = newposx,newposy # Player position changes;
        # Newpos variables now reflect current position.
        if dist > 0: # If player moves, update animation frame in list.
            if currentframe != len(framelists[currentmode]) - 1:
                currentframe += 1
            else:
                currentframe = 2 # Reset to third frame to loop
        else:
            currentframe = 0 # If player doesn't move, return to
    else:                             # stationary player.
        currentframe = 0 # If player cannot move, return to stationary.
    if timelapsed % 3 == 0 and (farmLocation[0] - playerx) ** 2 + (farmLocation[1] - playery) ** 2 < height ** 2 + width ** 2:
        moveSheep() # If player is near farm, move the sheep.
    pygame.time.delay(frametime)
    timelapsed += 1
    if timelapsed % 600 == 0:
        background = pygame.image.load(os.path.join('Assets','map_background.jpg'))
    elif timelapsed % 300 == 0:  # 'Light' refers to the dark version, because the function
        background = pygame.image.load(os.path.join('Assets','map_background_light.jpg'))
    drawscreen()                 # that made it lightens images by a scalar > 1.

        


