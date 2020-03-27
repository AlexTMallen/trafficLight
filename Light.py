import pygame
import json


class Light:
    RADIUS = 10

    def __init__(self, lane, intersection):  # The literal center of the box
        self.color = "green"  # "green" "yellow" "red"
        with open("colors.json") as f:
            self.colors = json.loads(f.read())
        if lane.direction == (0, 1):
            self.center = (lane.start[0], intersection.y+intersection.rect.height)
        if lane.direction == (0, -1):
            self.center = (lane.start[0], intersection.y)
        if lane.direction == (1, 0):
            self.center = (intersection.x+intersection.rect.width, lane.start[1])
        if lane.direction == (-1, 0):
            self.center = (intersection.x, lane.start[1])

    def draw(self, surface):
        pygame.draw.circle(surface, self.colors[self.color], self.center, self.RADIUS)
