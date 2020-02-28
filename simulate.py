import pygame
import json
from Lane import Lane
from Car import Car
from Street import Street
from random import randint

def main():
    # setup
    with open("colors.json") as f:
        text = f.read()
        colors = json.loads(text)

    w = pygame.display.set_mode((800, 800))
    w.fill(colors["green"])

    width = 30

    streetH = Street((0, 800 // 2), (800, 800 // 2), 2, 2)
    streetV = Street((800 // 2, 0), (800 // 2, 800), 1, 4)
    streets = [streetH, streetV]

    for l in streetH.lanes:
        l.draw(w)
    for l in streetV.lanes:
        l.draw(w)
    cars = []

    waitTime = 10
    running = True

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return

        if randint(1, 100) == 1:
            i = randint(0, 1)
            carLane = streets[i].lanes[randint(0, len(streets[i].lanes) - 1)]
            car = Car((255, 0, 0), carLane)
            cars.append(car)

        w.fill(colors["green"])
        for l in streetH.lanes:
            l.draw(w)
        for l in streetV.lanes:
            l.draw(w)
        for c in cars:
            c.distance += 1
            c.updateRect()
            c.draw(w)
            if c.distance >= 800 + 2 * c.LENGTH:
                cars.remove(c)

        pygame.display.flip()
        pygame.time.wait(waitTime)

if __name__ == "__main__":
    main()
