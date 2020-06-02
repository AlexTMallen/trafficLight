import pygame


class Button:
    #write
    #use is whether the button adds or deletes
    #item is what the button adds or deletes ()
    WIDTH = 30
    LENGTH = 60
    mouseover = False
    def __init__(self, color,use, item, mouse, pos):
        self.color = color
        mouse = pygame.mouse.get_pos()


#draw one button
#make button click-draggable?

def draw(self, surface, mouseover=True):

    if mouseover:
        pygame.draw.rect(surface, self.newcolor, self.newcolor)
    pygame.draw.rect(surface, self.color, self.rect)


#make the button interactive

def purpose(button, use, item):
    if click

