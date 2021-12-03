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
rabbitImage = pygame.image.load(os.path.join('Assets_poc',"rabbit print.png"))
rabbitImage = pygame.transform.scale(rabbitImage,(int(width/10),int(height/10)))
rabbitPrints = []

rabbitFace = pygame.image.load(os.path.join('Assets_poc',"rabbitSample.png"))
rabbitFace = pygame.transform.scale(rabbitFace,(int(width/2),int(height/2)))
#for i in range(50):
#    rabbitPrints.append((random.randint(0,worldx),random.randint(0,worldy)))
#rabbitPrints.sort(key=lambda x : x[1])
rabbitA = (random.randint(halfwidth,upperx-100),random.randint(halfheight,uppery-100))
print(f"rabbitA:{rabbitA}")


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

caught = 0
count = 0
# For moving the player, this function determines whether any point is within
# an obstacle's blit box.  For multiple barriers, consider passing a list argument
# containing a list of tuples which are lists of coordinates and the object corresponding
# to each list.
def posok(x,y):
    
    for ob in range(len(obstacleLocations)):
        if abs(x-obstacleLocations[ob][0]) < obstacleImages[obstacleTypes[ob]].get_width()/4   and abs(y-obstacleLocations[ob][1]) < obstacleImages[obstacleTypes[ob]].get_height()/4:
            return False
    if(x<halfwidth or x>upperx):
        return False
    elif(y<halfheight or y>uppery):
        return False
    if(abs(x-rabbitA[0]) < (rabbitFace.get_width()/5) and abs(y-rabbitA[1]) < (rabbitFace.get_height()/5)):
        #global caught
        #caught = 1
        global count
        count +=1
        print(f"x:{x},y{y}")
        print(f"colx: {x-rabbitA[0]}, coly: {y-rabbitA[1]}")
        #print(rabbitFace.get_width()/5, rabbitFace.get_height()/5)
        print(f"collide no {count}" )
        #print(caught)
        return True
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
    #for rabbit in rabbitPrints:
    #    screen.blit(rabbitImage, (int(rabbit[0]-playerx+width/2-rabbitImage.get_width()/20),int(rabbit[1]-playery+height/2-rabbitImage.get_height()/20)))
    for rx,ry in zip(rabbitpath_x, rabbitpath_y):
        # screen.blit(obstacleImages[obstacleTypes[ob]], (int(obstacleLocations[ob][0]-playerx+width/2-obstacleImages[obstacleTypes[ob]].get_width()/2),int(obstacleLocations[ob][1]-playery+height/2-obstacleImages[obstacleTypes[ob]].get_height()/2)))
        screen.blit(rabbitImage, (int(rx-playerx+width/2-rabbitImage.get_width()/2), int(ry-playery+height/2-rabbitImage.get_height()/2)) )
    for ob in range(len(obstacleLocations)):
        screen.blit(obstacleImages[obstacleTypes[ob]], (int(obstacleLocations[ob][0]-playerx+width/2-obstacleImages[obstacleTypes[ob]].get_width()/2),int(obstacleLocations[ob][1]-playery+height/2-obstacleImages[obstacleTypes[ob]].get_height()/2)))
    for gra in range(len(grassLocations)):
        screen.blit(grassImages[(timelapsed + grassOffsets[gra]) % len(grassImages)],(int(grassLocations[gra][0]-playerx+width/2),int(grassLocations[gra][1]-playery+height/2)))
    screen.blit(rabbitFace,(int(rabbitA[0]-playerx+width/2-rabbitFace.get_width()/2),int(rabbitA[1]-playery+height/2-rabbitFace.get_height()/2)))
    playerimage = framelists[currentmode][currentframe]
    screen.blit(playerimage,(int(width/2-playerimage.get_width()/2),int(height/2-playerimage.get_height()/2)))
    pygame.display.update()

# Pick random point where player starts.  Assume dimensions of map are greater
# than screen, else an error will occur.  Move the player to an acceptable
# position before starting.
playerx = random.randint(width/2,worldx-width/2)
playery = random.randint(height/2,worldy-height/2)
while not posok(playerx,playery):
    playerx = random.randint(width/2,worldx-width/2)
    playery = random.randint(height/2,worldy-height/2)


