import pygame
import config


class Car:

    WIDTH = int(2*config.METER)
    LENGTH = int(3.5*config.METER)
    FOLLOWING_TIME = 3*config.SECOND
    BUFFER_DISTANCE = 1*config.METER

    def __init__(self, color, lane, intersection, desiredSpeed=1):
        self.color = color
        self.hitBoxColor = (0, 0, 255, 10)
        self.lane = lane
        self.distance = 0
        self.desiredSpeed = desiredSpeed
        self.speed = 1
        self.rect = None
        self.hitBox = None
        self.inIntersection = False
        self.intersection = intersection
        self.addedSelfToIntersection = False
        self.removedSelfFromIntersection = False
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
                # print("Stopped" + "\n" * 5)
            self.inIntersection = True
        else:
            self.inIntersection = False
        if self.speed < self.desiredSpeed:
            # if (the light you've been waiting on is now green)
            #       or (you're not in an intersection and there's no car in front of you (aka collides only with self))
            if (self.lane.light.color == "green" and self.inIntersection and self.intersection.carsInIntersection == 0) \
                    or ((not self.inIntersection or self.rect.colliderect(self.intersection)) and len(self.hitBox.collidelistall(carRects)) == 1):
                self.speed += min((self.desiredSpeed - self.speed) / 2, 3*config.METER/(config.SECOND**2))
        self.distance += self.speed
        self.updateRect()
        # print("Rect", self.rect)
        # print(self.hitBox)

    def draw(self, surface, showHitbox=True):
        if showHitbox:
            pygame.draw.rect(surface, self.hitBoxColor, self.hitBox)
        pygame.draw.rect(surface, self.color, self.rect)

    def updateRect(self):
        if self.lane.direction[0] == 0:  # If vertical lane
            self.rect = pygame.Rect(
                self.lane.start[0] - self.WIDTH // 2,
                self.lane.start[1] - self.LENGTH * self.lane.direction[1] + self.distance * self.lane.direction[1],
                self.WIDTH,
                self.LENGTH
            )
            if self.lane.direction[1] == 1:  # If down
                self.hitBox = pygame.Rect(
                    self.lane.start[0] - self.WIDTH // 2,
                    self.lane.start[1] - self.LENGTH * self.lane.direction[1] + self.distance * self.lane.direction[1],
                    self.WIDTH,
                    self.LENGTH + self.FOLLOWING_TIME * self.speed + self.BUFFER_DISTANCE
                )
            else:  # If up
                self.hitBox = pygame.Rect(
                    self.lane.start[0] - self.WIDTH // 2,
                    self.lane.start[1] - self.LENGTH * self.lane.direction[1] + self.distance * self.lane.direction[1] - self.FOLLOWING_TIME * self.speed - self.BUFFER_DISTANCE,
                    self.WIDTH,
                    self.LENGTH + self.FOLLOWING_TIME * self.speed + self.BUFFER_DISTANCE
                )
        else:  # If horizontal (not vertical)
            self.rect = pygame.Rect(
                self.lane.start[0] - self.LENGTH * self.lane.direction[0] + self.distance * self.lane.direction[0],
                self.lane.start[1] - self.WIDTH // 2,
                self.LENGTH,
                self.WIDTH
            )
            if self.lane.direction[0] == 1:  # If right
                self.hitBox = pygame.Rect(
                    self.lane.start[0] - self.LENGTH * self.lane.direction[0] + self.distance * self.lane.direction[0],
                    self.lane.start[1] - self.WIDTH // 2,
                    self.LENGTH + self.FOLLOWING_TIME * self.speed + self.BUFFER_DISTANCE,
                    self.WIDTH
                )
            else:  # If left
                self.hitBox = pygame.Rect(
                    self.lane.start[0] - self.LENGTH * self.lane.direction[0] + self.distance * self.lane.direction[0] - self.FOLLOWING_TIME * self.speed - self.BUFFER_DISTANCE,
                    self.lane.start[1] - self.WIDTH // 2,
                    self.LENGTH + self.FOLLOWING_TIME * self.speed + self.BUFFER_DISTANCE,
                    self.WIDTH
                )

