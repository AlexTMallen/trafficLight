import numpy as np
from skimage import data, io
from matplotlib import pyplot as plt

dirs = ["Right", "Left", "Up", "Down"]
carIms = []
for dir in dirs:
    carIms.append(io.imread("yellowCar" + dir + ".png"))

greenCars = [np.zeros((12, 25, 4)), np.zeros((12, 25, 4)), np.zeros((25, 12, 4)), np.zeros((25, 12, 4))]
blueCars = [np.zeros((12, 25, 4)), np.zeros((12, 25, 4)), np.zeros((25, 12, 4)), np.zeros((25, 12, 4))]
grayCars = [np.zeros((12, 25, 4)), np.zeros((12, 25, 4)), np.zeros((25, 12, 4)), np.zeros((25, 12, 4))]
whiteCars = [np.zeros((12, 25, 4)), np.zeros((12, 25, 4)), np.zeros((25, 12, 4)), np.zeros((25, 12, 4))]
redCars = [np.zeros((12, 25, 4)), np.zeros((12, 25, 4)), np.zeros((25, 12, 4)), np.zeros((25, 12, 4))]

for dirNum, im in enumerate(carIms):
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if im[i, j, 0] == im[i, j, 1]:
                greenCars[dirNum][i, j, 1] = im[i, j, 0]
                blueCars[dirNum][i, j, 2] = im[i, j, 0]
                whiteCars[dirNum][i, j, 0:3] = im[i, j, 0]
                grayCars[dirNum][i, j, 0:3] = im[i, j, 0] / 5
                redCars[dirNum][i, j, 0] = im[i, j, 0]

                greenCars[dirNum][i, j, 3] = im[i, j, 3]
                blueCars[dirNum][i, j, 3] = im[i, j, 3]
                grayCars[dirNum][i, j, 3] = im[i, j, 3]
                whiteCars[dirNum][i, j, 3] = im[i, j, 3]
                redCars[dirNum][i, j, 3] = im[i, j, 3]
            else:
                greenCars[dirNum][i, j, 0:4] = im[i, j, 0:4].copy()
                blueCars[dirNum][i, j, 0:4] = im[i, j, 0:4].copy()
                grayCars[dirNum][i, j, 0:4] = im[i, j, 0:4].copy()
                whiteCars[dirNum][i, j, 0:4] = im[i, j, 0:4].copy()
                redCars[dirNum][i, j, 0:4] = im[i, j, 0:4].copy()

for i, im in enumerate(greenCars):
    io.imsave("greenCar" + dirs[i] + ".png", im)
for i, im in enumerate(redCars):
    io.imsave("redCar" + dirs[i] + ".png", im)
for i, im in enumerate(grayCars):
    io.imsave("grayCar" + dirs[i] + ".png", im)
for i, im in enumerate(whiteCars):
    io.imsave("whiteCar" + dirs[i] + ".png", im)
for i, im in enumerate(blueCars):
    io.imsave("blueCar" + dirs[i] + ".png", im)


