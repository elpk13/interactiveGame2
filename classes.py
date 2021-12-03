import math
import random

# Any object that exists in the world is of object class.
class Object:
    def __init__(self,xpos,ypos,height,width,dynamic,appearance,nightappearance):
        self.xpos = xpos # Distance between object's left side and that of the world.
        self.ypos = ypos # Distance between object's TOP side and that of the world.
        self.width = width
        self.height = height
        self.dynamic = dynamic # A Boolean indicating whether the object is animated.
        self.appearance = appearance # Could be a Surface or a list or a list of lists of surfaces
        self.nightappearance = nightappearance
        self.ybase = ypos + height # Used for sorting blit order.

    def draw(self,screen,playerx,playery,window_width,window_height,night,time,scroll=True,leftx=0,topy=0):
        if night: # Night-time is defined in globals.  Seasons are defined in the tree class.
            if self.dynamic:
                appearance = self.nightappearance[time % len(self.nightappearance)]
            else:
                appearance = self.nightappearance
        else:
            if self.dynamic:
                appearance = self.appearance[time % len(self.appearance)]
            else:
                appearance = self.appearance
        if scroll:
            screen.blit(appearance,(int(self.xpos-playerx+window_width/2),int(self.ypos-playery+window_height/2)))
        else:
            screen.blit(appearance,(self.xpos-leftx,self.ypos-topy))

# Objects that impede the player's movement have a collision box as well.
# The 'collidesat' checks if a point is inside it.
# A collision box is - in this code - a tuple (a,b,c,d), 0 < a < b < 1,
# 0 < c < d < 1, referring to the portion of the image considered the box.
class Obstacle(Object):
    def __init__(self,xpos,ypos,height,width,dynamic,appearance,nightappearance,collisionBox):
        self.collisionBox = collisionBox
        super().__init__(xpos,ypos,height,width,dynamic,appearance,nightappearance)

    def collidesat(self,possiblex,possibley):
        if self.collisionBox[0] < (possiblex-self.xpos)/self.width < self.collisionBox[1] and self.collisionBox[2] < (possibley-self.ypos)/self.height < self.collisionBox[3]:
            return True
        return False

# Objects below have specific appearances that should relate to other properties,
# like a stream's aim or a tree's type; however, these are passed to the class in
# the initialization functions like 'pourStream' or 'plantTree' so that the
# graphics dictionaries can be passed as well.

class StreamSegment(Object): # appearance should come from the getStreamGraphics dictionary
    def __init__(self,xpos,ypos,height,width,dynamic,appearance,nightappearance,aim):
        self.aim = aim
        if len(aim) < 4:
            self.a = int(aim[:2])*math.pi/180 # Angle in radians as float, for straights and sources
        super().__init__(xpos,ypos,height,width,dynamic,appearance,nightappearance)

    def __str__(self):
        return 'A stream segment of aim ' + self.aim + ' at (' + self.xpos + ',' + self.ypos + ')'

    def covers(self,possiblex,possibley,streamCurveCoefficients): # Curve coefficients come from
        x = possiblex - self.xpos                                 # the dictionary.
        y = self.ypos + self.height - possibley
        if not (0 < x < self.width and 0 < y < self.height):
            return False
        if self.aim in ['30','45','60']:
            if y > x*math.tan(self.a) and y < x*math.tan(self.a) + 50/math.cos(self.a):
                return True
            return False
        elif self.aim[-1] == 's':
            if ((x-self.width/2)**2+(y-self.height/2)**2)**0.5 < self.width/2:
                return True
            elif x < self.width/2 and y > x*math.tan(self.a) and y < x*math.tan(self.a) + 50/math.cos(self.a):
                return True
            return False
        else:
            f, g = streamCurveCoefficients[self.aim]
            if f[0]*x**3 + f[1]*x**2 + f[2]*x + f[3] > y > g[0]*x**3 + g[1]*x**2 + g[2]*x + g[3]:
                return True
            return False

