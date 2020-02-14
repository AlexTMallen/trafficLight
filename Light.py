import pygame

class Light:

    def __init__(self, rect, color):
        self.rect = rect
        self.color = color

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)