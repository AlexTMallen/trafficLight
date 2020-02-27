import pygame
import Lane

class Street:

    def __init__(self, point1, point2, numPos, numNeg):
        self.numLanes = numPos + numNeg
        self.numNeg = numNeg
        self.numPos = numPos
        for lane in range(numPos)