class Tree(Obstacle): # The 'appearance' and 'evergreen' states should come from the getTreeGraphics dictionary.
    def __init__(self,xpos,ypos,height,width,dynamic,appearance,nightappearance,type,evergreen):
        self.type = type
        self.evergreen = evergreen # Collision box for trees is defined here \|/
        super().__init__(xpos,ypos,height,width,dynamic,appearance,nightappearance,(0.4,0.6,0.6,0.8))

    def __str__(self):
        return 'A(n) ' + self.type + ' tree at (' + self.xpos + ',' + self.ypos + ')'

    def draw(self,screen,playerx,playery,window_width,window_height,night,time,scroll=True,leftx=0,topy=0):
        if time % 2400 < 1200:
            s = 0 # And the leaves that are green...
        elif time % 2400 < 1800:
            s = 1 # turn to brown
        else:
            s = 2 # and they wither with the wind
        m = 3
        t = time % (8*m)
        if t % (4*m) < 2*m: # Unique animation for trees is described in a
            f = m # side document.
        elif t < 3*m:
            f = t - m
        elif t < 4*m:
            f = 5*m - t
        elif t < 7*m:
            f = 7*m - t
        else:
            f = t-7*m
        if night:
            if self.evergreen:
                appearance = self.nightappearance[f]
            else:
                appearance = self.nightappearance[s][f]
        else:
            if self.evergreen:
                appearance = self.appearance[f]
            else:
                appearance = self.appearance[s][f]
        if scroll:
            screen.blit(appearance,(int(self.xpos-playerx+window_width/2),int(self.ypos-playery+window_height/2)))
        else:
            screen.blit(appearance,(self.xpos-leftx,self.ypos-topy))

class Rock(Obstacle): # Appearance can be any Surface.  Ideally one depicting a rock.
    def __init__(self,xpos,ypos,height,width,appearance,nightappearance):
        super().__init__(xpos,ypos,height,width,False,appearance,nightappearance,(0.2,0.8,0.2,0.8))

class Decoration(Object): # Not necessary, but seemed nice
    def __init__(self,xpos,ypos,height,width,dynamic,appearance,nightappearance):
        super().__init__(xpos,ypos,height,width,dynamic,appearance,nightappearance)

class Interactive(Object):
    def __init__(self,xpos,ypos,height,width,dynamic,appearance,nightappearance):
        super().__init__(xpos,ypos,height,width,dynamic,appearance,nightappearance)

    def covers(self,possiblex,possibley):
        if self.xpos < possiblex < self.xpos + self.width and self.ypos < possibley < self.ypos + self.height:
            return True
        return False

class Print(Interactive): # Appearance should come from dictionary
    def __init__(self,xpos,ypos,height,width,animal,appearance):
        self.animal = animal
        super().__init__(xpos,ypos,height,width,False,appearance,appearance)

