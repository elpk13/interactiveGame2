#The purpose of this file is to host the choose your character screen that follows the main menu
#eventually a difficulty setting will be integrated here or on the settings page?

#import necessary systems
import pygame

def character_select(screen,menuGraphics):
    window_width, window_height = screen.get_width(), screen.get_height()
    settingsfile = open("settings.txt",'r')
    currentsettings = settingsfile.readlines()
    settingsfile.close()
    indicator1rad, ypos1, ypos2 = int(window_height/24), int(window_height/2)-int(window_height)/24, window_height-int(window_height/24)
    positions1list = [(int(window_width/6)-indicator1rad,ypos1),(int(window_width/2)-indicator1rad,ypos1),(int(5*window_width/6)-indicator1rad,ypos1),
        (int(window_width/6)-indicator1rad,ypos2),(int(window_width/2)-indicator1rad,ypos2),(int(5*window_width/6)-indicator1rad,ypos2)]
    position1 = int(currentsettings[2][0]) # Current character is chosen by number on third line of settings file.

    def draw_char_screen(screen,menuGraphics,window_width,window_height):
        screen.blit(menuGraphics['background'], (0,0)) # Portrait widths may vary, so justify.
        screen.blit(menuGraphics['topleftwolf'],(int(window_width/6-menuGraphics['topleftwolf'].get_width()/2),int(window_height/12)))
        screen.blit(menuGraphics['topcentwolf'],(int(window_width/2-menuGraphics['topcentwolf'].get_width()/2),int(window_height/12)))
        screen.blit(menuGraphics['topritewolf'],(int(5*window_width/6-menuGraphics['topritewolf'].get_width()/2),int(window_height/12)))
        screen.blit(menuGraphics['basleftwolf'],(int(window_width/6-menuGraphics['basleftwolf'].get_width()/2),int(7*window_height/12)))
        screen.blit(menuGraphics['bascentwolf'],(int(window_width/2-menuGraphics['bascentwolf'].get_width()/2),int(7*window_height/12)))
        screen.blit(menuGraphics['basritewolf'],(int(5*window_width/6-menuGraphics['basritewolf'].get_width()/2),int(7*window_height/12)))
        screen.blit(menuGraphics['indicator'],positions1list[position1])
        pygame.display.update()
    draw_char_screen(screen,menuGraphics,window_width,window_height)

    runningcyc = True
    while runningcyc:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If 'x' button selected, end
                return 'stop'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and position1 % 3 != 2:
                    position1 += 1
                elif event.key == pygame.K_LEFT and position1 % 3 != 0:
                    position1 -= 1
                elif event.key == pygame.K_UP and position1 > 2:
                    position1 -= 3
                elif event.key == pygame.K_DOWN and position1 < 3:
                    position1 += 3
                draw_char_screen(screen,menuGraphics,window_width,window_height)
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    currentsettings[2] = str(position1) + '\n'
                    settingsfile = open("settings.txt",'w')
                    for eachline in currentsettings:
                        settingsfile.write(eachline)
                    settingsfile.close()
                    runningcyc = False
