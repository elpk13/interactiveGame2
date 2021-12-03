# Like pygame, this is not a standard module. It can be downloaded via pip
from PIL import Image # Limited imports
import os

def lighten_image(path,extent):
    oldimage = Image.open(path)
    pathname = str(path)
    imagename = pathname.split('\\')[-1][:-4]
    newimage = Image.new(oldimage.mode,oldimage.size)
    #print(oldimage.mode)
    #print(oldimage.getpixel((0,0)))
    if oldimage.mode == "RGBA":
        for x in range(oldimage.size[0]):
            for y in range(oldimage.size[1]):
                oldpixel = oldimage.getpixel((x,y))
                newpixel = (int(oldpixel[0]*extent), int(oldpixel[1]*extent), int(oldpixel[2]*extent), oldpixel[3])
                newimage.putpixel((x,y),newpixel)
        newimage.save(os.path.join('Assets', imagename + '_light.png'))
    elif oldimage.mode == "RGB":
        for x in range(oldimage.size[0]):
            for y in range(oldimage.size[1]):
                oldpixel = oldimage.getpixel((x,y))
                newpixel = (int(oldpixel[0]*extent), int(oldpixel[1]*extent), int(oldpixel[2]*extent))
                newimage.putpixel((x,y),newpixel)
        newimage.save(os.path.join('Assets', imagename + '_light.jpg'))

def nightenImage(path):
    oldimage = Image.open(path)
    pathname = str(path)
    imagename = pathname[:-4]
    newimage = Image.new(oldimage.mode,oldimage.size)
    if oldimage.mode == "RGBA":
        for x in range(oldimage.size[0]):
            for y in range(oldimage.size[1]):
                oldpixel = oldimage.getpixel((x,y))
                newpixel = (int(oldpixel[0]/2), int(oldpixel[1]/2), int(oldpixel[2]/2), oldpixel[3])
                newimage.putpixel((x,y),newpixel)
        newimage.save(os.path.join(imagename + '_Night.png'))
    elif oldimage.mode == "RGB":
        for x in range(oldimage.size[0]):
            for y in range(oldimage.size[1]):
                oldpixel = oldimage.getpixel((x,y))
                newpixel = (int(oldpixel[0]/2), int(oldpixel[1]/2), int(oldpixel[2]/2))
                newimage.putpixel((x,y),newpixel)
        newimage.save(os.path.join(imagename + '_Night.jpg'))

def reopacity(streampath):
    oldimage = Image.open(streampath)
    newimage = Image.new("RGBA",oldimage.size)
    for x in range(oldimage.size[0]):
        for y in range(oldimage.size[1]):
            oldpixel = oldimage.getpixel((x,y))
            if oldpixel[0] + oldpixel[1] + oldpixel[2] > 730:
                newpixel = (0,0,0,0)
            else:
                newpixel = (oldpixel[0],oldpixel[1],oldpixel[2],255)
            newimage.putpixel((x,y),newpixel)
    newimage.save(streampath)
    nightenImage(streampath)

def fallTree(path):
    oldimage = Image.open(path)
    pathname = str(path)
    imagename = pathname.split('\\')[-1][:-4]
    imagenames = imagename.split('Summer')
    newimage = Image.new(oldimage.mode,oldimage.size)
    if oldimage.mode == "RGBA":
        for x in range(oldimage.size[0]):
            for y in range(oldimage.size[1]):
                oldpixel = oldimage.getpixel((x,y))
                if oldpixel[1] > oldpixel [0]:
                    newpixel = (int(oldpixel[1]), int(oldpixel[1]/2), oldpixel[2], oldpixel[3])
                else:
                    newpixel = oldpixel
                newimage.putpixel((x,y),newpixel)
        newimage.save(os.path.join('Animations','Trees','Autumn'.join(imagenames) + '.png'))
    elif oldimage.mode == "RGB":
        for x in range(oldimage.size[0]):
            for y in range(oldimage.size[1]):
                oldpixel = oldimage.getpixel((x,y))
                if oldpixel[1] > oldpixel [0]:
                    newpixel = (int(oldpixel[1]), int(oldpixel[1]/2), oldpixel[2])
                else:
                    newpixel = oldpixel
                newimage.putpixel((x,y),newpixel)
        newimage.save(os.path.join('Animations','Trees','Autumn'.join(imagenames) + '.png'))