class Animal(Interactive): # *Every* animal should be a member of a subclass.
    def __init__(self,xpos,ypos,height,width,appearance,species,speed,strength):
        self.species = species
        self.speed = speed # Found in the initialization of the subclass.
        self.maxspeed = speed
        self.strength = strength
        self.maxstrength = strength
        self.currentmode = 0
        self.currentframe = 0
        self.health = 100
        self.dead = False
        super().__init__(xpos,ypos,height,width,True,appearance,appearance)
        self.ybase = ypos + height/2 # Co-ordinates of animals are different.

    def __str__(self):
        return self.species

    # Animals' x-positions and y-positions are unique in that they refer to the
    # center of the animal and not the upper left corner.  As such, they intersect
    # via a different method.
    def covers(self,possiblex,possibley):
        if self.xpos - self.width/3 < possiblex < self.xpos + self.width/3 and self.ypos - self.height/3 < possibley < self.ypos + self.height/3:
            return True
        return False

    def posok(self,x,y,obstacles): # Every animal will need to check positions
        for ob in obstacles: # in motion.
            if ob.collidesat(x,y):
                return False
        else:
            return True

    # Animals are drawn differently, as they have four framelists and direction,
    # and of course a different thing meant by xpos and ypos.
    def draw(self,screen,playerx,playery,window_width,window_height,night,time,scroll=True,leftx=0,topy=0):
        appearance = self.appearance[self.currentmode][self.currentframe]
        if scroll:
            screen.blit(appearance,(int(self.xpos-self.width/2-playerx+window_width/2),int(self.ypos-self.height/2-playery+window_height/2)))
        else:
            screen.blit(appearance,(self.xpos-self.width/2-leftx,self.ypos-self.height/2-topy))

    def orient(self,direction): # Figure out orientation (currentmode) from direction.
        if direction == -1:
            return 0
        while direction < 0:
            direction += 2*math.pi
        while direction > 2*math.pi:
            direction -= 2*math.pi
        if direction < math.pi/4: # Direction is counterclockwise from east.
            return 0
        elif direction < 3*math.pi/4:
            return 3
        elif direction < 5*math.pi/4:
            return 1
        elif direction < 7*math.pi/4:
            return 2
        else:
            return 0

    def framepush(self):
        if self.currentframe == len(self.appearance[self.currentmode]) - 1:
            self.currentframe = 0
        else:
            self.currentframe += 1

    def move(self,obstacles,animals,direction=135): # A default movement method, wherein "direction"
        directionr = direction*math.pi/180 # is degrees counterclockwise from east.
        newx = self.xpos + self.speed*math.cos(directionr) # Recall that positive
        newy = self.ypos - self.speed*math.sin(directionr) # y is southwards.
        while not self.posok(newx,newy,obstacles):
            direction += 1
            directionr = direction*math.pi/180
            newx = self.xpos + self.speed*math.cos(directionr) # Recall that positive
            newy = self.ypos - self.speed*math.sin(directionr) # y is southwards.
        self.currentmode = self.orient(directionr)
        self.framepush()
        self.xpos = newx
        self.ypos = newy # Do not call draw - the drawScreen will do that.
        self.ybase = newy + self.height

class Rabbit(Animal): # Animals' subclasses should - but do not yet - have unique
    def __init__(self,xpos,ypos,height,width,appearance): # move methods.
        super().__init__(xpos,ypos,height,width,appearance,'rabbit',20,0)

    def safe(self,obstacles,animals,direction): # For a rabbit, a direction is
        newx = self.xpos + 4*self.speed*math.cos(direction) # acceptable if no
        newy = self.ypos - 4*self.speed*math.sin(direction) # obstacles a jump away
        if not self.posok(newx,newy,obstacles): # and no non-rabbits in that
            return False                        # direction.
        for animal in animals:
            if not isinstance(animal,Rabbit):
                enemydir = math.atan2(self.ypos-animal.ypos,animal.xpos-self.xpos)
                if -0.5 < enemydir - direction < 0.5:
                    return False
        return True

    def move(self,obstacles,animals):
        # Rabbits will bounce in random directions, never toward other animals
        # or into obstacles.  They change directions every time they cycle
        # through their frames.
        if self.currentframe == len(self.appearance[self.currentmode]) - 1:
            direction = random.random()*2*math.pi
            attempts = 0
            while not self.safe(obstacles,animals,direction) and attempts < 6:
                direction = random.random()*2*math.pi
                attempts += 1
            if attempts == 6:
                direction = -1 # If rabbit cannot find safe direction, no motion.
        if direction != -1:
            self.xpos += self.speed*math.cos(direction)
            self.ypos -= self.speed*math.sin(direction)
            self.ybase = self.ypos + self.height
            self.currentmode = self.orient(direction)
        self.framepush()

class Deer(Animal):
    def __init__(self,xpos,ypos,height,width,appearance):
        self.direction = 0
        super().__init__(xpos,ypos,height,width,appearance,'deer',40,30)

class Bison(Animal):
    def __init__(self,xpos,ypos,height,width,appearance):
        super().__init__(xpos,ypos,height,width,appearance,'bison',50,100)

