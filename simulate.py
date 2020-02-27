import pygame
import json
from Lane import Lane
from Car import Car
from random import randint

def main():
    # setup
    with open("colors.json") as f:
        text = f.read()
        colors = json.loads(text)

    w = pygame.display.set_mode((1000, 1000))
    w.fill(colors["green"])

    width = 30

    # lanes
    laneGoingRight = Lane((100, 800 // 2 - width), (800, 800 // 2 - width))
    laneGoingLeft = Lane((800, 800 // 2), (100, 800 // 2))
    laneGoingDown = Lane((800 // 2 - width, 100), (800 // 2 - width, 800))
    laneGoingUp = Lane((800 // 2, 800), (800 // 2, 100))

    lanes = [laneGoingRight, laneGoingLeft, laneGoingDown, laneGoingUp]
    for l in lanes:
        l.draw(w)
    cars = []

    waitTime = 10
    running = True

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return

        if randint(1, 100) == 1:
            carLane = lanes[randint(0, len(lanes) - 1)]
            car = Car((255, 0, 0), carLane)
            cars.append(car)

        w.fill(colors["green"])
        for l in lanes:
            l.draw(w)
        for c in cars:
            c.distance += 1
            c.updateRect()
            c.draw(w)
            if c.distance >= 800:
                cars.remove(c)

        pygame.display.flip()
        pygame.time.wait(waitTime)

if __name__ == "__main__":
    main()
