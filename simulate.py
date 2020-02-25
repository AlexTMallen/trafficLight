import pygame
import json
from Lane import Lane

def main():
    # setup
    with open("colors.json") as f:
        text = f.read()
        colors = json.loads(text)

    width = 800
    height = 800
    w = pygame.display.set_mode((width, height))
    w.fill(colors["green"])
    laneLeft = Lane(pygame.Rect(0, 200, width, height // 5), 1)
    laneRight = Lane(pygame.Rect(0, 250, width, height // 5), 1)
    laneDown = Lane(pygame.Rect(200, 0, width // 5, height), 1)
    laneUp = Lane(pygame.Rect(250, 0, width // 5, height), 1)
    laneLeft.draw(w)
    laneRight.draw(w)
    laneDown.draw(w)
    laneUp.draw(w)

    waitTime = 10
    running = True

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
        pygame.display.flip()
        pygame.time.wait(waitTime)

if __name__ == "__main__":
    main()