class Wolf(Animal): # Consider making part of a general animal class for the hunting game?
    def __init__(self,xpos,ypos,height,width,appearance,name):
        self.name = name
        super().__init__(xpos,ypos,height,width,appearance,'wolf',40,45)

    def identify(self,animals): # Wolves can tell predators from prey based on
        prey = []               # current strength, which enables them to
        predators = []          # scavenge.
        for animal in animals:
            if animal.species != 'wolf':
                if animal.strength > self.strength:
                    predators.append(animal)
                else:
                    prey.append(animal)
        return predators, prey

    def move(self,obstacles,animals):
        predators, prey = self.identify(animals)
        if len(predators) > 0: # If predators around, avoid all.
            directions_to_avoid = []
            for predator in predators:
                directions_to_avoid.append(math.atan2(self.ypos-predator.ypos,predator.xpos-self.xpos))
            if len(directions_to_avoid) == 1: # If one predator, run away.
                direction = directions_to_avoid[0] + math.pi
            else:
                directions_to_avoid.sort() # Otherwise, middle of the widest gap between predators.
                directions_to_avoid.append(directions_to_avoid[0]+2*math.pi)
                gaps = []
                for d in range(len(directions_to_avoid)-1):
                    gaps.append(directions_to_avoid[d+1]-directions_to_avoid[d])
                choice = gaps.index(max(gaps))
                direction = directions_to_avoid[choice] + gaps[choice]/2
        elif len(prey) > 0: # If there are prey, aim for the closest.
            distances = []
            for eachprey in prey:
                distances.append((self.xpos-eachprey.xpos)**2+(self.ypos-eachprey.ypos)**2) # Do not take root - just comparing.
            choice = prey[distances.index(min(distances))]
            direction = math.atan2(self.ypos-choice.ypos,choice.xpos-self.xpos)
        else: # If only other wolves, head north.
            direction = math.pi/2
        newx, newy = self.xpos + self.speed*math.cos(direction), self.ypos - self.speed*math.sin(direction)
        while not self.posok(newx,newy,obstacles):
            direction += 0.1
            newx, newy = self.xpos + self.speed*math.cos(direction), self.ypos - self.speed*math.sin(direction)
        self.xpos, self.ypos = newx, newy
        self.currentmode = self.orient(direction)
        self.framepush()


class World:
    def __init__(self,worldx,worldy,background,nightbackground,streams,forest,rocks,prints,decorations,settlements,animals):
        self.width = worldx # Dimensions of the world
        self.height = worldy
        self.background = background # Background, which should be scaled to the dimensions of the world.
        self.nightbackground = nightbackground # in its initializer, generateWorld().
        self.streams = streams # A list of lists of stream segments
        self.forest = forest # A list of trees
        self.rocks = rocks # A list of rocks (really, any obstacles)
        self.prints = prints # A list of prints
        self.decorations = decorations # A list of decoration objects
        self.settlements = settlements # A list of settlement objects
        self.animals = animals # A list of animals, currently excluding the player.
        self.obstacles = forest + rocks # All obstacles, to be sent to the posok() function
        self.interactives = prints + settlements + animals # All interactives, to be sent to the collision() function
        self.objectsofheight = forest + rocks + prints + decorations + settlements + animals
        self.objectsofheight.sort(key=lambda x:x.ybase) # Sort all blittables, to be sent to the drawscreen() function

    def turn(self): # For worlds with animals, move the animals in the world.
        for animal in self.animals:
            if animal.dead == False:
                animal.move(self.obstacles,self.animals)
            for otheranimal in self.animals:
                if animal.covers(otheranimal.xpos,otheranimal.ypos) and animal.strength > otheranimal.strength and animal.species != otheranimal.species:
                    otheranimal.health -= animal.strength
                    otheranimal.speed = otheranimal.health*otheranimal.maxspeed//100
                    if otheranimal.health <= 0:
                        otheranimal.dead = True
        self.objectsofheight.sort(key=lambda x:x.ybase) # A rare case in which bubble-sort might be more efficient, but
                                                        # we will use built-in sort anyway.