def completeTree(tree,seasonal=True):
    if seasonal:
        for i in range(1,8):
            fallTree(os.path.join('Animations','Trees',tree+'_Summer000'+str(i)+'.png'))
            nightenImage(os.path.join('Animations','Trees',tree+'_Summer000'+str(i)+'.png'))
            nightenImage(os.path.join('Animations','Trees',tree+'_Autumn000'+str(i)+'.png'))
            nightenImage(os.path.join('Animations','Trees',tree+'_Winter000'+str(i)+'.png'))
    else:
        for i in range(1,8):
            nightenImage(os.path.join('Animations','Trees',tree+'000'+str(i)+'.png'))

def nopacity(path,mark=True):
    oldimage = Image.open(path)
    newimage = Image.new(oldimage.mode,oldimage.size)
    imagename = str(path).split('\\')[-1][:-4]
    for x in range(oldimage.size[0]):
        for y in range(oldimage.size[1]):
            oldpixel = oldimage.getpixel((x,y))
            if oldpixel[3] in [0,255]:
                newimage.putpixel((x,y),oldpixel)
            else:
                newpixel = (oldpixel[0],oldpixel[1],oldpixel[2],255)
                newimage.putpixel((x,y),newpixel)
    if mark:
        newimage.save(os.path.join('Animations','Nopacity',imagename+'nopaque.png'))
    else:
        newimage.save(path)

def nopacity2(path,threshold,mark=True):
    oldimage = Image.open(path)
    newimage = Image.new(oldimage.mode,oldimage.size)
    imagename = str(path).split('\\')[-1][:-4]
    for x in range(oldimage.size[0]):
        for y in range(oldimage.size[1]):
            oldpixel = oldimage.getpixel((x,y))
            if oldpixel[3] in [0,255]:
                newimage.putpixel((x,y),oldpixel)
            else:
                if oldpixel[3] > threshold:
                    newpixel = (oldpixel[0],oldpixel[1],oldpixel[2],255)
                else:
                    newpixel = (oldpixel[0],oldpixel[1],oldpixel[2],0)
                newimage.putpixel((x,y),newpixel)
    if mark:
        newimage.save(os.path.join('Animations','Nopacity',imagename+'nopaque.png'))
    else:
        newimage.save(path)

# lighten_image(os.path.join('Assets','Aspen_Headshot.png'),0.5)
# will make a 50% darker 'Aspen_Headshot.png' called 'Aspen_Headshot_light.png'

#lighten_image(os.path.join('Assets','oak_tree.png'),0.5)
#lighten_image(os.path.join('Assets','pine_tree.png'),0.5)
#for i in range(1,9):
#    nopacity2(os.path.join('Animations','Nopacity','Outline_Walking_Away000'+str(i)+'_nopaque.png'),128)
#    nopacity2(os.path.join('Animations','Nopacity','Outline_Walking_Forward000'+str(i)+'_nopaque.png'),128)
#    nopacity2(os.path.join('Animations','Nopacity','Outline_Walking_Right000'+str(i)+'_nopaque.png'),128)
#nopacity2(os.path.join('Animations','Nico','Nico_Walking_Away0002.png'),128)
#for i in range(1,9):
#    nopacity(os.path.join('Animations','Nico','Nico_Walking_Away000'+str(i)+'.png'),False)
#    nopacity(os.path.join('Animations','Nico','Nico_Walking_Forward000'+str(i)+'.png'),False)
#    nopacity(os.path.join('Animations','Nico','Nico_Walking_Right000'+str(i)+'.png'),False)

#completeTree('White_Oak')
#completeTree('Spruce',False)
#for aim in ['30','45','60','30s','45s','60s','30-45','45-60','60-30','30-60','60-45','45-30']:
#    for i in range(1,4):
#        reopacity(os.path.join('Animations','Streams',aim+'000'+str(i)+'.png'))
for i in range(1,8):
    reopacity(os.path.join('Animations','Trees','Spruce000'+str(i)+'.png'))
