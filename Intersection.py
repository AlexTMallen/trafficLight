import pygame
import json

class Intersection:

    def __init__(self, horizontalLanes, verticalLanes):
        self.horizontalLanes = horizontalLanes
        self.verticalLanes = verticalLanes
        self.rect = pygame.Rect(verticalLanes[0].rect.x, horizontalLanes[0].rect.y, verticalLanes[0].width * len(verticalLanes),
                         horizontalLength[0].width * len(horizontalLanes))
        with open("colors.json") as f:
            text = f.read()
            self.colors = json.loads(text)

    def draw(self, surface):
        pygame.draw.fill(surface, self.colors["lightGray"], self.rect)