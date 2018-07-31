
import numpy as np
import matplotlib
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
from scipy import signal
from scipy.optimize import leastsq, fmin


import Image
import scipy
import math
import pylab

im = Image.open('/home/kkirsanov/workspace/LMM/cap/img/335.jpg').convert("L")

nim = np.asarray(im)
nim = signal.medfilt(nim, 1)
print im.format, im.size, im.mode

sy, sx = nim.shape
tops = [0.0] * sx
            
for x in range(sx - 1):
    for y in range(sy - 1):
        if nim[y][x] < 200:
            tops[x] = y
            break


tops[0] = 30
tops[-1] = 30
#filter


tops = signal.medfilt(tops, 1)
fig = plt.figure()
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)

ax1.imshow(nim)


def F(V, x):
    return  V[0] + V[1] * np.sin(x * V[2] + V[3]) + V[4] * np.sin(x * V[5] + V[6])

error = lambda v, x, y: ((F(v, x) - y) ** 2).sum()
startData = [15.07, 41.22, 0.099, 10.584, 35.251, 0.1029, 0.93 ]
startData = [1.50637172e+01 , 6.30227864e+02   , 1.01086914e-01 , 1.04784433e+01,
   6.27265787e+02  , 1.01292067e-01  , 1.04071755e+00]
x = np.arange(0, 140)
fn = lambda x: tops[x]
y = fn(x)
v = fmin(error, startData, args=(x, y), maxiter=10000, maxfun=10000)
print v
ax1.plot(tops, label="filtered", color="g")
ax2.plot(tops, label="filtered", color="g")
vals = F(v, np.arange(0, 140))
ax2.plot(vals, label="aproxV", color="r")
vals = F(startData, np.arange(0, 140))
ax2.plot(vals, label="aproxS", color="g")
ax2.legend()


newim = Image.new("L", (sx, sy))
sd = startData
#sd[0] = 0
for x in range(sx):
    newY = F(sd, x)
    for y in range(sy):
        ny = y - newY
        if ny > sy or ny < 0:
            newim.putpixel((x, y), 255)
        else:
            newim.putpixel((x, y), nim[int(sy - ny - 1)][x])

ax3.imshow(newim)

plt.show()
