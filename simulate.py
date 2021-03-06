import pygame
import json
import numpy as np

from Lane import Lane
from Car import Car
from Street import Street
from Intersection import Intersection
from Options import Options
from collections import deque
import constants


def main():

    pygame.init()
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
    timeAbsolute = 0
    carDensity = 1.2
    running = True
    simulating = True #whether we're in th options menu or not
    typing = False #whether we're typing or not
    intersection.changeToCycle(intersection.hgreenCycle)
    vProb = 0.5
    densityLightAlgorithm = True
    options = Options(streetH.numPos, streetH.numNeg, streetH.numLeftOnly, streetV.numPos, streetV.numNeg, streetV.numLeftOnly, carDensity, 10/waitTime, vProb, densityLightAlgorithm)
    carsPassed = 0
    carsPassedQueue = deque([0]*500)
    flowRate = 0
    avgFlowRate = 0


    carRects = []
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return

            if e.type == pygame.KEYDOWN:
                if typing:
                    if e.key == pygame.K_RETURN:
                        typing = False
                        options.typing = False
                    elif e.key == pygame.K_BACKSPACE:
                        options.index[options.currentIndex] = options.index[options.currentIndex][:-1]
                    else:
                        if options.currentIndex < 6:
                            if options.index[options.currentIndex] == '':
                                options.index[options.currentIndex] += e.unicode
                        else:
                            options.index[options.currentIndex] += e.unicode
                else:
                    if e.key == pygame.K_ESCAPE:
                        if not simulating:
                            waitTime = int(round(10 / float(options.index[7])))
                            carDensity = np.math.log(float(options.index[6]) + 1) + 1
                        simulating = not simulating
                    if e.key == pygame.K_r:
                        streetH = Street((0, wHeight // 2), (wWidth, wHeight // 2), int(options.index[0]), int(options.index[1]), int(options.index[2]), wWidth // 2)
                        streetV = Street((wWidth // 2, 0), (wWidth // 2, wHeight), int(options.index[3]), int(options.index[4]), int(options.index[5]), wHeight // 2)
                        intersection = Intersection(streetH, streetV)
                        waitTime = int(round(10/float(options.index[7])))
                        carDensity = float(options.index[6])
                        cars = []
                        time = 0
                        timeAbsolute = 0
                        carsPassed = 0
                        carsPassedQueue = deque([0]*500)
                        simulating = True

            if not simulating:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    for box in options.inputBoxes:
                        if box.collidepoint(e.pos):
                            if options.inputBoxes.index(box) == 9:
                                densityLightAlgorithm = not densityLightAlgorithm
                                options.index[9] = densityLightAlgorithm
                            else:
                                typing = True
                                options.typing = True
                                options.currentBox = box
                                options.currentIndex = options.inputBoxes.index(box)
                                options.flashTimer = 0

        if time > intersection.totalCycleLength:
            time = 0
        intersection.changeCycle(time)

        time += 1
        if timeAbsolute != 0:
            timeAbsolute += 1

        if simulating:

            if time > intersection.totalCycleLength:
                time = 0
            intersection.changeCycle(time)
            time += 1


            if np.random.rand() > 1/carDensity:
                vProb = float(options.index[8])
                street = np.random.choice((streetV, streetH), p=(vProb, 1 - vProb))
                carLane = street.lanes[np.random.randint(0, len(street.lanes))]
                carColor = np.random.choice(Car.COLORS)
                car = Car(carLane, intersection, carColor, desiredSpeed=np.random.normal(1.35, 0.1))
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
                            #print("multiple collisions detected")
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
                    carsPassed += 1
                    if timeAbsolute == 0:
                        timeAbsolute += 1


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
            if densityLightAlgorithm and numCarsInGreen * (
                    streetH.numLanes + streetV.numLanes) < 0.2 * numGreenLanes * len(carsWaiting) and len(
                    cars) >= 6 and time - intersection.trafficFlow[intersection.cycleNumber - 1][1] * constants.SECOND > 200:
                time = intersection.abruptChangeCycle()

            carsPassedQueue.appendleft(carsPassed)
            flowRate = carsPassed - carsPassedQueue.pop()
            avgFlowRate = 500 * carsPassed/(timeAbsolute + 1)
            if timeAbsolute < 100:
                Options.text(w, "Flow Rate: n/a" , 20, 20, 20)
                Options.text(w, "Average Flow Rate: n/a", 20, 70, 20)
            else:
                Options.text(w, "Current Flow Rate: "+str(flowRate), 20, 20, 20)
                Options.text(w, "Average Flow Rate: " + str(round(avgFlowRate, 1)), 20, 70, 20)

            Options.text(w, "ESC for options", 550, 20, 20)
            Options.text(w, "R to reset", 550, 70, 20)

            pygame.display.flip()
            pygame.time.wait(waitTime)

        else:
            options.draw(w)

            pygame.display.flip()
            pygame.time.wait(waitTime)


if __name__ == "__main__":
    main()
