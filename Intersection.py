import pygame
from Street import Street
from Lane import Lane
from Light import Light

class Intersection:
#spawned automatically by main which does the math to find out where the streets intersect
#streets encompass all the lanes going into an intersection so there will always be TWO streets (horiz and vert)
    def __init__ (self,streetH,streetV): #topLeft and bottomRIght are already given as the intersection corners
        #lists holding all lights opposite a lane of that direction
        self.lightup = []
        self.lightdown = []
        self.lightleft = []
        self.lightright = []
        #spawn lights for horizontal street
        for current in self.streetH.lanesPos:
            self.lightright.append(Light(current,self))
        for current in self.streetH.lanesNeg:
            self.lightright.append(Light(current,self))
        for current in self.streetV.lanesPos:
            self.lightright.append(Light(current,self))
        for current in self.streetV.laneNeg:
            self.lightright.append(Light(current,self))
        #calculate coordinates of intersect
        self.x = streetV.point1[0] - streetV.lanesPos.length * Lane.WIDTH
        self.y = streetH.point1[1] - streetH.lanesNeg.length * Lane.WIDTH
        wide = (streetV.lanesPos.length + streetV.laneNeg.length) * Lane.WIDTH
        long = (streetH.lanesPos.length + streetH.laneNeg.length) * Lane.WIDTH
        self.rect = pygame.Rect(x, y, wide,long)

    def draw(self, surface):
        pygame.draw.fill(surface, colors["darkG"], self.rect)
