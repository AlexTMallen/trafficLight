import pygame
import json
import numpy as np

from Lane import Lane
from Car import Car
from Street import Street
from Intersection import Intersection
import constants


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

    streetH = Street((0, wHeight // 2), (wWidth, wHeight // 2), 2, 2, 0, wWidth // 2)
    streetV = Street((wWidth // 2, 0), (wWidth // 2, wHeight), 1, 3, 0, wHeight // 2)
    streets = [streetH, streetV]
    intersection = Intersection(streetH, streetV)

    for l in streetH.lanes:
        l.draw(w)
    for l in streetV.lanes:
        l.draw(w)
    cars = []

    waitTime = 10
    time = 0
    running = True
    intersection.changeToCycle(intersection.hgreenCycle)

    carRects = []
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
        time += 1
        intersection.changeCycle(time)
        if time == intersection.totalCycleLength:
            time = 0
        

        if np.random.randint(20) == 0:
            i = np.random.randint(2)
            carLane = streets[i].lanes[np.random.randint(0, len(streets[i].lanes) - 1)]
            car = Car((255, 0, 0), carLane, intersection, desiredSpeed=np.random.normal(1.35, 0.1))
            if not car.hitBox.collidelistall(carRects):  # Making sure the cars don't overlap when spawned
                cars.append(car)

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
                    # TODO: better way to handle this?
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