speed = 10 # pixels by which player moves in a frame
frametime = 100 # milliseconds of each frame

runninggame = True
timelapsed = 0 # frames, ticks, tenths of a second


#path function to determine the path on which to blit the rabbit prints
#takes an acceptable radius and angle, using these two things
#determines the path of the footprints that the player will
#have to follow to get to the animal
rabbitPath = []
rad = []

def findPath():
    
    newx = []
    newy = []
    # sort the location of the rabbit relative to the player. 
    #initial iteration, will need to be done in a loop using rabbitPath
    #so that way it varies the path for each increment.

    global rabbitPath
    rabbitPath.append(playerx)
    rabbitPath.append(playery)
    ind = 0
    rabRad = 10000
    global rad
    rad.append(5)
    radInd = 0

    #loop through the distance from the player blit through the rabbit's location
    #stop when the rabbit's location is within the radius that the player can move within
    while rabRad > 400: 
        #
        if(rabbitA[0] > rabbitPath[-2] and rabbitA[1] >= rabbitPath[-1]):
            yLen = rabbitA[1] - rabbitPath[-1]
            xLen = rabbitA[0] - rabbitPath[-2]
            oppAdj = xLen / yLen
            loc = 1
            xc = 1
            yc = 1
            print("one")
        elif(rabbitA[0] < rabbitPath[-2] and rabbitA[1] <= rabbitPath[-1]):
            yLen = rabbitPath[-1] - rabbitA[1]
            xLen = rabbitPath[-2] - rabbitA[0]
            oppAdj = yLen / xLen
            loc = 2
            xc = -1
            yc = -1
            print("two")
        elif(rabbitA[0] < rabbitPath[-2] and rabbitA[1] >= rabbitPath[-1]):
            yLen = rabbitA[1] - rabbitPath[-1]
            xLen = rabbitPath[-2] - rabbitA[0] 
            oppAdj = xLen / yLen
            loc = 2
            xc = -1
            yc = 1
            print("three")
        elif(rabbitA[0] > rabbitPath[-2] and rabbitA[1] <= rabbitPath[-1]):
            yLen = rabbitPath[-1] - rabbitA[1]
            xLen = rabbitA[0] - rabbitPath[-2] 
            oppAdj = yLen / xLen
            loc = 1
            xc = 1
            yc = -1
            print("four")
        rabRadSq = (xLen**2) + (yLen**2) # calculate norm^2 from current pos to rabbit
        if math.sqrt(rabRadSq) > rabRad:
            rabbitPath.pop()
            rabbitPath.pop()
            rad.append(random.randint(75, 400)) #choose new random radius for next point
            ind -= 2
            print('.',end='')
            continue
        rabRad = math.sqrt(rabRadSq) # calculate norm from current pos to rabbit
        print("rabRad:", end='')
        print(rabRad)
        theta = math.atan(oppAdj) # calculate current angle to rabbit
        angle = random.randint(0, int(theta * 1000)) / 1000 # choose new random angle between 0 and that angle
        rabbitPath.append(rad[-1] * math.cos(angle) * xc + rabbitPath[ind]) # choose new random point x
        rabbitPath.append(rad[-1] * math.sin(angle) * yc + rabbitPath[ind+1]) # choose new random point y
        ind += 2
        radInd += 1
        rad.append(random.randint(75, 400)) #choose new random radius for next point
        print(f"radInd{radInd}")
        #print(rabRad, xc, yc, loc)

    #footprint array calculations here 
    newx, newy = [x for i,x in enumerate(rabbitPath) if i % 2 == 0],[x for i,x in enumerate(rabbitPath) if i % 2 == 1]

    return (newx,newy)

rabbitpath_x, rabbitpath_y = findPath()
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
    if pressed[pygame.K_SPACE]:
        speed = 40
    else:
        speed = 10
    if caught == 1:
        runninggame = False
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
    pygame.time.delay(frametime)

    drawscreen()                 # that made it lightens images by a scalar > 1.
