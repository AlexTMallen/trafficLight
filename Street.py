import pygame
from Lane import Lane


class Street:

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
                yPos = point1[1] + self.width // 2 - (laneNum * Lane.WIDTH + Lane.WIDTH // 2)
                self.lanesPos.append(
                    Lane(
                        (point1[0], yPos),
                        (point2[0], yPos)
                    )
                )
            for laneNum in range(numLeftOnly):
                yPos = point1[1] + self.width // 2 - ((numPos + laneNum) * Lane.WIDTH + Lane.WIDTH // 2)
                self.lanesPosLeft.append(
                    Lane(
                        (point1[0], yPos),
                        (self.intersectionMidpoint, yPos)
                    )
                )
                self.lanesNegLeft.append(
                    Lane(
                        (point2[0], yPos),
                        (self.intersectionMidpoint, yPos)
                    )
                )
            for laneNum in range(numNeg):
                yPos = point1[1] - self.width // 2 + laneNum * Lane.WIDTH + Lane.WIDTH // 2
                self.lanesNeg.append(
                    Lane(
                        (point2[0], yPos),
                        (point1[0], yPos)
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
                        (xPos, point2[1])
                    )
                )
            # building the left only lanes from left to right
            for laneNum in range(numLeftOnly):
                xPos = point1[0] - self.width // 2 + (numPos + laneNum) * Lane.WIDTH + Lane.WIDTH // 2
                self.lanesPosLeft.append(
                    Lane(
                        (xPos, point1[1]),
                        (xPos, self.intersectionMidpoint)
                    )
                )
                self.lanesNegLeft.append(
                    Lane(
                        (xPos, point2[1]),
                        (xPos, self.intersectionMidpoint)
                    )
                )
            # building up lanes from right inwards
            for laneNum in range(numNeg):
                xPos = self.point1[0] + self.width // 2 - (laneNum * Lane.WIDTH + Lane.WIDTH // 2)
                self.lanesNeg.append(
                    Lane(
                        (xPos, point2[1]),
                        (xPos, point1[1])
                    )
                )

        self.lanes = self.lanesNeg + self.lanesNegLeft + self.lanesPosLeft + self.lanesPos