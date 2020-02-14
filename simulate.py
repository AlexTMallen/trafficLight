import pygame
import json

def main():
    # setup
    with open("colors.json") as f:
        text = f.read()
        colors = json.loads(text)

    w = pygame.display.set_mode((500, 500))
    w.fill(colors["green"])

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
