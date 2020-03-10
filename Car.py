import pygame


class Car:
    WIDTH = 20
    LENGTH = 50
    FOLLOWING_TIME = 10

    def __init__(self, color, lane):
        self.color = color
        self.hitBoxColor = (0, 0, 255, 10)
        self.lane = lane
        self.distance = 0
        self.speed = 1
        self.rect = None
        self.hitBox = None
        self.updateRect()

    def draw(self, surface):
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
                    self.LENGTH + self.FOLLOWING_TIME * self.speed
                )
            else:  # If up
                self.hitBox = pygame.Rect(
                    self.lane.start[0] - self.WIDTH // 2,
                    self.lane.start[1] - self.LENGTH * self.lane.direction[1] + self.distance * self.lane.direction[1] - self.FOLLOWING_TIME * self.speed,
                    self.WIDTH,
                    self.LENGTH + self.FOLLOWING_TIME * self.speed
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
                    self.LENGTH + self.FOLLOWING_TIME * self.speed,
                    self.WIDTH
                )
            else:  # If left
                self.hitBox = pygame.Rect(
                    self.lane.start[0] - self.LENGTH * self.lane.direction[0] + self.distance * self.lane.direction[0] - self.FOLLOWING_TIME * self.speed,
                    self.lane.start[1] - self.WIDTH // 2,
                    self.LENGTH + self.FOLLOWING_TIME * self.speed,
                    self.WIDTH
                )

