import pygame
from numpy import random

from Lane import Lane

class Car:
    WIDTH = 12
    LENGTH = 25
    FOLLOWING_TIME = 20
    BUFFER_DISTANCE = 10
    DIRECTIONS = {
        (1, 0): "Right",
        (-1, 0): "Left",
        (0, 1): "Down",
        (0, -1): "Up"
    }
    COLORS = ("Blue", "Yellow", "Green", "Red", "Gray", "White")

    def __init__(self, lane, intersection, color, desiredSpeed=1):
        self.color = color
        self.hitBoxColor = (0, 0, 255, 10)
        self.lane = lane
        self.distance = 0
        self.desiredSpeed = desiredSpeed
        self.speed = 1
        if color in Car.COLORS:
            self.color = color
        else:
            raise ValueError('Color must be one of {"Blue", "Yellow", "Green", "Red", "Gray", "White"}')
        self.rect = None
        self.hitBox = None
        self.inIntersection = False
        self.intersection = intersection
        self.addedSelfToIntersection = False
        self.removedSelfFromIntersection = False
        self.image = pygame.image.load(self.color + "Car" + Car.DIRECTIONS[self.lane.direction] + ".png")

        # for turning left
        self.isTurningLeft = False
        self.targetLane = None
        self.targetLaneDist = 0
        self.initiateDist = 0
        self.leftOffset = 0

        # for turning right
        self.isTurningRight = False

        self.updateRect()

    def move(self, carRects):

        if self.rect.colliderect(self.intersection):
            if not self.addedSelfToIntersection:
                self.intersection.carsInIntersection += 1
                self.addedSelfToIntersection = True
        else:
            if not self.removedSelfFromIntersection and self.addedSelfToIntersection:
                self.intersection.carsInIntersection -= 1
                self.removedSelfFromIntersection = True

        if self.hitBox.colliderect(self.intersection):
            if self.lane.light.color == "red" and not self.inIntersection:
                self.speed = 0
                # print("Stopped"    + "\n" * 5)

            # if the care just entered the intersection and it can turn right maybe turn right
            if not self.inIntersection and self.lane.type == "straightORright" and random.randint(3) == 0:
                self.isTurningRight = True
                if self.lane.direction[0] == 0:  # if car is on a vertical lane
                    otherStreet = self.intersection.streetH
                    dir = self.lane.direction[1]
                    self.targetLane = otherStreet.lanesNeg[0] if dir == 1 else otherStreet.lanesPos[-1]
                    self.targetLaneDist = (self.targetLane.start[1] - self.lane.start[1]) * dir

                else:
                    otherStreet = self.intersection.streetV
                    dir = self.lane.direction[0]
                    self.targetLane = otherStreet.lanesNeg[0] if dir == -1 else otherStreet.lanesPos[0]
                    self.targetLaneDist = (self.targetLane.start[0] - self.lane.start[0]) * dir

            # if the car just entered the intersection and it's going to turn left, figure out where to turn
            if not self.inIntersection and self.lane.type == "left":
                self.isTurningLeft = True
                if self.lane.direction[0] == 0:  # if car is on a vertical lane
                    otherStreet = self.intersection.streetH
                    dir = self.lane.direction[1]
                    n = self.intersection.streetV.numLeftOnly \
                        - (self.intersection.streetV.lanesPosLeft.index(self.lane) if dir == 1
                           else self.intersection.streetV.lanesNegLeft.index(self.lane))
                    self.targetLane = otherStreet.lanesNeg[-n] if dir == -1 else otherStreet.lanesPos[0]

                    self.targetLaneDist = (self.targetLane.start[1] - self.lane.start[1]) * dir
                else:
                    otherStreet = self.intersection.streetV
                    dir = self.lane.direction[0]
                    n = self.intersection.streetH.numLeftOnly \
                        - (self.intersection.streetH.lanesPosLeft.laneIndex(self.lane) if dir == 1
                           else self.intersection.streetH.lanesNegLeft.index(self.lane))
                    self.targetLane = otherStreet.lanesNeg[-n] if dir == 1 else otherStreet.lanesPos[-n]
                    self.targetLaneDist = (self.targetLane.start[0] - self.lane.start[0]) * dir
                # when the car's distance (front of car) is self.initiateDist, it will start turning
                self.initiateDist = self.targetLaneDist - 2.3 * Lane.WIDTH + (Lane.WIDTH - Car.WIDTH // 2)

            self.inIntersection = True
        else:
            self.inIntersection = False
        if self.speed < self.desiredSpeed:
            # if (the light you've been waiting on is now green and the intersection is clear)
            #       or (you're not in an intersection and there's no car in front of you (aka collides only with self))
            if (self.lane.light.color == "green" and self.inIntersection and self.intersection.carsInIntersection == 0)\
                    or ((not self.inIntersection or self.rect.colliderect(self.intersection)) and len(self.hitBox.collidelistall(carRects)) == 1):
                self.speed = (self.desiredSpeed + self.speed) / 2

        if self.isTurningLeft and self.distance >= self.targetLaneDist:
            if self.lane.direction[0] == 1:  # if current car's lane is right
                self.distance = self.targetLane.start[1] - self.rect.y
            if self.lane.direction[0] == -1:  # if current car's lane is left
                self.distance = self.rect.y - self.targetLane.start[1]
            if self.lane.direction[1] == 1:  # if current car's lane is down
                self.distance = self.rect.x - self.targetLane.start[0]
            if self.lane.direction[1] == -1:  # if current car's lane is up
                self.distance = self.targetLane.start[0] - self.rect.x
            self.distance += Car.LENGTH * 0.75
            self.lane = self.targetLane
            self.image = pygame.image.load(self.color + "Car" + Car.DIRECTIONS[self.lane.direction] + ".png")
            self.isTurningLeft = False
            self.leftOffset = 0
            self.targetLane = None
            self.initiateDist = 0
            self.targetLaneDist = 0

        if self.isTurningRight and self.distance >= self.targetLaneDist:
            if self.lane.direction[0] == 1:  # if current car's lane is right
                self.distance = self.rect.y - self.targetLane.start[1]
            if self.lane.direction[0] == -1:  # if current car's lane is left
                self.distance = self.targetLane.start[1] - self.rect.y
            if self.lane.direction[1] == 1:  # if current car's lane is down
                self.distance = self.targetLane.start[0] - self.rect.x
            if self.lane.direction[1] == -1:  # if current car's lane is up
                self.distance = self.rect.x - self.targetLane.start[0]
            self.distance += Car.LENGTH * 0.75
            self.lane = self.targetLane
            self.image = pygame.image.load(self.color + "Car" + Car.DIRECTIONS[self.lane.direction] + ".png")
            self.targetLane = None
            self.targetLaneDist = 0
            self.isTurningRight = False

        if self.isTurningLeft and self.distance >= self.initiateDist:
            self.leftOffset += self.speed
            self.distance += self.speed
        else:
            self.distance += self.speed
        self.updateRect()

    def draw(self, surface, showHitbox=True):
        if showHitbox:
            pygame.draw.rect(surface, self.hitBoxColor, self.hitBox)
        # pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def updateRect(self):
        if self.lane.direction[0] == 0:  # If vertical lane
            self.rect = pygame.Rect(
                self.lane.start[0] - self.WIDTH // 2 + self.leftOffset * self.lane.direction[1],
                self.lane.start[1] - self.LENGTH * (self.lane.direction[1]/2 + 0.5) + self.distance * self.lane.direction[1],
                self.WIDTH,
                self.LENGTH
            )
            if self.lane.direction[1] == 1:  # If down
                self.hitBox = pygame.Rect(
                    self.lane.start[0] - self.WIDTH // 2 + self.leftOffset,
                    self.lane.start[1] - self.LENGTH * self.lane.direction[1] + self.distance * self.lane.direction[1],
                    self.WIDTH,
                    self.LENGTH + self.FOLLOWING_TIME * self.speed + self.BUFFER_DISTANCE
                )
            else:  # If up
                self.hitBox = pygame.Rect(
                    self.lane.start[0] - self.WIDTH // 2 - self.leftOffset,
                    self.lane.start[1] + self.distance * self.lane.direction[1] - self.FOLLOWING_TIME * self.speed - self.BUFFER_DISTANCE,
                    self.WIDTH,
                    self.LENGTH + self.FOLLOWING_TIME * self.speed + self.BUFFER_DISTANCE
                )
        else:  # If horizontal (not vertical)
            self.rect = pygame.Rect(
                self.lane.start[0] - self.LENGTH * (self.lane.direction[0]/2 + 0.5) + self.distance * self.lane.direction[0],
                self.lane.start[1] - self.WIDTH // 2 - self.leftOffset * self.lane.direction[0],
                self.LENGTH,
                self.WIDTH
            )
            if self.lane.direction[0] == 1:  # If right
                self.hitBox = pygame.Rect(
                    self.lane.start[0] - self.LENGTH * self.lane.direction[0] + self.distance * self.lane.direction[0],
                    self.lane.start[1] - self.WIDTH // 2 - self.leftOffset,
                    self.LENGTH + self.FOLLOWING_TIME * self.speed + self.BUFFER_DISTANCE,
                    self.WIDTH
                )
            else:  # If left
                self.hitBox = pygame.Rect(
                    self.lane.start[0] + self.distance * self.lane.direction[0] - self.FOLLOWING_TIME * self.speed - self.BUFFER_DISTANCE,
                    self.lane.start[1] - self.WIDTH // 2 + self.leftOffset,
                    self.LENGTH + self.FOLLOWING_TIME * self.speed + self.BUFFER_DISTANCE,
                    self.WIDTH
                )

