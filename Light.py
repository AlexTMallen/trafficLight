import pygame

class Light:
    RADIUS = 10

    def __init__(self, lane, intersection): ##the literal center of the box
        self.color = "green"
        if lane.direction == (0, 1):
            self.center = (lane.start[0], intersection.y+intersection.rect.height)
        if lane.direction == (0, -1):
            self.center = (lane.start[0], intersection.y)
        if lane.direction == (1, 0):
            self.center = (intersection.x+intersection.rect.width, lane.start[1])
        if lane.direction == (-1, 0):
            self.center = (intersection.x, lane.start[1])



    def drawLight(self, surface):
        pygame.draw.circle(surface, self.color, self.center, self.RADIUS)

    def changeLights(self):
        pass
