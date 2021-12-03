#The purpose of this file is to host the choose your chapter screen that follows the choose your
#eventually a difficulty setting will be integrated here or on the settings page?

#import necessary systems
import pygame

def chapter_select(screen,menuGraphics):
    window_width, window_height = screen.get_width(), screen.get_height()
    positionslist = [(int(window_width/6),int(7*window_height/12)),(int(window_width/2),int(7*window_height/12)),
        (int(5*window_width/6),int(7*window_height/12))]
    position = 0

    def draw_chapter_screen(screen,menuGraphics,window_width,window_height):
        screen.blit(menuGraphics['background'], (0,0))
        screen.blit(menuGraphics['chap1'],(int(window_width/16),int(window_height/4)))
        screen.blit(menuGraphics['chap2'],(int(3*window_width/8),int(window_height/4)))
        screen.blit(menuGraphics['chap3'],(int(11*window_width/16),int(window_height/4)))
        screen.blit(menuGraphics['indicator'],positionslist[position])
        pygame.display.update()
    draw_chapter_screen(screen,menuGraphics,window_width,window_height)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If 'x' button selected, end
                return 'stop'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and position < 2:
                    position += 1
                elif event.key == pygame.K_LEFT and position > 0:
                    position -= 1
                draw_chapter_screen(screen,menuGraphics,window_width,window_height)
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return position
