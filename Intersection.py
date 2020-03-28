import threading

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
        self.lightColors = ['green', 'red']
        self.carsInIntersection = 0

        # a list of lists of which green lights can be on at the same time
        self.cycles = [
            list(range(self.streetH.numLanes)),  # horizontal lights
            list(range(self.streetH.numLanes, self.streetH.numLanes + self.streetV.numLanes))  # vertical lights
        ]

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
        self.lights = []
        # spawn lights for horizontal street
        for current_lane in self.streetH.lanesPos:
            light = Light(current_lane, self)
            self.lightsRight.append(light)
            self.lights.append(light)
            current_lane.light = light
        for current_lane in self.streetH.lanesNeg:
            light = Light(current_lane, self)
            self.lightsLeft.append(light)
            self.lights.append(light)
            current_lane.light = light
        for current_lane in self.streetV.lanesPos:
            light = Light(current_lane, self)
            self.lightsDown.append(light)
            self.lights.append(light)
            current_lane.light = light
        for current_lane in self.streetV.lanesNeg:
            light = Light(current_lane, self)
            self.lightsUp.append(light)
            self.lights.append(light)
            current_lane.light = light


        with open("colors.json") as f:
            self.lightColors = json.loads(f.read())

    def draw(self, surface):
        pygame.draw.rect(surface, self.lightColors["darkG"], self.rect)

    def changeToYellow(self):
        for light in self.lights:
            if light.color == 'green':
                light.color = 'yellow'

    def changeToRed(self):
        for light in self.lights:
            light.color = 'red'

    def changeToCycle(self, cycle):
        for light in self.lights:
            light.color = 'red'

        for light in cycle:
            self.lights[light].color = 'green'

    def findStops(self):
        for light in self.lights:
            if light.color == 'red':
                if light.lane.direction == (1, 0):
                    light.lane.stopPoints.append(self.x)
                if light.lane.direction == (-1, 0):
                    light.lane.stopPoints.append(self.x + self.wide)
                if light.lane.direction == (0, 1):
                    light.lane.stopPoints.append(self.y)
                if light.lane.direction == (0, -1):
                    light.lane.stopPoints.append(self.y + self.long)
            if light.color == 'green':
                light.lane.stopPoints = []

# currently not being called
    def changeLights(self, i):
        # use traffic data to determine when to change the lights
        if 'green' in self.lightColors:
            self.lightColors[i] = 'yellow'
            timer = threading.Timer(3.5, self.changeLights, i)
            timer.start()
        elif 'yellow' in self.lightColors:
            self.lightColors[i] = 'red'
            timer = threading.Timer(1.0, self.changeLights, i)
            timer.start()
        else:
            self.lightColors[(i + 2) % 2] = 'green'
            timer = threading.Timer(5.0, self.changeLights, (i + 2) % 2)
            timer.start()
