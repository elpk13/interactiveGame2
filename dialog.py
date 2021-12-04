import pygame
pygame.init()
import os

# The linebreak function yields a list of image-type objects rendering a line
# of the given text of the appropriate width.
def linebreak(text,width,maxheight=0,font=pygame.font.SysFont('constantia',24),color=(239,228,176)):
    pars = text.split('\n\n')
    for i in range(len(pars)):
        par = pars[i]
        par = par.replace('\n',' ')
        par = par.replace('  ',' ')
        pars[i] = par
    text = ' \n '.join(pars)
    words = text.split(' ') # This is NOT equivalent to text.split()
    lines = []
    line = words[0]
    if font.render(words[0],True,color).get_width() > width:
        return False         # Linebreak yields false if a word is too long for
    for word in words[1:]:   # the width or the whole exceeds a maximum height.
        if font.render(word,True,color).get_width() > width:
            return False
        linextend = ' '.join([line,word])
        if word == '\n':
            lines.append(font.render(line,True,color))
            #lines.append(line)
            line = ''
        elif font.render(linextend,True,color).get_width() > width:
            lines.append(font.render(line,True,color))
            #lines.append(line)
            line = word
        else:
            line = linextend
    lines.append(font.render(line,True,color))
    #lines.append(line)
    lineheight = lines[0].get_height()
    if maxheight > 0 and lineheight*len(lines) > maxheight:
        return False
    else:
        return lines

# Bliterate takes a text string, line-breaks it, and blits it.
# It yields the y-position ideal for blitting text beneath it,
# as well as the width of the text block.
# Buffer here is used between lines and between block edges - the
# dialog method has its own buffers.
def bliterate(screen,text,x,y,width,height=0,justify=False,buffer=0,font=pygame.font.SysFont('constantia',24),color=(239,228,176)):
    lines = linebreak(text,width-2*buffer,height-2*buffer,font)
    widths = []
    if lines == False: # Display error for lines if word too wide or text too tall.
        screen.blit(font.render('Error',True,(255,0,0)),(x,y))
    else:
        runningheight = y + buffer
        change = int(lines[0].get_height() + buffer / 2)
        for line in lines:
            if justify:
                screen.blit(line,(int(x+(width-line.get_width())/2),runningheight))
            else:
                screen.blit(line,(x+buffer,runningheight))
            widths.append(line.get_width())
            runningheight += change
    return runningheight, max(widths)

