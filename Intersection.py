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
        self.carsInIntersection = 0

        self.hg = 10  # horizontalGreenTime
        self.hy = 3  # horizontalYellowTime
        self.hr = 2  # horizontalRedTime
        self.hlg = 10  # horizontalLeftGreen
        self.hly = 3  # horizontalLeftYellow
        self.hlr = 2  # horizontalLeftRed
        if self.streetH.numLeftOnly == 0:
            self.hlg = 0
            self.hly = 0
            self.hlr = 0
        self.vg = 10  # verticalGreenTime
        self.vy = 3  # verticalYellowTime
        self.vr = 2  # verticalRedTime
        self.vlg = 10  # verticalLeftGreen
        self.vly = 3  # verticalLeftYellow
        self.vlr = 2  # verticalLeftRed
        if self.streetV.numLeftOnly == 0:
            self.vlg = 0
            self.vly = 0
            self.vlr = 0

        self.totalCycleLength = (self.hg+self.hy+self.hr+self.hlg+self.hly+self.hlr+self.vg+self.vy+self.vr+self.vlg+self.vly+self.vlr) * constants.SECOND

        # calculate coordinates of intersection
        self.x = streetV.point1[0] - streetV.width // 2
        self.y = streetH.point1[1] - streetH.width // 2
        self.rect = pygame.Rect(self.x, self.y, streetV.width, streetH.width)

        # lists holding all lights opposite a lane of that direction
        self.lights = []

        # spawn lights for horizontal street
        for current_lane in self.streetH.lanesPos:
            light = Light(current_lane, self)
            self.lights.append([light, 'hPos'])
            current_lane.light = light
        for current_lane in self.streetH.lanesPosLeft:
            light = Light(current_lane, self)
            self.lights.append([light, "hPosLeft"])
            current_lane.light = light
        for current_lane in self.streetH.lanesNeg:
            light = Light(current_lane, self)
            self.lights.append([light, 'hNeg'])
            current_lane.light = light
        for current_lane in self.streetH.lanesNegLeft:
            light = Light(current_lane, self)
            self.lights.append([light, 'hNegLeft'])
            current_lane.light = light

        # creates lights for vertical street
        for current_lane in self.streetV.lanesPos:
            light = Light(current_lane, self)
            self.lights.append([light, 'vPos'])
            current_lane.light = light
        for current_lane in self.streetV.lanesPosLeft:
            light = Light(current_lane, self)
            self.lights.append([light, 'vPosLeft'])
            current_lane.light = light
        for current_lane in self.streetV.lanesNeg:
            light = Light(current_lane, self)
            self.lights.append([light, 'vNeg'])
            current_lane.light = light
        for current_lane in self.streetV.lanesNegLeft:
            light = Light(current_lane, self)
            self.lights.append([light, 'vNegLeft'])
            current_lane.light = light

        with open("colors.json") as f:
            self.lightColors = json.loads(f.read())

        # a list of cycles
        self.redCycle = ['red' for i in range(len(self.lights))]

        self.hgreenCycle = ['red' for i in range(len(self.lights))]
        for i in range(len(self.lights)):
            if self.lights[i][1] == 'hPos' or self.lights[i][1] == 'hNeg':
                self.hgreenCycle[i] = 'green'

        self.hyellowCycle = ['red' for i in range(len(self.lights))]
        for i in range(len(self.lights)):
            if self.lights[i][1] == 'hPos' or self.lights[i][1] == 'hNeg':
                self.hyellowCycle[i] = 'yellow'

        self.vgreenCycle = ['red' for i in range(len(self.lights))]
        for i in range(len(self.lights)):
            if self.lights[i][1] == 'vPos' or self.lights[i][1] == 'vNeg':
                self.vgreenCycle[i] = 'green'

        self.vyellowCycle = ['red' for i in range(len(self.lights))]
        for i in range(len(self.lights)):
            if self.lights[i][1] == 'vPos' or self.lights[i][1] == 'vNeg':
                self.vyellowCycle[i] = 'yellow'

        self.hleftgreenCycle = ['red' for i in range(len(self.lights))]
        for i in range(len(self.lights)):
            if self.lights[i][1] == 'hPosLeft' or self.lights[i][1] == 'hNegLeft':
                self.hleftgreenCycle[i] = 'green'

        self.hleftyellowCycle = ['red' for i in range(len(self.lights))]
        for i in range(len(self.lights)):
            if self.lights[i][1] == 'hPosLeft' or self.lights[i][1] == 'hNegLeft':
                self.hleftyellowCycle[i] = 'yellow'

        self.vleftgreenCycle = ['red' for i in range(len(self.lights))]
        for i in range(len(self.lights)):
            if self.lights[i][1] == 'vPosLeft' or self.lights[i][1] == 'vNegLeft':
                self.vleftgreenCycle[i] = 'green'

        self.vleftyellowCycle = ['red' for i in range(len(self.lights))]
        for i in range(len(self.lights)):
            if self.lights[i][1] == 'vPosLeft' or self.lights[i][1] == 'vNegLeft':
                self.vleftyellowCycle[i] = 'yellow'


        #The overall traffic cycle. Format is [light config, time in seconds since start of overall traffic cycle]. Make sure the last light config is the same as the first one.
        self.trafficFlow = [[self.hgreenCycle, 0],
                               [self.hyellowCycle, self.hg],
                                   [self.redCycle, self.hg+self.hy],
                            [self.hleftgreenCycle, self.hg+self.hy+self.hr],
                           [self.hleftyellowCycle, self.hg+self.hy+self.hr+self.hlg],
                                   [self.redCycle, self.hg+self.hy+self.hr+self.hlg+self.hly],
                                [self.vgreenCycle, self.hg+self.hy+self.hr+self.hlg+self.hly+self.hlr],
                               [self.vyellowCycle, self.hg+self.hy+self.hr+self.hlg+self.hly+self.hlr+self.vg],
                                   [self.redCycle, self.hg+self.hy+self.hr+self.hlg+self.hly+self.hlr+self.vg+self.vy],
                            [self.vleftgreenCycle, self.hg+self.hy+self.hr+self.hlg+self.hly+self.hlr+self.vg+self.vy+self.vr],
                           [self.vleftyellowCycle, self.hg+self.hy+self.hr+self.hlg+self.hly+self.hlr+self.vg+self.vy+self.vr+self.vlg],
                                   [self.redCycle, self.hg+self.hy+self.hr+self.hlg+self.hly+self.hlr+self.vg+self.vy+self.vr+self.vlg+self.vly],
                                [self.hgreenCycle, self.hg+self.hy+self.hr+self.hlg+self.hly+self.hlr+self.vg+self.vy+self.vr+self.vlg+self.vly+self.vlr]]

        self.totalCycleLength = self.trafficFlow[len(self.trafficFlow) - 1][1]*constants.SECOND
        self.cycleNumber = 0

    def abruptChangeCycle(self):
        self.changeToCycle(self.trafficFlow[self.cycleNumber][0])
        newTime = self.trafficFlow[self.cycleNumber][1] * constants.SECOND
        if self.cycleNumber == len(self.trafficFlow) - 1:
            self.cycleNumber = 0
            newTime = 0
        else:
            self.cycleNumber += 1
        return newTime

    def draw(self, surface):
        pygame.draw.rect(surface, self.lightColors["darkG"], self.rect)

    def changeToCycle(self, cycle):
        for i in range(len(self.lights)):
            self.lights[i][0].color = cycle[i]


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

    #Goes through the traffic flow configs
    def changeCycle(self, time):
        if time == 0:
            self.cycleNumber = 0
        if time == self.trafficFlow[self.cycleNumber][1] * constants.SECOND:
            #print(self.trafficFlow[self.cycleNumber][0])
            self.changeToCycle(self.trafficFlow[self.cycleNumber][0])
            if self.cycleNumber < len(self.trafficFlow) - 1:
                self.cycleNumber += 1

