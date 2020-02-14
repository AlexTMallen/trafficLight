import pygame
import colors

class Lane:

    def __init__(self, rect, direction):
        self.rect = rect
        self.direction = direction

        if direction == 1:
            x = 0
            y = 0
        else:
            x = rect.width
            y = rect.height

        if rect.width > rect.height:
            y = (2 * rect.y + rect.height) // 2
        else:
            x = (2 * rect.x + rect.width) // 2

        self.start = (x, y)

    def draw(self, surface):
        pygame.draw.fill(surface, colors["lightGray"], self.rect)