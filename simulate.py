import pygame
import json
import numpy as np

from Lane import Lane
from Car import Car
from Street import Street
from Intersection import Intersection
import constants


def main():
    seed = 1
    np.random.seed(seed)
    # setup
    with open("colors.json") as f:
        text = f.read()
        colors = json.loads(text)

    wWidth = 800
    wHeight = 800
    w = pygame.display.set_mode((wWidth, wHeight))

    width = 30

    streetH = Street((0, wHeight // 2), (wWidth, wHeight // 2), 4, 2, 1, wWidth // 2)
    streetV = Street((wWidth // 2, 0), (wWidth // 2, wHeight), 3, 3, 1, wHeight // 2)

    intersection = Intersection(streetH, streetV)

    cars = []
    carsWaiting = []  # cars that aren't past the intersection yet

    waitTime = 10
    time = 0
    running = True
    intersection.changeToCycle(intersection.hgreenCycle)

    carRects = []
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return


        if time > intersection.totalCycleLength:
            time = 0
        intersection.changeCycle(time)
        #if
        time += 1
        

        if np.random.randint(20) == 0:
            streetNum = np.random.randint(0, 9)
            street = streetV
            if streetNum >= 7:  # cars x2 as likely to spawn v than h
                street = streetH
            carLane = street.lanes[np.random.randint(0, len(street.lanes))]
            carColor = np.random.choice(Car.COLORS)
            car = Car(carLane, intersection, carColor, desiredSpeed=np.random.normal(1.35, 0.1))
            # TODO
            # car = Car((255, 0, 0), street.lanesNeg[0], intersection, desiredSpeed=np.random.normal(1.35, 0.1))
            if not car.hitBox.collidelistall(carRects):  # Making sure the cars don't overlap when spawned
                cars.append(car)
                carLane.cars.append(car)
                carsWaiting.append(car)

        w.fill(colors["green"])
        for l in streetH.lanes:
            l.draw(w)
        for l in streetV.lanes:
            l.draw(w)

        streetH.drawLines(w)
        streetV.drawLines(w)

        intersection.draw(w)
        carRects = []
        for car in cars:
            carRects.append(car.rect)

        for i, car in enumerate(cars):
            if not car.isTurningLeft:
                collisionIdxs = car.hitBox.collidelistall(carRects)
                if collisionIdxs != [i]:
                    collisionIdxs.remove(i)
                    if len(collisionIdxs) > 1:
                        # TODO: better way to handle this?
                        # print("multiple collisions detected")
                        cheese = 0
                    else:
                        if car.speed != 0:
                            car.speed = cars[collisionIdxs[0]].speed * 0.7

        for c in cars:
            c.move(carRects)
            c.draw(w, showHitbox=False)

            if c.distance >= c.lane.length + 10 * c.LENGTH:
                if c in c.lane.cars:
                    c.lane.cars.remove(c)
                cars.remove(c)
            if c.rect.colliderect(intersection.rect):
                if c in c.lane.cars:
                    c.lane.cars.remove(c)
                if c in carsWaiting:
                    carsWaiting.remove(c)

        numCarsInGreen = 0
        numGreenLanes = 0
        for light in intersection.lights:
            light[0].draw(w)
            if light[0].color == "green":
                numGreenLanes += 1
                numCarsInGreen += len(light[0].lane.cars)

        # if the density algorithm is on, and the density of cars with green ahead is less than 20% the density of cars
        # waiting overall, and there are at least 6 cars, and it's been green for at least 2 seconds, then switch
        densityLightAlgorithm = True
        if densityLightAlgorithm and numCarsInGreen * (streetH.numLanes + streetV.numLanes) < 0.2 * numGreenLanes * len(carsWaiting) and len(cars) >= 6 and time - intersection.trafficFlow[intersection.cycleNumber - 1][1]*constants.SECOND > 200:
            time = intersection.abruptChangeCycle()

        pygame.display.flip()
        pygame.time.wait(waitTime)


if __name__ == "__main__":
    main()
