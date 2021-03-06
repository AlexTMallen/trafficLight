import pygame
import json

class Options:
    COLORS = {
        "red": [255, 0, 0],
        "green": [0, 255, 0],
        "yellow": [255, 255, 0],
        "white": [255, 255, 255],
        "black": [0, 0, 0],
        "lightG": [200, 200, 200],
        "darkG": [100, 100, 100]
    }

    def __init__(self, hposLanes, hnegLanes, hleftLanes, vposLanes, vnegLanes, vleftLanes, carDensity, simSpeed, vProb, isAlgorithm):

        self.index = list(map(str, [hposLanes, hnegLanes, hleftLanes, vposLanes, vnegLanes, vleftLanes, carDensity, simSpeed, vProb, isAlgorithm]))

        self.inputBoxes = []

        self.left_column_x = 80
        self.left_column_y = 200
        self.right_column_x = 450
        self.right_column_y = 200
        self.spacing = 40
        for i in range(6):
            self.inputBoxes.append(pygame.Rect(self.left_column_x + 190, self.left_column_y - 10 + self.spacing * i, 35, 40))

        for i in range(4):
            self.inputBoxes.append(pygame.Rect(self.right_column_x + 195, self.right_column_y - 10 + self.spacing * i, 40, 40))


        self.typing = False
        self.currentBox = self.inputBoxes[0]
        self.currentIndex = self.inputBoxes.index(self.currentBox)



    def draw(self, surface):
        surface.fill(Options.COLORS["white"])

        if self.typing:
            pygame.draw.rect(surface, Options.COLORS["lightG"], self.currentBox)

        Options.text(surface, "Options", 20, 40, 44)
        Options.text(surface, "Lane Counts", self.left_column_x - 10, 120, 34)
        Options.text(surface, "Simulation Settings", self.right_column_x - 20, 120, 34)

        Options.text(surface, "R to Apply Changes", 500, 500, 26)

        Options.text(surface, "# Rightward Lanes: ", self.left_column_x, self.left_column_y, 20)
        Options.text(surface, "# Leftward Lanes:  ", self.left_column_x, self.left_column_y + self.spacing, 20)
        Options.text(surface, "# Horz. Left Turn: ", self.left_column_x, self.left_column_y + self.spacing * 2, 20)
        Options.text(surface, "# Downward Lanes:  ", self.left_column_x, self.left_column_y + self.spacing * 3, 20)
        Options.text(surface, "# Upward Lanes:    ", self.left_column_x, self.left_column_y + self.spacing * 4, 20)
        Options.text(surface, "# Vert. Left Turn: ", self.left_column_x, self.left_column_y + self.spacing * 5, 20)

        Options.text(surface, "Car Density:", self.right_column_x, self.right_column_y, 20)
        Options.text(surface, "Simulation Speed:", self.right_column_x, self.right_column_y + self.spacing, 20)
        Options.text(surface, "Vrt. Rel. Density:", self.right_column_x, self.right_column_y + self.spacing * 2, 20)
        Options.text(surface, "Light Algorithm:", self.right_column_x, self.right_column_y + self.spacing * 3, 20)



        for i in range(6):
            Options.text(surface, str(self.index[i]), self.left_column_x + 200, self.left_column_y + self.spacing * i, 20)

        for i in range(6, len(self.index)):
            Options.text(surface, str(self.index[i]), self.right_column_x + 200, self.right_column_y + self.spacing * (i-6), 20)

    @staticmethod
    def text(surface, message, x, y, textsize):
        font = pygame.font.Font(pygame.font.get_default_font(), textsize)
        text_surface = font.render(message, True, Options.COLORS["black"])
        surface.blit(text_surface, dest=(x, y))
