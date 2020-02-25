import pygame
import json

class Lane:

    def __init__(self, rect, direction):
        self.rect = rect
        self.direction = direction
        with open("colors.json") as f:
            text = f.read()
            self.colors = json.loads(text)

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
        pygame.draw.rect(surface, self.colors["lightG"], self.rect)