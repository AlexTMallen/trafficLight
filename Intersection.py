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
        self.timer = threading.Timer(5.0, self.changeLights, self.lightColors.index('green'))
        self.cycles = [
            []
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
            self.lightsRight.append(Light(current_lane, self))
            self.lights.append(Light(current_lane, self))
        for current_lane in self.streetH.lanesNeg:
            self.lightsRight.append(Light(current_lane, self))
            self.lights.append(Light(current_lane, self))
        for current_lane in self.streetV.lanesPos:
            self.lightsRight.append(Light(current_lane, self))
            self.lights.append(Light(current_lane, self))
        for current_lane in self.streetV.lanesNeg:
            self.lightsRight.append(Light(current_lane, self))
            self.lights.append(Light(current_lane, self))


        with open("colors.json") as f:
            self.lightColors = json.loads(f.read())

    def draw(self, surface):
        pygame.draw.rect(surface, self.lightColors["darkG"], self.rect)
        '''
        for light in self.lightsUp:
            light.color = self.lightColors[0]
        for light in self.lightsDown:
            light.color = self.lightColors[0]
        for light in self.lightsLeft:
            light.color = self.lightColors[1]
        for light in self.lightsRight:
            light.color = self.lightColors[1]

    '''
    def changeTo(self, cycle):
        for light in self.lights:
            if light.color == 'green':
                light.color = 'yellow'
                #wait 3.5 seconds
                light.color = 'red'

        for light in cycle:
            self.lights[light].color = 'green'

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
