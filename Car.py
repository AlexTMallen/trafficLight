import pygame


class Car:
    WIDTH = 20
    LENGTH = 50

    def __init__(self, color, lane):
        self.color = color
        self.lane = lane
        self.distance = 0
        self.updateRect()

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def updateRect(self):
        if self.lane.direction[0] == 0:
            self.rect = pygame.Rect(
                self.lane.start[0] - self.WIDTH // 2,
                self.lane.start[1] - self.LENGTH * self.lane.direction[1] + self.distance * self.lane.direction[1],
                self.WIDTH,
                self.LENGTH
            )
        else:
            self.rect = pygame.Rect(
                self.lane.start[0] - self.LENGTH * self.lane.direction[0] + self.distance * self.lane.direction[0],
                self.lane.start[1] - self.WIDTH // 2,
                self.LENGTH,
                self.WIDTH
            )

