import threading

import pygame
import json
from Street import Street
from Lane import Lane
from Light import Light
import constants


class Intersection:
    """spawned automatically by main which does the math to find out where the streets intersect
    streets encompass all the lanes going into an intersection so there will always be TWO streets (horiz and vert)"""

    def __init__(self, streetH, streetV):
        self.streetH = streetH
        self.streetV = streetV
        self.lightColors = ['green', 'red']
        self.carsInIntersection = 0
        self.totalCycleLength = 32*constants.SECOND

        # calculate coordinates of intersection
        self.x = streetV.point1[0] - streetV.width // 2
        self.y = streetH.point1[1] - streetH.width // 2
        self.rect = pygame.Rect(self.x, self.y, streetV.width, streetH.width)

        # lists holding all lights opposite a lane of that direction
        self.lightsUp = []
        self.lightsDown = []
        self.lightsLeft = []
        self.lightsRight = []
        self.lights = []
        # spawn lights for horizontal street
        # TODO: possibly restructure how we store lights to account for different kinds of lights
        for current_lane in self.streetH.lanesPos + self.streetH.lanesPosLeft:
            light = Light(current_lane, self)
            self.lightsRight.append(light)
            self.lights.append(light)
            current_lane.light = light
        for current_lane in self.streetH.lanesNeg + self.streetH.lanesNegLeft:
            light = Light(current_lane, self)
            self.lightsLeft.append(light)
            self.lights.append(light)
            current_lane.light = light
        # creates lights for vertical street
        for current_lane in self.streetV.lanesPos + self.streetV.lanesPosLeft:
            light = Light(current_lane, self)
            self.lightsDown.append(light)
            self.lights.append(light)
            current_lane.light = light
        for current_lane in self.streetV.lanesNeg + self.streetV.lanesNegLeft:
            light = Light(current_lane, self)
            self.lightsUp.append(light)
            self.lights.append(light)
            current_lane.light = light

        with open("colors.json") as f:
            self.lightColors = json.loads(f.read())
        
        
        # a list of default cycles
        self.redCycle = ['red' for i in range(self.streetH.numLanes + self.streetV.numLanes)]
        self.greenCycle = ['green' for i in range(self.streetH.numLanes + self.streetV.numLanes)]
        self.hgreenCycle = ['red' for i in range(self.streetH.numLanes + self.streetV.numLanes)]
        for i in range(self.streetH.numLanes):
            self.hgreenCycle[i] = 'green'
            
        self.hyellowCycle = ['red' for i in range(self.streetH.numLanes + self.streetV.numLanes)]
        for i in range(self.streetH.numLanes):
            self.hyellowCycle[i] = 'yellow'
            
        self.vgreenCycle = ['red' for i in range(self.streetH.numLanes + self.streetV.numLanes)]
        for i in range(self.streetH.numLanes, self.streetH.numLanes + self.streetV.numLanes):
            self.vgreenCycle[i] = 'green'
            
        self.vyellowCycle = ['red' for i in range(self.streetH.numLanes + self.streetV.numLanes)]
        for i in range(self.streetH.numLanes, self.streetH.numLanes + self.streetV.numLanes):
            self.vyellowCycle[i] = 'yellow'
        




    

        
        

    def draw(self, surface):
        pygame.draw.rect(surface, self.lightColors["darkG"], self.rect)


    def changeToCycle(self, cycle):
        for i in range (self.streetH.numLanes + self.streetV.numLanes):
            self.lights[i].color = cycle[i]

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


    def changeCycle(self, time):
        # if time == 0:
        #     self.changeToCycle(self.hgreenCycle)
        #
        # elif time == 10*constants.SECOND:
        #     self.changeToCycle(self.hyellowCycle)
        #
        # elif time == 14*constants.SECOND:
        #     self.changeToCycle(self.redCycle)
        #
        # elif time == 16*constants.SECOND:
        #     self.changeToCycle(self.vgreenCycle)
        #
        # elif time == 26*constants.SECOND:
        #     self.changeToCycle(self.vyellowCycle)
        #
        # elif time == 30*constants.SECOND:
        #     self.changeToCycle(self.redCycle)
        #
        # elif time == 32*constants.SECOND:
        #     self.changeToCycle(self.hgreenCycle)
        self.changeToCycle(self.greenCycle)
        
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
