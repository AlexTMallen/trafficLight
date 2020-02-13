import pygame


class Car:

    def __init__(self, rect, color):
        self.rect = rect
        self.color = color

    def draw(self, surface):
        pygame.draw.fill(surface, self.color, self.rect)
