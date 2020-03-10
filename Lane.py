import pygame
import json

class Lane:
    WIDTH = 30;
    def __init__(self, start, end):
        self.start = start
        if start[0] == end[0]:
            self.rect = pygame.Rect(start[0] - self.WIDTH // 2, min(start[1], end[1]), self.WIDTH, abs(end[1] - start[1]))
            self.direction = (0, (end[1] - start[1]) // abs(end[1] - start[1]))
        else:
            self.rect = pygame.Rect(min(start[0], end[0]), start[1] - self.WIDTH // 2, abs(end[0] - start[0]), self.WIDTH)
            self.direction = ((end[0] - start[0]) // abs(end[0] - start[0]), 0)

        with open("colors.json") as f:
            self.colors = json.loads(f.read())

        self.stopPoints = []

    def draw(self, surface):
        pygame.draw.rect(surface, self.colors["lightG"], self.rect)