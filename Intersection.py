import pygame
import json
from Street import Street
from Lane import Lane
from Light import Light


class Intersection:
    """spawned automatically by main which does the math to find out where the streets intersect
    streets encompass all the lanes going into an intersection so there will always be TWO streets (horiz and vert)"""

    def __init__(self, streetH, streetV):
        self.streetH = streetH
        self.streetV = streetV

        # calculate coordinates of intersection
        self.x = streetV.point1[0] - streetV.numPos * Lane.WIDTH
        self.y = streetH.point1[1] - streetH.numNeg * Lane.WIDTH
        wide = (streetV.numPos + streetV.numNeg) * Lane.WIDTH
        long = (streetH.numPos + streetH.numNeg) * Lane.WIDTH
        self.rect = pygame.Rect(self.x, self.y, wide, long)

        # lists holding all lights opposite a lane of that direction
        self.lightsUp = []
        self.lightsDown = []
        self.lightsLeft = []
        self.lightsRight = []
        # spawn lights for horizontal street
        for current in self.streetH.lanesPos:
            self.lightsRight.append(Light(current, self))
        for current in self.streetH.lanesNeg:
            self.lightsRight.append(Light(current, self))
        for current in self.streetV.lanesPos:
            self.lightsRight.append(Light(current, self))
        for current in self.streetV.lanesNeg:
            self.lightsRight.append(Light(current, self))


        with open("colors.json") as f:
            self.colors = json.loads(f.read())

    def draw(self, surface):
        pygame.draw.rect(surface, self.colors["darkG"], self.rect)

    def changeLights(self):
        # use traffic data to determine when to change the lights
        pass