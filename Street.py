import pygame
from Lane import Lane

class Street:

    def __init__(self, point1, point2, numPos, numNeg):
        # Streets should always list in increasing order (left to right or up to down)
        self.numLanes = numPos + numNeg
        self.numNeg = numNeg
        self.numPos = numPos
        self.point1 = point1
        self.point2 = point2
        self.lanesPos = []
        self.lanesNeg = []
        if point1[0] == point2[0]:
            self.direction = (0, (point2[1] - point1[1]) // abs(point2[1] - point1[1]))
        else:
            self.direction = ((point2[0] - point1[0]) // abs(point2[0] - point1[0]), 0)



        if point1[1] == point2[1]:
            for laneNum in range(numPos):
                self.lanesPos.append(
                    Lane(
                        (point1[0], point1[1] + laneNum * Lane.WIDTH + Lane.WIDTH // 2),
                        (point2[0], point1[1] + laneNum * Lane.WIDTH + Lane.WIDTH // 2)
                    )
                )
            for laneNum in range(numNeg):
                self.lanesNeg.append(
                    Lane(
                        (point2[0], point1[1] - laneNum * Lane.WIDTH - Lane.WIDTH // 2),
                        (point1[0], point1[1] - laneNum * Lane.WIDTH - Lane.WIDTH // 2)
                    )
                )

        else:
            for laneNum in range(numPos):
                self.lanesPos.append(
                    Lane(
                        (point1[0] - laneNum * Lane.WIDTH - Lane.WIDTH // 2, point1[1]),
                        (point1[1] - laneNum * Lane.WIDTH - Lane.WIDTH // 2, point2[1])
                    )
                )
            for laneNum in range(numNeg):
                self.lanesNeg.append(
                    Lane(
                        (point1[1] + laneNum * Lane.WIDTH + Lane.WIDTH // 2, point2[1]),
                        (point1[1] + laneNum * Lane.WIDTH + Lane.WIDTH // 2, point1[2])
                    )
                )
