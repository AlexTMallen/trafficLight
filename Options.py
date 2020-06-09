import pygame
import json

class Options:

    def __init__(self, hposLanes, hnegLanes, hleftLanes, vposLanes, vnegLanes, vleftLanes):
        self.hposLanes = str(hposLanes)
        self.hnegLanes = str(hnegLanes)
        self.hleftLanes = str(hleftLanes)
        self.vposLanes = str(vposLanes)
        self.vnegLanes = str(vnegLanes)
        self.vleftLanes = str(vleftLanes)


        self.hposBox = pygame.Rect(200,20,50,50)
        self.hnegBox = pygame.Rect(200, 100, 50, 50)
        self.hleftBox = pygame.Rect(200, 180, 50, 50)
        self.vposBox = pygame.Rect(200, 260, 50, 50)
        self.vnegBox = pygame.Rect(200, 340, 50, 50)
        self.vleftBox = pygame.Rect(200, 420, 50, 50)

        self.typing = False
        self.currentBox = self.hposBox
        self.typeBoxes = [self.hposBox, self.hnegBox, self.hleftBox, self.vposBox, self.vnegBox, self.vleftBox]
        self.laneIndex = [self.hposLanes, self.hnegLanes, self.hleftLanes, self.vposLanes, self.vnegLanes, self.vleftLanes]
        self.currentIndex = self.typeBoxes.index(self.currentBox)


        with open("colors.json") as f:
            self.colors = json.loads(f.read())


    def draw(self, surface):
        surface.fill(self.colors["white"])

        if self.typing:
            pygame.draw.rect(surface, self.colors["lightG"], self.currentBox)


        self.text(surface, "Right: ", 0, 20)
        self.text(surface, "Left:  ", 0, 100)
        self.text(surface, "HTurn: ", 0, 180)
        self.text(surface, "Down:  ", 0, 260)
        self.text(surface, "Up:    ", 0, 340)
        self.text(surface, "VTurn: ", 0, 420)

        self.text(surface, str(self.hposLanes), 200, 20)
        self.text(surface, str(self.hnegLanes), 200, 100)
        self.text(surface, str(self.hleftLanes), 200, 180)
        self.text(surface, str(self.vposLanes), 200, 260)
        self.text(surface, str(self.vnegLanes), 200, 340)
        self.text(surface, str(self.vleftLanes), 200, 420)





    def text(self, surface, message, x, y):
        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        text_surface = font.render(message, True, self.colors["black"])
        surface.blit(text_surface, dest=(x, y))
