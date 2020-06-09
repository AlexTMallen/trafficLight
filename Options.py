import pygame
import json

class Options:

    def __init__(self, hposLanes, hnegLanes, hleftLanes, vposLanes, vnegLanes, vleftLanes, carDensity, simSpeed):


        self.index = [str(hposLanes), str(hnegLanes), str(hleftLanes), str(vposLanes), str(vnegLanes),
                          str(vleftLanes), str(carDensity), str(simSpeed)]

        self.inputBoxes = []

        self.left_column_x = 80
        self.left_column_y = 200
        self.right_column_x = 450
        self.right_column_y = 200
        self.spacing = 80
        for i in range(6):
            self.inputBoxes.append(pygame.Rect(self.left_column_x + 185, self.left_column_y - 10 + 80 * i, 40, 50))

        for i in range(2):
            self.inputBoxes.append(pygame.Rect(self.right_column_x + 192, self.right_column_y - 15 + 80 * i, 40, 50))


        self.typing = False
        self.currentBox = self.inputBoxes[0]
        self.currentIndex = self.inputBoxes.index(self.currentBox)


        with open("colors.json") as f:
            self.colors = json.loads(f.read())


    def draw(self, surface):
        surface.fill(self.colors["white"])

        if self.typing:
            pygame.draw.rect(surface, self.colors["lightG"], self.currentBox)

        self.text(surface, "Options", 20, 40, 44)
        self.text(surface, "Lane Counts", self.left_column_x - 10, 120, 34)
        self.text(surface, "Simulation Settings", self.right_column_x - 20, 120, 34)

        self.text(surface, "Right: ", self.left_column_x, self.left_column_y, 20)
        self.text(surface, "Left:  ", self.left_column_x, self.left_column_y + self.spacing, 20)
        self.text(surface, "Horizontal Turn: ", self.left_column_x, self.left_column_y + self.spacing * 2, 20)
        self.text(surface, "Down:  ", self.left_column_x, self.left_column_y + self.spacing * 3, 20)
        self.text(surface, "Up:    ", self.left_column_x, self.left_column_y + self.spacing * 4, 20)
        self.text(surface, "Vertical Turn: ", self.left_column_x, self.left_column_y + self.spacing * 5, 20)

        self.text(surface, "Car Density:", self.right_column_x, self.right_column_y, 20)
        self.text(surface, "Simulation Speed:", self.right_column_x, self.right_column_y + self.spacing, 20)


        for i in range(6):
            self.text(surface, str(self.index[i]), self.left_column_x + 200, self.left_column_y + 80 * i, 20)

        for i in range(6,8):
            self.text(surface, str(self.index[i]), self.right_column_x + 200, self.right_column_y + 80 * (i-6), 20)




    def text(self, surface, message, x, y, textsize):
        font = pygame.font.Font(pygame.font.get_default_font(), textsize)
        text_surface = font.render(message, True, self.colors["black"])
        surface.blit(text_surface, dest=(x, y))
