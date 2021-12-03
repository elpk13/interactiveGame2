import pygame
import os

def get_menu_graphics(window_width,window_height):

    menuGraphics = { }

    # Load background, crop to same aspect ratio as window, and scale to size
    # of window.
    background = pygame.image.load(os.path.join('Assets','winter_forest_background.jpg')) # Image credit:
    bgw, bgh = background.get_width(), background.get_height() # Linnaea Mallette, publicdomainpictures.net
    if window_width / bgw > window_height > bgh:
        background = background.subsurface(int((bgw - bgh*window_width/window_height)/2),0,int(bgh*window_width/window_height),bgh)
    else:
        background = background.subsurface(0,int((bgh-bgw*window_height/window_width)/2),bgw,int(bgw*window_height/window_width))
    background = pygame.transform.scale(background,(window_width,window_height))
    menuGraphics['background'] = background

    # Load buttons and scale to appropriate portions of window.
    # For the main menu
    playbutton = pygame.image.load(os.path.join('Assets',"play_button.jpg"))
    playbutton = pygame.transform.scale(playbutton,(int(window_width/2),int(window_height/4)))
    settingsbutton = pygame.image.load(os.path.join('Assets',"settings_button.jpg"))
    settingsbutton = pygame.transform.scale(settingsbutton,(int(window_width/6),int(window_height/12)))
    aboutbutton = pygame.image.load(os.path.join('Assets',"about_button.jpg"))
    aboutbutton = pygame.transform.scale(aboutbutton,(int(window_width/6),int(window_height/12)))
    menuGraphics['about'] = aboutbutton
    menuGraphics['play'] = playbutton
    menuGraphics['settings'] = settingsbutton

    # For the settings page
    soundlabel = pygame.image.load(os.path.join('Assets',"sound_effects_label.png"))
    soundlabel = pygame.transform.scale(soundlabel,(int(window_width/2),int(window_height/6)))
    narrlabel = pygame.image.load(os.path.join('Assets',"narration_label.png"))
    narrlabel = pygame.transform.scale(narrlabel,(int(window_width/2),int(window_height/6)))
    menuGraphics['sound'] = soundlabel
    menuGraphics['narration'] = narrlabel

    # For the choose your character - wolves' portraits
    topleft = pygame.image.load(os.path.join('Assets',"Aspen_Headshot.png"))
    topcent = pygame.image.load(os.path.join('Assets',"Khewa_Headshot.png"))
    toprite = pygame.image.load(os.path.join('Assets',"Mani_Headshot.png"))
    basleft = pygame.image.load(os.path.join('Assets',"Nico_Headshot.png"))
    bascent = pygame.image.load(os.path.join('Assets',"Sparrow_Headshot.png"))
    basrite = pygame.image.load(os.path.join('Assets',"Timber_Headshot.png"))
    # Scale without distortion to uniform height.  Widths may continue to vary.
    topleft = pygame.transform.scale(topleft,(int(window_height*topleft.get_width()/(3*topleft.get_height())),int(window_height/3)))
    topcent = pygame.transform.scale(topcent,(int(window_height*topcent.get_width()/(3*topcent.get_height())),int(window_height/3)))
    toprite = pygame.transform.scale(toprite,(int(window_height*toprite.get_width()/(3*toprite.get_height())),int(window_height/3)))
    basleft = pygame.transform.scale(basleft,(int(window_height*basleft.get_width()/(3*basleft.get_height())),int(window_height/3)))
    bascent = pygame.transform.scale(bascent,(int(window_height*bascent.get_width()/(3*bascent.get_height())),int(window_height/3)))
    basrite = pygame.transform.scale(basrite,(int(window_height*basrite.get_width()/(3*basrite.get_height())),int(window_height/3)))
    menuGraphics['topleftwolf'] = topleft
    menuGraphics['topcentwolf'] = topcent
    menuGraphics['topritewolf'] = toprite
    menuGraphics['basleftwolf'] = basleft
    menuGraphics['bascentwolf'] = bascent
    menuGraphics['basritewolf'] = basrite

    # Chapter thumbnails for chapter menu - consider replacing with useful pictures.
    chap1thumb = pygame.image.load(os.path.join('Assets',"chap1_thumb.jpg"))
    chap2thumb = pygame.image.load(os.path.join('Assets',"chap2_thumb.jpg"))
    chap3thumb = pygame.image.load(os.path.join('Assets',"chap3_thumb.jpg"))
    chap1thumb = pygame.transform.scale(chap1thumb,(int(window_width/4),int(window_height/4)))
    chap2thumb = pygame.transform.scale(chap2thumb,(int(window_width/4),int(window_height/4)))
    chap3thumb = pygame.transform.scale(chap3thumb,(int(window_width/4),int(window_height/4)))
    menuGraphics['chap1'] = chap1thumb
    menuGraphics['chap2'] = chap2thumb
    menuGraphics['chap3'] = chap3thumb

    indicator = pygame.image.load(os.path.join('Assets',"indicator_paw.png"))
    indicator = pygame.transform.scale(indicator,(int(window_height/12),int(window_height/12)))
    indicator2 = pygame.transform.flip(indicator,True,False)
    menuGraphics['indicator'] = indicator
    menuGraphics['indicator2'] = indicator2

    return menuGraphics
