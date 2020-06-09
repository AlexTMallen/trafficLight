import pygame
import numpy as np
from Lane import Lane


class Street:
    COLORS = {
      "red": [255, 0, 0],
      "green": [0, 255, 0],
      "yellow": [255, 255, 0],
      "white": [255, 255, 255],
      "black": [0, 0, 0],
      "lightG": [200, 200, 200],
      "darkG": [100, 100, 100]
    }

    def __init__(self, point1, point2, numPos, numNeg, numLeftOnly, intersectionMidpoint):
        """
        :param point1: center of starting point
        :param point2: center of ending point (must be in positive direction of start--ie. left to right or up to down)
        :param numPos: number of lanes traveling in the positive direction
        :param numNeg: ""
        :param numLeftOnly: num left turn only lanes. assumes same number in both directions. TODO: make more versatile
        :param intersectionMidpoint: distance along the street at which the intersection is centered (defining center
        as the spatial midpoint--halfway along the street)
        """
        self.numLanes = numPos + numNeg + numLeftOnly
        self.numNeg = numNeg
        self.numPos = numPos
        self.numLeftOnly = numLeftOnly
        self.point1 = point1
        self.point2 = point2
        self.lanesPosLeft = []
        self.lanesNegLeft = []
        self.lanesPos = []
        self.lanesNeg = []
        self.intersectionMidpoint = intersectionMidpoint
        self.width = Lane.WIDTH * self.numLanes

        # if vertical then the direction is (0, +/-1)
        if point1[0] == point2[0]:
            self.direction = (0, (point2[1] - point1[1]) // abs(point2[1] - point1[1]))
        # if horizontal then the direction is (+/-1, 0)
        else:
            self.direction = ((point2[0] - point1[0]) // abs(point2[0] - point1[0]), 0)

        # making the lanes in the horizontal case
        if point1[1] == point2[1]:
            for laneNum in range(numPos):
                # build lanes from middle outward
                yPos = point1[1] + self.width // 2 - (laneNum * Lane.WIDTH + Lane.WIDTH // 2)
                self.lanesPos.append(
                    Lane(
                        (point1[0], yPos),
                        (point2[0], yPos),
                        type="straightORright" if laneNum == 0 else "normal"
                    )
                )
            # TODO: this may have been a hacky fix
            self.lanesPos = self.lanesPos[::-1]
            for laneNum in range(numLeftOnly):
                yPos = point1[1] + self.width // 2 - ((numPos + laneNum) * Lane.WIDTH + Lane.WIDTH // 2)
                self.lanesPosLeft.append(
                    Lane(
                        (point1[0], yPos),
                        (self.intersectionMidpoint, yPos),
                        type="left"
                    )
                )
                self.lanesNegLeft.append(
                    Lane(
                        (point2[0], yPos),
                        (self.intersectionMidpoint, yPos),
                        "left"
                    )
                )
            for laneNum in range(numNeg):
                yPos = point1[1] - self.width // 2 + laneNum * Lane.WIDTH + Lane.WIDTH // 2

                self.lanesNeg.append(
                    Lane(
                        (point2[0], yPos),
                        (point1[0], yPos),
                        type="straightORright" if laneNum == 0 else "normal"
                    )
                )

        # vertical lanes
        else:
            # building the down lanes from the left inward
            for laneNum in range(numPos):
                xPos = point1[0] - self.width // 2 + laneNum * Lane.WIDTH + Lane.WIDTH // 2

                self.lanesPos.append(
                    Lane(
                        (xPos, point1[1]),
                        (xPos, point2[1]),
                        type="straightORright" if laneNum == 0 else "normal"
                    )
                )
            # building the left only lanes from left to right
            for laneNum in range(numLeftOnly):
                xPos = point1[0] - self.width // 2 + (numPos + laneNum) * Lane.WIDTH + Lane.WIDTH // 2
                self.lanesPosLeft.append(
                    Lane(
                        (xPos, point1[1]),
                        (xPos, self.intersectionMidpoint),
                        type="left"
                    )
                )
                self.lanesNegLeft.append(
                    Lane(
                        (xPos, point2[1]),
                        (xPos, self.intersectionMidpoint),
                        type="left"
                    )
                )
            # building up lanes from right inwards
            for laneNum in range(numNeg):
                xPos = self.point1[0] + self.width // 2 - (laneNum * Lane.WIDTH + Lane.WIDTH // 2)
                self.lanesNeg.append(
                    Lane(
                        (xPos, point2[1]),
                        (xPos, point1[1]),
                        type="straightORright" if laneNum == 0 else "normal"
                    )
                )

        self.lanes = self.lanesNeg + self.lanesNegLeft + self.lanesPosLeft + self.lanesPos

    def drawLines(self, surface):
        # TODO: doesn't work with multiple left turn only lanes
        if self.direction[0] == 0:  # if vertical
            for i, lane in enumerate(self.lanes[::-1][:-1]):
                self._drawDashedLine(surface, lane.rect.y, lane.rect.y + lane.rect.height,
                                     lane.rect.x + lane.rect.width, "v", Street.COLORS["white"])
                if lane in self.lanesNegLeft:
                    self._drawDashedLine(surface, lane.rect.y, lane.rect.y + lane.rect.height,
                                         lane.rect.x, "v", Street.COLORS["yellow"])
                if lane in self.lanesPosLeft:
                    self._drawDashedLine(surface, lane.rect.y, lane.rect.y + lane.rect.height,
                                         lane.rect.x + lane.rect.width, "v", Street.COLORS["yellow"])
                if self.numLeftOnly == 0 and i == self.numPos - 1:
                    self._drawDashedLine(surface, lane.rect.y, lane.rect.y + lane.rect.height,
                                         lane.rect.x + lane.rect.width, "v", Street.COLORS["yellow"])
        else:
            for i, lane in enumerate(self.lanes[:-1]):
                # self._drawDashedLine(surface, lane.rect.x, lane.rect.x + lane.rect.width,
                #                      lane.rect.y + lane.rect.height, "h", Street.COLORS["white"])
                self._drawDashedLine(surface, lane.rect.x, lane.rect.x + lane.rect.width,
                                     lane.rect.y + lane.rect.height, "h", Street.COLORS["white"])
                if lane in self.lanesNegLeft:
                    self._drawDashedLine(surface, lane.rect.x, lane.rect.x + lane.rect.width,
                                         lane.rect.y + lane.rect.height, "h", Street.COLORS["yellow"])
                if lane in self.lanesPosLeft:
                    self._drawDashedLine(surface, lane.rect.x, lane.rect.x + lane.rect.width,
                                         lane.rect.y, "h", Street.COLORS["yellow"])
                if self.numLeftOnly == 0 and i == self.numPos - 1:
                    self._drawDashedLine(surface, lane.rect.x, lane.rect.x + lane.rect.width,
                                         lane.rect.y + lane.rect.height, "h", Street.COLORS["yellow"])

    def _drawDashedLine(self, surface, start, end, otherCoord, dir, color):
        """
        :param start: int coordinate of start
        :param end: int coordinate of end
        :param dir: horizontal ("h") or vertical ("v")
        :param otherCoord: the x coord of the line if vertical, or the y coord if horizontal
        :param color: color
        :return: None
        """
        points = np.arange(start, end, 20)
        for i, point in enumerate(points[:-1]):
            if i % 2 == 0:
                if dir == "h":
                    pygame.draw.line(surface, color, (points[i+1], otherCoord), (point, otherCoord), 2)
                else:
                    pygame.draw.line(surface, color, (otherCoord, points[i+1]), (otherCoord, point), 2)
