import pygame
import json
import numpy as np
from math import sqrt

from Lane import Lane
from Car import Car
from Street import Street
from Intersection import Intersection
import config

def main():
    # setup
    with open("colors.json") as f:
        text = f.read()
        colors = json.loads(text)

    wWidth = 800
    wHeight = 800
    w = pygame.display.set_mode((wWidth, wHeight))
    w.fill(colors["green"])

    streetH = Street((0, wHeight // 2), (wWidth, wHeight // 2), 2, 2)
    streetV = Street((wWidth // 2, 0), (wWidth // 2, wHeight), 2, 2)
    streets = [streetH, streetV]
    intersection = Intersection(streetH, streetV)

    for l in streetH.lanes:
        l.draw(w)
    for l in streetV.lanes:
        l.draw(w)
    cars = []
    carDict = []
    travelTimes = []
 
    waitTime = 10
    
    #For data collection
    flipTime = -10
    timer = 0
    cyclecount = 0
    
    greenTime = 10*config.SECOND
    yellowTime = 5*config.SECOND
    redTime = 3*config.SECOND
    totalTime = greenTime + yellowTime + redTime
    
    carsPerSecond = 1
    
    cycleNumber = 0
    running = True

    carRects = []
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
        flipTime = flipTime + 1
        timer = timer + 1/config.SECOND
        if ((flipTime % totalTime) == greenTime):
            intersection.changeToYellow()

        if ((flipTime % totalTime) == greenTime + yellowTime):
            intersection.changeToRed()

        if ((flipTime % totalTime) == 0):
            if cycleNumber == 0:
                intersection.changeToCycle(intersection.cycles[0])
                cycleNumber = 1
            else:
                intersection.changeToCycle(intersection.cycles[1])
                cycleNumber = 0
            
            cyclecount = cyclecount + 1
                    
        if cyclecount == 10:
            temptimeAvg = 0
            temptimeDev = 0
            for time in travelTimes:
                temptimeAvg += time
                
            avgTime = temptimeAvg / len(travelTimes)
            for time in travelTimes:
                temptimeDev += (time - avgTime)**2 
            
            deviation = sqrt(temptimeDev / len(travelTimes))
            
            print("Green Time:" + str(greenTime/config.SECOND))
            print("Average: " + str(avgTime))
            print("Deviation: " + str(deviation))
            print("")
            print("-------------------------------")
            
            fliptime = 1
            cyclecount = 0
            greenTime += 5 * config.SECOND
            totalTime = greenTime + yellowTime + redTime
            travelTimes = []

        if np.random.randint(int(config.SECOND/carsPerSecond)) == 0:
            i = np.random.randint(2)
            carLane = streets[i].lanes[np.random.randint(0, len(streets[i].lanes))]
            car = Car((255, 0, 0), carLane, intersection, desiredSpeed=max(np.random.normal(17*config.METER/config.SECOND, 0.1), 14*config.METER/config.SECOND))
            if not car.hitBox.collidelistall(carRects):  # Making sure the cars don't overlap when spawned
                cars.append(car)
                carDict.append([car, timer])
        
        w.fill(colors["green"])
        for l in streetH.lanes:
            l.draw(w)
        for l in streetV.lanes:
            l.draw(w)

        intersection.draw(w)
        carRects = []
        for car in cars:
            carRects.append(car.rect)
        
        intersection.clear = True
        for car in cars:
            if car.rect.colliderect(car.intersection):
                intersection.clear = False
            

        for i, car in enumerate(cars):

            collisionIdxs = car.hitBox.collidelistall(carRects)
            if collisionIdxs != [i]:
                collisionIdxs.remove(i)
                if len(collisionIdxs) > 1:
                    car.speed = 0  # TODO: better way to handle this?
                    # print("multiple collisions detected")
                else:
                    car.speed = cars[collisionIdxs[0]].speed * 0.7

        for c in cars:
            c.move(carRects)
            c.draw(w, showHitbox=False)

            if c.distance >= c.lane.length + 2 * c.LENGTH:
                for pair in carDict:
                    if pair[0] is c:
                        travelTimes.append(timer - pair[1])
                        carDict.remove(pair)
                cars.remove(c)
                
            
        for light in intersection.lights:
            light.draw(w)
            

        pygame.display.flip()
        pygame.time.wait(waitTime)


if __name__ == "__main__":
    main()