# Dialog produces a dialog with options and returns the player's choice.
def dialog(screen,question,options,image=None,width=0.5,height=1/3):
    # Dialog is always centered and rests on the horizontal mid-line of the screen.
    # Width and height arguments between 0 and 1 determine portion of screen occupied.
    swidth, sheight = screen.get_width(), screen.get_height()
    dialogbg = pygame.image.load(os.path.join("Assets","Dialog_Panel.jpg"))
    dialogbg = pygame.transform.scale(dialogbg,(int(width*swidth),int(height*sheight)))
    paw = pygame.image.load(os.path.join("Assets","indicator_paw.png"))
    paw = pygame.transform.scale(paw,(int(sheight/12),int(sheight/12)))

    runningwidth = int((1-width)*swidth/2)
    runningheight = int(sheight/3 - height*sheight/2)
    buffer = 10 # On the sides of image, etc.
    textbuffer = 20 # Between lines.
    myfont = pygame.font.SysFont('constantia',24)
    TEXT_COLOR = (239,228,176)
    choice = 0

    # Drawscreen blits options using bliterate.
    # NOTE!:  Heights are not passed to bliterate here, so it will not
    # print error if the whole of the answers runs down below the base of
    # the dialog box.  Alternative lines are shown, commented.
    # If text and paw escaped dialog, it will have blit error b/c not being
    # drawn over - I just don't know what we'd rather do if our text is too
    # much, besides write something shorter.
    def drawscreen(runningwidth,runningheight,buffer,image):
        screen.blit(dialogbg,(runningwidth,runningheight))
        runningwidth += buffer
        runningheight += buffer
        if question != "":
            runningheight = bliterate(screen,question,runningwidth,runningheight,swidth-2*runningwidth,justify=True,font=myfont)[0]
            #runningheight = bliterate(screen,question,runningwidth,runningheight,swidth-2*runningwidth,maxheight=int(sheight/2-buffer-runningheight),justify=True,font=myfont)[0]
        if image != None:
            image = pygame.transform.scale(image,(int(0.5*width*swidth-2*buffer),int(sheight/3+height*sheight/2-runningheight-buffer)))
            screen.blit(image,(int(swidth/2 + buffer),runningheight))
        optionpos = []
        for option in options:
            newheight, optwidth = bliterate(screen,option,runningwidth,runningheight,int(swidth/2-sheight/12-runningwidth-buffer),font=myfont)
            #newheight, optwidth = bliterate(screen,option,runningwidth,runningheight,int(swidth/2-sheight/12-runningwidth-buffer),maxheight=int(sheight/2-buffer-runningheight),font=myfont)
            optionpos.append((runningwidth+optwidth+buffer,int((newheight+runningheight)/2-sheight/24)))
            runningheight = newheight + textbuffer
        screen.blit(paw,optionpos[choice])
        pygame.display.update()

    drawscreen(runningwidth,runningheight,buffer,image)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return choice
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and choice > 0:
                    choice -= 1
                elif event.key == pygame.K_DOWN and choice < len(options) - 1:
                    choice += 1
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return choice
                drawscreen(runningwidth,runningheight,buffer,image)

def akela(screen,text,options=[]):
    akelapic = pygame.image.load(os.path.join('Assets','Akela.png'))
    if options == []:
        return dialog(screen,'Akela',[text],akelapic)
    else:
        return dialog(screen,text,options,akelapic)

# Dialog test with long text.
#testimage = pygame.image.load(os.path.join('Assets','Aspen_Headshot.png'))
#screen = pygame.display.set_mode((1200,900))
#longquestion = 'To be or not to be'
#longanswers = ["Whether 'tis nobler in the mind to suffer",
#"The slings and arrows of outrageous fortune,",
#"Or to take arms against a sea of troubles,",
#"And by opposing end them..."] # -- William Shakespeare, Hamlet
#dialog(screen,longquestion,longanswers,testimage)


#longtext = '''Jarndyce and Jarndyce drones on.
#This scarecrow of a suit has, in course of time, become so complicated that no
#man alive knows what it means.  The parties to it understand it least, but it
#has been observed that no two Chancery lawyers can talk about it for five
#minutes without coming to a total disagreement as to all the premises.
#Innumerable children have been born into the cause; innumerable old people have
#died out of it.  Scores of persons have deliriously found themselves made
#parties in Jarndyce and Jarndyce without knowing how or why; whole families
#have inherited legendary hatreds with the suit.  The little plaintiff or
#defendant who was promised a new rocking-horse when Jarndyce and Jarndyce
#should be settled has grown up, possessed himself of a real horse, and trotted
#away into the other world...''' # - from Charles Dickens's 'Bleak House'
#print(linebreak(longtext,400))
#print(longtext)

#txtwbreaks = '''Of mans first disobedience, and the Fruit
#
#Of that forbidden Tree, whose mortal tast
#
#Brought Death into the World, and all our Woe,
#
#With loss of Eden, till one greater Man
#
#Restore us, and regain the blissful Seat,
#
#Sing Heav'nly Muse, that on the secret top
#
#Of Oreb, or of Sinai, didst inspire
#
#That Shepherd, who first taught the chosen Seed,
#
#In the Beginning how the Heav'ns and Earth
#
#Rose out of Chaos...''' # - from John Milton, 'Paradise Lost'
#print(txtwbreaks)
#print(linebreak(txtwbreaks,200))
