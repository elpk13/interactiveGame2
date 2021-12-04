from classes import *
import pygame
import random
import os
import math
import dialog
import bisect

# This script contains two functions:  getWorldGraphics, which loads all the
# images that appear in the world from their files and sends them in dictionaries.
# Running this function only once allows the image loading to only occur once,
# good for keeping world generation fast.  Keeping all image loading in this
# function also makes it a one-stop place to check filenames, though menu images
# are not a part of it.

# The second function, generateWorld, produces an object of the class World,
# which has as attributes lists of every object to appear in the world.
# This function has two primary parts:  the first, a set of sub-functions that
# initialize objects of our own classes (e.g., plantTree), the second, a set of
# subfunctions that produces lists of these to be sent to the world object.

# Argument names in subfunctions generally match those in the parent function.

def getWorldGraphics(window_height,worldx=0,worldy=0,bgname="Map_Background.png"):
    # worldx = worldy = 0 causes them to be determined by the dimensions of the background image.
    def getBackground(bgname,worldx=0,worldy=0):
        background = pygame.image.load(os.path.join('Assets',"Map_Background.png"))
        nightbackground = pygame.image.load(os.path.join('Assets',"Map_Background_Night.png"))
        if worldx + worldy > 0:
            background = pygame.transform.scale(background,(worldx,worldy))
            nightbackground = pygame.transform.scale(nightbackground,(worldx,worldy))
        return background, nightbackground

    background, nightbackground = getBackground(bgname,worldx,worldy)
    worldx = background.get_width()
    worldy = background.get_height()

    def getWolfGraphics(height): # Returns list of framelists for four animations and name.
        # Identity of the character determined from settings file edited by choice screen,
        # not passed to function.


        wolfGraphics = { }
        for wolfname in ['Mani']:
            pframers = [] # Form list of animations.  One for right-walking, one for
            pframels = [] # left-walking, one up, one down.
            pframeus = [] # Each starts with standing and loops from the third frame.
            pframeds = []
            pupframers = []
            pupframels = []
            pupframeus = []
            pupframeds = []
            for f in range(1,9):
                frame = pygame.image.load(os.path.join('Animations','Wolves',wolfname,wolfname + '_Walking_Right000' + str(f) + '.png'))
                frame = pygame.transform.scale(frame,(int(height*frame.get_width()/(9*frame.get_height())),int(height/9)))
                pframers.append(frame)
                frame = pygame.transform.scale(frame,(int(height*frame.get_width()/(12*frame.get_height())),int(height/12)))
                pupframers.append(frame)
                frame = pygame.image.load(os.path.join('Animations','Wolves',wolfname,wolfname + '_Walking_Right000' + str(f) + '.png'))
                frame = pygame.transform.scale(frame,(int(height*frame.get_width()/(9*frame.get_height())),int(height/9)))
                frame = pygame.transform.flip(frame,True,False)
                pframels.append(frame)
                frame = pygame.transform.scale(frame,(int(height*frame.get_width()/(12*frame.get_height())),int(height/12)))
                pupframels.append(frame)
                frame = pygame.image.load(os.path.join('Animations','Wolves',wolfname,wolfname + '_Walking_Forward000' + str(f) + '.png'))
                frame = pygame.transform.scale(frame,(int(height*frame.get_width()/(9*frame.get_height())),int(height/9)))
                pframeus.append(frame)
                frame = pygame.transform.scale(frame,(int(height*frame.get_width()/(12*frame.get_height())),int(height/12)))
                pupframeus.append(frame)
                frame = pygame.image.load(os.path.join('Animations','Wolves',wolfname,wolfname + '_walking_Away000' + str(f) + '.png'))
                frame = pygame.transform.scale(frame,(int(height*frame.get_width()/(7*frame.get_height())),int(height/7)))
                pframeds.append(frame)
                frame = pygame.transform.scale(frame,(int(height*frame.get_width()/(9*frame.get_height())),int(height/9)))
                pupframeds.append(frame)
            frame = pygame.image.load(os.path.join('Assets',wolfname+'_Headshot.png'))

            if wolfname == "Mani":
                wolfname = "Máni"  # Accent mark not in filename.

            wolfGraphics[wolfname] = [pframers,pframels,pframeus,pframeds,frame,pupframers,pupframels,pupframeus,pupframeds]

        return wolfGraphics

    wolfGraphics = getWolfGraphics(window_height)

    def getStreamGraphics():
        streamAppearancesByAim = { } # The 'aim' of a stream roughly refers to the
        streamNightAppearancesByAim = { } # direction south of the west-axis in
        appearances = [] # which it flows.  Rivers flow south-west, always.
        nightappearances = []
        streamDimensionsByAim = { } # 's' refers to source.
        for aim in ['30','45','60','30s','45s','60s','30-45','45-60','60-30','30-60','60-45','45-30']:
            for i in range(1,4):  # Change length of stream animations here.
                appearances.append(pygame.image.load(os.path.join('Animations','Streams',aim+'000'+str(i)+'.png')))
                nightappearances.append(pygame.image.load(os.path.join('Animations','Streams',aim+'000'+str(i)+'_Night.png')))
            streamAppearancesByAim[aim] = appearances
            streamNightAppearancesByAim[aim] = nightappearances
            width, height = appearances[0].get_width(), appearances[0].get_height()
            streamDimensionsByAim[aim] = (width,height)
            appearances = []
            nightappearances = []
        return streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim

    streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim = getStreamGraphics()

    def getStreamCurveCoefficients(): # The coefficients of curves in stream bends
        def fg(t,w,i,e): # need only be calculated once.  This method is explained in a side document.
            def r(d): # Cool, a fourth-order nested function!
                return int(d)*math.pi/180 # Converts degree-strings to radians.
            f = ( (t*math.tan(r(i))+t*math.tan(r(e))+2*w/math.cos(r(e))-2*t)/t**3 , (3*t-3*w/math.cos(r(e))-2*t*math.tan(r(e))-t*math.tan(r(i)))/t**2 , math.tan(r(e)) , w/math.cos(r(e)) )
            g = ( (t*math.tan(r(i))+t*math.tan(r(e))+2*w/math.cos(r(i))-2*t)/t**3 , (3*t-3*w/math.cos(r(i))-2*t*math.tan(r(e))-t*math.tan(r(i)))/t**2 , math.tan(r(e)) , 0 )
            return f, g
        streamCurveCoefficients = { }
        for aim in ['30-45','30-60','45-30','45-60','60-30','60-45']:
            streamCurveCoefficients[aim] = fg(300,50,aim[:2],aim[-2:])
        return streamCurveCoefficients

    streamCurveCoefficients = getStreamCurveCoefficients()

    def getTreeGraphics():
        treeGraphics = { } # Dictionary of framelists (one for each season) by type.
        treeNightGraphics = { }
        treeGreenness = { } # Dictionary of whether a tree is evergreen (same image in winter)
        for type in ['White_Oak','Common_Ash']: # List all non-evergreen trees here.
            summerdays = []
            summernits = []
            autumndays = []
            autumnnits = []
            winterdays = []
            winternits = []
            for i in range(1,8):
                summerdays.append(pygame.image.load(os.path.join('Animations','Trees',type+'_Summer000'+str(i)+'.png')))
                summernits.append(pygame.image.load(os.path.join('Animations','Trees',type+'_Summer000'+str(i)+'_Night.png')))
                autumndays.append(pygame.image.load(os.path.join('Animations','Trees',type+'_Autumn000'+str(i)+'.png')))
                autumnnits.append(pygame.image.load(os.path.join('Animations','Trees',type+'_Autumn000'+str(i)+'_Night.png')))
                winterdays.append(pygame.image.load(os.path.join('Animations','Trees',type+'_Winter000'+str(i)+'.png')))
                winternits.append(pygame.image.load(os.path.join('Animations','Trees',type+'_Winter000'+str(i)+'_Night.png')))
            treeGraphics[type] = (summerdays,autumndays,winterdays)
            treeNightGraphics[type] = (summernits,autumnnits,winternits)
            treeGreenness[type] = False
        for type in ['Spruce']: # List all evergreen trees here.
            days = []
            nits = []
            for i in range(1,8):
                days.append(pygame.image.load(os.path.join('Animations','Trees',type+'000'+str(i)+'.png')))
                nits.append(pygame.image.load(os.path.join('Animations','Trees',type+'000'+str(i)+'_Night.png')))
            treeGraphics[type] = days
            treeNightGraphics[type] = nits
            treeGreenness[type] = True
        return treeGraphics, treeNightGraphics, treeGreenness

    treeGraphics, treeNightGraphics, treeGreenness = getTreeGraphics()

    def getRockGraphics(): # Any static obstacle is a rock.
        rockGraphics = { }
        rockNightGraphics = { }
        for rocktype in ['limestone','nonrock']:
            rockGraphics[rocktype] = pygame.image.load(os.path.join('Assets',rocktype+'.png'))
            rockNightGraphics[rocktype] = pygame.image.load(os.path.join('Assets',rocktype+'_Night.png'))
        return rockGraphics, rockNightGraphics

    rockGraphics, rockNightGraphics = getRockGraphics()

    def getDecorGraphics():
        decorGraphics = { }
        decorNightGraphics = { }
        decorDynamics = { }
        for dynamictype in ['grass']:
            dynamicLengths = {'grass':7}
            appearances = []
            nightappearances = []
            for i in range(1,dynamicLengths[dynamictype]+1):
                appearances.append(pygame.image.load(os.path.join('Animations','Decorations',dynamictype+'000'+str(i)+'.png')))
                nightappearances.append(pygame.image.load(os.path.join('Animations','Decorations',dynamictype+'000'+str(i)+'_Night.png')))
            decorGraphics[dynamictype] = appearances
            decorNightGraphics[dynamictype] = nightappearances
            decorDynamics[dynamictype] = True
        for statictype in ['flower1','flower2','flower3','flower4']:
            decorGraphics[statictype] = pygame.image.load(os.path.join('Assets','Decorations',statictype+'.png'))
            decorNightGraphics[statictype] = pygame.image.load(os.path.join('Assets','Decorations',statictype+'_Night.png'))
            decorDynamics[statictype] = False
        return decorGraphics, decorNightGraphics, decorDynamics

    decorGraphics, decorNightGraphics, decorDynamics = getDecorGraphics()

    def getPrintGraphics(height): # Height is the height of the world, by which prints are scaled.
        printGraphics = { } # Prints, large and identifiable for dialogs
        printGraphicsSmall = { } # Blitted images in the world
        animalTypes = { } # Types by animal - 0 for prey, 1 for mutual, 2 for predator
        for animal in ['bison']: # List predators here - bear, moose
            printImage = pygame.image.load(os.path.join('Assets',animal+"_print.png"))
            printImageSmall = pygame.transform.scale(printImage,(int(height/15),int(height/15)))
            printGraphics[animal] = printImage
            printGraphicsSmall[animal] = printImageSmall
            animalTypes[animal] = 2
        for animal in []: # List neither predator nor prey here - raccoons, foxes
            printImage = pygame.image.load(os.path.join('Assets',animal+"_print.png"))
            printImageSmall = pygame.transform.scale(printImage,(int(height/15),int(height/15)))
            printGraphics[animal] = printImage
            printGraphicsSmall[animal] = printImageSmall
            animalTypes[animal] = 1
        for animal in ['deer','rabbit']: # List prey here
            printImage = pygame.image.load(os.path.join('Assets',animal+"_print.png"))
            printImageSmall = pygame.transform.scale(printImage,(int(height/15),int(height/15)))
            printGraphics[animal] = printImage
            printGraphicsSmall[animal] = printImageSmall
            animalTypes[animal] = 0
        return printGraphics, printGraphicsSmall, animalTypes

    printGraphics, printGraphicsSmall, animalTypes = getPrintGraphics(window_height)

    def getMiscellaneousGraphics():
        miscellaneousGraphics = { }
        miscellaneousNightGraphics = { }
        miscellaneousGraphics['den'] = pygame.image.load(os.path.join('Assets','Wolf_Den.png'))
        miscellaneousNightGraphics['den'] = pygame.image.load(os.path.join('Assets','Wolf_Den_Night.png'))
        miscellaneousGraphics['farm'] = pygame.image.load(os.path.join('Assets','farm.png'))
        miscellaneousNightGraphics['farm'] = pygame.image.load(os.path.join('Assets','farm_Night.png'))
        return miscellaneousGraphics, miscellaneousNightGraphics

    miscellaneousGraphics, miscellaneousNightGraphics = getMiscellaneousGraphics()

    def getAnimalGraphics(animalTypes):
        animalGraphics = { }
        for animal in animalTypes: # Iterate through the keys of dictionary animalTypes.
            framers = []
            framels = []
            frameus = []
            frameds = []
            for frame in range(1,2):
                framers.append(pygame.image.load(os.path.join('Animations','Animals',animal+'_right000'+str(frame)+'.png')))
                framels.append(pygame.transform.flip(framers[-1],True,False))
                frameus.append(pygame.image.load(os.path.join('Animations','Animals',animal+'_up000'+str(frame)+'.png')))
                frameds.append(pygame.image.load(os.path.join('Animations','Animals',animal+'_down000'+str(frame)+'.png')))
            animalGraphics[animal] = [framers,framels,frameus,frameds]
        return animalGraphics

    animalGraphics = getAnimalGraphics(animalTypes)

    return worldx, worldy, background, nightbackground, wolfGraphics, streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim, streamCurveCoefficients, treeGraphics, treeNightGraphics, treeGreenness, rockGraphics, rockNightGraphics, decorGraphics, decorNightGraphics, decorDynamics, printGraphics, printGraphicsSmall, miscellaneousGraphics, miscellaneousNightGraphics, animalTypes, animalGraphics

