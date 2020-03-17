import pygame
import json
import numpy as np

from Lane import Lane
from Car import Car
from Street import Street
from Intersection import Intersection


def main():
    # setup
    with open("colors.json") as f:
        text = f.read()
        colors = json.loads(text)

    wWidth = 800
    wHeight = 800
    w = pygame.display.set_mode((wWidth, wHeight))
    w.fill(colors["green"])

    width = 30

    streetH = Street((0, wHeight // 2), (wWidth, wHeight // 2), 2, 2)
    streetV = Street((wWidth // 2, 0), (wWidth // 2, wHeight), 1, 4)
    streets = [streetH, streetV]
    intersection = Intersection(streetH, streetV)

    for l in streetH.lanes:
        l.draw(w)
    for l in streetV.lanes:
        l.draw(w)
    cars = []

    waitTime = 10
    flipTime = 590
    cycleNumber = 0
    running = True

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
        flipTime = flipTime + 1
        if flipTime == 300:
            intersection.changeToYellow()

        if flipTime == 500:
            intersection.changeToRed()

        if flipTime == 600:
            if cycleNumber == 0:
                intersection.changeToCycle(intersection.cycles[0])
                cycleNumber = 1
            else:
                intersection.changeToCycle(intersection.cycles[1])
                cycleNumber = 0
            flipTime = 0

        if np.random.randint(20) == 0:
            i = np.random.randint(2)
            carLane = streets[i].lanes[np.random.randint(0, len(streets[i].lanes) - 1)]
            car = Car((255, 0, 0), carLane, intersection, desiredSpeed=np.random.normal(1.35, 0.1))
            cars.append(car)
            #TODO make sure the cars dont overlap when you spawn them

        w.fill(colors["green"])
        for l in streetH.lanes:
            l.draw(w)
        for l in streetV.lanes:
            l.draw(w)

        intersection.draw(w)
        carRects = []
        for car in cars:
            carRects.append(car.rect)

        for i, car in enumerate(cars):

            collisionIdxs = car.hitBox.collidelistall(carRects)
            if collisionIdxs != [i]:
                collisionIdxs.remove(i)
                if len(collisionIdxs) > 1:
                    car.speed = 0  # TODO: better way to handle this?
                    print("multiple collisions detected")
                else:
                    car.speed = cars[collisionIdxs[0]].speed * 0.7

        for c in cars:
            c.move(carRects)
            c.draw(w, showHitbox=False)

            if c.distance >= c.lane.length + 2 * c.LENGTH:
                cars.remove(c)

        for light in intersection.lights:
            light.draw(w)

        pygame.display.flip()
        pygame.time.wait(waitTime)

if __name__ == "__main__":
    main()