# Observe that not all the output from the above function is input into that
# below.  The character, the animalTypes dictionary, and the larger print graphics
# are not necessary for the construction of the world.

def generateWorld(worldx,worldy,window_width,window_height,background, nightbackground, streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim, streamCurveCoefficients, treeGraphics, treeNightGraphics, treeGreenness, rockGraphics, rockNightGraphics, decorGraphics, decorNightGraphics, decorDynamics, printGraphicsSmall, miscellaneousGraphics, miscellaneousNightGraphics, animalGraphics):
    # The first part of this function, concerning sub-functions that initialize
    # user-defined classes.  Updates to classes probably need to be updated here.

    def pourStream(worldx,worldy,window_width,window_height,streamAppearancesByAim,streamNightAppearancesByAim,streamDimensionsByAim):
        sourcex = random.randint(window_width,worldx) # Place a random source, pick a direction, and go.
        sourcey = random.randint(window_height,worldy)
        dir = random.choice(['30','45','60'])
        riverys = {'30':58,'45':71,'60':100} # Vertical height of the river at crossing, by angle.
                                             # Equals width times the secant of the angle.
        aim = dir+'s'
        stream = [StreamSegment(sourcex,sourcey,200,200,True,streamAppearancesByAim[aim],streamNightAppearancesByAim[aim],aim)]
        runningx = sourcex
        runningy = sourcey + 200 - riverys[dir]

        while runningx > 0 and runningy < worldy:
            if random.random() > 0.25: # Half a chance of changing direction with each.
                newdir = random.choice(['30','45','60'])
            else:
                newdir = dir
            if newdir == dir:
                aim = dir
            else:
                aim = '-'.join([dir,newdir])
            segwidth, segheight = streamDimensionsByAim[aim]
            stream.append(StreamSegment(int(runningx-segwidth),runningy,segwidth,segheight,True,streamAppearancesByAim[aim],streamNightAppearancesByAim[aim],aim))
            runningx -= segwidth
            runningy += segheight - riverys[newdir]
            dir = newdir
        return stream # Returns list of segments

    def dry(x,y,streams=[]): # This function checks whether any
        for stream in streams: # streams cover a given point.  Used in later
            for segment in stream: # initialization functions to ensure that
                if segment.covers(x,y,streamCurveCoefficients): # trees, etc.
                    return False                                # not in water.
        return True

    def plantTree(worldx,worldy,type,streams,treeGraphics,treeNightGraphics,treeGreenness):
        while True:
            x = random.randint(0,worldx)
            y = random.randint(0,worldy)
            if dry(x,y,streams):
                appearance = treeGraphics[type]
                if treeGreenness[type]:
                    height = appearance[0].get_height()
                    width = appearance[0].get_width()
                else:
                    height = appearance[0][0].get_height()
                    width = appearance[0][0].get_width()
                return Tree(int(x-width/2),int(y-3*height/4),height,width,True,treeGraphics[type],treeNightGraphics[type],type,treeGreenness[type])

    def placeRock(worldx,worldy,streams,rockGraphics,rockNightGraphics,rocktype=None):
        while True:
            x = random.randint(0,worldx)
            y = random.randint(0,worldy)
            if dry(x,y,streams):
                if rocktype == None:
                    rocktype = random.choice(list(rockGraphics))
                appearance = rockGraphics[rocktype]
                nightappearance = rockNightGraphics[rocktype]
                return Rock(x,y,appearance.get_height(),appearance.get_width(),appearance,nightappearance)

    def posok(x,y,obstacles):
        for ob in obstacles:
            if ob.collidesat(x,y):
                return False
        else:
            return True

    def growDecoration(worldx,worldy,streams,decorGraphics,decorNightGraphics,decorDynamics,decortype=None):
        while True:
            x = random.randint(0,worldx)
            y = random.randint(0,worldy)
            if dry(x,y,streams):
                if decortype == None:
                    decortype = random.choice(list(decorDynamics))
                appearance = decorGraphics[decortype]
                nightappearance = decorNightGraphics[decortype]
                dynamicity = decorDynamics[decortype]
                if dynamicity:
                    return Decoration(x,y,appearance[0].get_height(),appearance[0].get_width(),True,appearance,nightappearance)
                else:
                    return Decoration(x,y,appearance.get_height(),appearance.get_width(),False,appearance,nightappearance)

    def stampPrint(worldx,worldy,window_width,window_height,animal,streams,printGraphicsSmall):
        while True:
            x = random.randint(window_width//2,worldx-window_width//2)
            y = random.randint(window_height//2,worldy-window_height//2)
            if dry(x,y,streams):
                appearance = printGraphicsSmall[animal]
                return Print(x,y,appearance.get_height(),appearance.get_width(),animal,appearance)

    def digDen(worldx,worldy,window_width,window_height,streams,obstacles,miscellaneousGraphics,miscellaneousNightGraphics):
        denappearance = miscellaneousGraphics['den']
        denightappearance = miscellaneousNightGraphics['den']
        attempts = 0
        while attempts < 6:
            s = random.choice(random.choice(streams))
            if window_width / 2 < s.xpos < worldx - window_width / 2 and window_height / 2 + denappearance.get_height() < s.ypos < worldy - window_height/2:
                if posok(s.xpos + denappearance.get_width()/2, s.ypos + denappearance.get_height()/2,obstacles):
                    return Settlement(s.xpos,s.ypos-denappearance.get_height(),denappearance.get_height(),denappearance.get_width(),False,denappearance,denightappearance,(0.8,0.1,0.5,0.8))
            attempts += 1
        x = random.randint(window_width//2,worldx-window_width//2-denappearance.get_width())
        y = random.randint(window_height//2,worldy-window_height//2-denappearance.get_height())
        return Settlement(x,y,denappearance.get_height(),denappearance.get_width(),False,denappearance,denightappearance,(0.8,0.1,0.5,0.8))

    def buildFarm(worldx,worldy,window_width,window_height,world_items,miscellaneousGraphics,miscellaneousNightGraphics):
        farmappearance = miscellaneousGraphics['farm']
        farmnightappearance = miscellaneousNightGraphics['farm']
        if random.random() > 0.5:
            x = random.randint(0,window_width-farmappearance.get_width())
        else:
            x = random.randint(worldx - window_width, worldx-farmappearance.get_width())
        if random.random() > 0.5:
            y = random.randint(0,window_height-farmappearance.get_height())
        else:
            y = random.randint(worldy - window_height, worldy-farmappearance.get_height())
        farm = Settlement(x,y,farmappearance.get_height(),farmappearance.get_width(),False,farmappearance,farmnightappearance,(0,1,0,1),True)
        cleared = []
        for item in world_items:
            if item.xpos + item.width > farm.xpos and item.xpos < farm.xpos + farm.width and item.ypos + item.height > farm.ypos and item.ypos < farm.ypos - farm.height:
                cleared.append(item)
        return farm, cleared

    # The birthAnimal method, which initializes the animal class, is not here, as
    # animals are not present in the default world.

    # The second part of this function concerns the placement of objects
    # initialized in the above code, beginning with streams and continuing
    # through obstacles and decorations.

    mystreams = [] # Pourstream is sufficient; I didn't feel like making a whole subfunction for the multiple streams.
    for s in range(2//random.randint(1,6)+1): # Maximum 3, but probably just one.
        mystreams.append(pourStream(worldx,worldy,window_width,window_height,streamAppearancesByAim,streamNightAppearancesByAim,streamDimensionsByAim))

    def forestWorld(worldx,worldy,treeTypes,streams,treeGraphics,treeNightGraphics,treeGreenness):
        treecount = worldx*worldy * random.randint(28,175) // 10000000   # Based on historical forest estimates
        if len(treeTypes) > 7: # If we get so far, forests can be unique # and an arbitrary conversion of pixels
            treeTypes = random.sample(treeTypes,random.randint(5,7))     # to real-life units.
        forest = []
        for t in range(treecount):
            forest.append(plantTree(worldx,worldy,random.choice(treeTypes),streams,treeGraphics,treeNightGraphics,treeGreenness))
        forest.sort(key=lambda x: x.ybase)
        return forest

    myforest = forestWorld(worldx,worldy,list(treeGraphics),mystreams,treeGraphics,treeNightGraphics,treeGreenness)

    def setRocks(worldx,worldy,rockGraphics,rockNightGraphics,streams):
        rocks = []
        for i in range(10):
            rocks.append(placeRock(worldx,worldy,streams,rockGraphics,rockNightGraphics,'limestone'))
        for i in range(5):
            rocks.append(placeRock(worldx,worldy,streams,rockGraphics,rockNightGraphics,'nonrock'))
        return rocks

    myrocks = setRocks(worldx,worldy,rockGraphics,rockNightGraphics,mystreams)

    def decorate(worldx,worldy,decorGraphics,decorNightGraphics,decorDynamics,streams):
        decorations = []
        for i in range(50):
            decorations.append(growDecoration(worldx,worldy,streams,decorGraphics,decorNightGraphics,decorDynamics))
        return decorations

    mydecorations = decorate(worldx,worldy,decorGraphics,decorNightGraphics,decorDynamics,mystreams)

    def leavePrints(worldx,worldy,window_width,window_height,printGraphicsSmall,streams):
        count = worldx*worldy // 1000000
        prints = []
        for i in range(count):
            prints.append(stampPrint(worldx,worldy,window_width,window_height,random.choice(list(printGraphicsSmall)),streams,printGraphicsSmall))
        return prints

    myprints = leavePrints(worldx,worldy,window_width,window_height,printGraphicsSmall,mystreams)

    myden = digDen(worldx,worldy,window_width,window_height,mystreams,myforest + myrocks,miscellaneousGraphics,miscellaneousNightGraphics)
    myclearance = []
    mysettlements = [myden]
    for f in range(2//random.randint(1,6)+1): # Same as streams - count of farms is at most three, probably one.
        farm, clearance = buildFarm(worldx,worldy,window_width,window_height,myforest+myrocks+myprints+mydecorations,miscellaneousGraphics,miscellaneousNightGraphics)
        mysettlements.append(farm)
        myclearance.append(clearance)
    for cleareditem in myclearance:
        if cleareditem in myforest:
            myforest.remove(cleareditem)
        elif cleareditem in myrocks:
            myrocks.remove(cleareditem)
        elif cleareditem in myprints:
            myprints.remove(cleareditem)
        elif cleareditem in mydecorations:
            mydecorations.remove(cleareditem)

    return World(worldx,worldy,background,nightbackground,mystreams,myforest,myrocks,myprints,mydecorations,mysettlements,[       ])
#    return World(worldx,worldy,background,nightbackground,mystreams,myforest,myrocks,myprints,mydecorations,mysettlements,myanimals)
# When we iterate through a null list, it can only throw syntax errors.  Try:
# for i in []:
#     tom = turtle.Turtle()
#     tom.throwmeanerror(idareyou)
# in a command prompt; it's fun!

def makeHuntWorld(oldworld,centerx,centery,window_width,window_height,prey,animalGraphics,night,pack=False,wolfGraphics={ },maincharname='',packmemcount=0):
    borders = (int(centerx - window_width/2), int(centerx + window_width/2), int(centery - window_height/2), int(centery + window_width/2))
    if night:
        huntbackground = oldworld.nightbackground.subsurface((borders[0],borders[2],window_width,window_height))
    else:
        huntbackground = oldworld.background.subsurface((borders[0],borders[2],window_width,window_height))

    def inHuntWorld(object, borders):
        if object.xpos < borders[1] and object.width + object.xpos > borders[0] and object.ypos < borders[3] and object.ybase > borders[2]:
            return True
        return False

    newstream = []
    for stream in oldworld.streams:
        for segment in stream:
            if inHuntWorld(segment,borders):
                newstream.append(segment)
    keptforest = []
    for tree in oldworld.forest:
        if inHuntWorld(tree,borders):
            keptforest.append(tree)
    keptrocks = []
    for rock in oldworld.rocks:
        if inHuntWorld(rock,borders):
            keptrocks.append(rock)
    keptdecorations = []
    for decor in oldworld.decorations:
        if inHuntWorld(rock,borders):
            keptdecorations.append(decor)
    # There are no settlements nor prints in the hunting world.

    def posok(x,y,obstacles):
        for ob in obstacles:
            if ob.collidesat(x,y):
                return False
        else:
            return True

    def birthPreyAnimal(borders,animal,obstacles,animalGraphics):
        while True:
            x = random.randint(borders[0]+window_width//5,borders[1]-window_width//5)
            y = random.randint(borders[2]+window_height//5,borders[3]-window_height//5)
            if posok(x,y,obstacles):
                appearance = animalGraphics[animal]
                if animal == 'rabbit': # Keep in if-elif tree so that class is different.
                    return Rabbit(x,y,appearance[0][0].get_height(),appearance[0][0].get_width(),appearance)
                elif animal == 'deer': # Class is different so that move method is different,
                    return Deer(x,y,appearance[0][0].get_height(),appearance[0][0].get_width(),appearance)
                elif animal == 'bison': # Else there would be an uglier if-else tree in 'move()'.
                    return Bison(x,y,appearance[0][0].get_height(),appearance[0][0].get_width(),appearance)
                else:
                    return Animal(x,y,appearance[0][0].get_height(),appearance[0][0].get_height(),appearance,animal,10)

    newanimals = [ birthPreyAnimal(borders,prey,keptforest+keptrocks,animalGraphics) ]

    def addWolf(borders,obstacles,wolfGraphics,maincharname):
        while True:
            s = random.randint(0,2*(borders[1]+borders[3]-borders[0]-borders[2]))
            if s < borders[1] - borders[0]:
                x = borders[0] + s
                y = borders[3]
            elif s < borders[1]+borders[3]-borders[0]-borders[2]:
                x = borders[1]
                y = borders[3] - s + borders[1] - borders[0]
            elif s < 2*borders[1]+borders[3]-2*borders[0]-borders[2]:
                x = borders[0] + s - borders[1] - borders[3] + borders[0] + borders[2]
                y = borders[2]
            else:
                x = borders[0]
                y = borders[2] + s - 2*borders[1] - borders[3] + 2*borders[0] + borders[2]
            if posok(x,y,obstacles):
                charnamelist = list(wolfGraphics)
                #charnamelist.remove(maincharname) Re-instate this line when we have graphics for a second wolf!
                wolfname = random.choice(charnamelist)
                appearances = wolfGraphics[wolfname]
                return Wolf(x,y,appearances[0][0].get_height(),appearances[0][0].get_width(),appearances,wolfname)

    if pack:
        for i in range(packmemcount):
            newanimals.append(addWolf(borders,keptforest+keptrocks,wolfGraphics,maincharname))

    return borders, World(window_width,window_height,huntbackground,huntbackground,[newstream],keptforest,keptrocks, [    ], keptdecorations, [          ],newanimals)
