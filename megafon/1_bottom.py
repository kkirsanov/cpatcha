
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

im = Image.open('/home/kkirsanov/workspace/LMM/cap/img/14.jpg').convert("L")

nim = np.asarray(im)
nim = signal.medfilt(nim, 3)
print im.format, im.size, im.mode


sy, sx = nim.shape

medians = [0.0] * sx
tops = [0.0] * sx

divs = [0] * sx

for x in range(sx - 1):
    for y in range(sy - 1):
        if nim[y][x] == 0:
            if divs[x] < 1:
                pass 
            medians[x] += sy - y
            divs[x] += 1
            
for x in range(sx - 1):
    for y in range(sy - 1):
        if nim[sy - y - 1][x] < 200:
            tops[x] = sy - y - 1
            break
        


tops[0] = 30
#filter
tops = signal.medfilt(tops, 3)


#for i, m in enumerate(tops):
#    if i > 1:
#        if abs(tops[i] - tops[i - 1]) > 10:
#            tops[i] = tops[i - 1]


fig = plt.figure()
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)

#print m2
ax1.imshow(nim)

#ax1.plot(tops, label="filtered", color="g")
#ax1.legend()



def F(V, x):
    return  V[0] + V[1] * np.sin(x * V[2] + V[3]) + V[4] * np.sin(x * V[5] + V[6])

error = lambda v, x, y: ((F(v, x) - y) ** 2).sum()
startData = [35.07, 41.22, 0.099, 10.584, 35.251, 0.1029, 0.93 ]

#[ 39.60971775  44.52777594   0.10000669  10.24120648  40.90469910.10714123   0.36085274]

x = np.arange(0, 140)
fn = lambda x: tops[x]
y = fn(x)
v = fmin(error, startData, args=(x, y), maxiter=10000, maxfun=10000)
print v
ax2.plot(tops, label="filtered", color="g")
vals = F(v, np.arange(0, 140))
ax2.plot(vals, label="filtered2", color="r")
vals = F(startData, np.arange(0, 140))
ax2.plot(vals, label="filtered2", color="g")



newim = Image.new("L", (sx, sy))
sd = v
sd[0] = 0
for x in range(sx):
    newY = F(sd, x)
    for y in range(sy):
        ny = y - newY/2
        if ny > sy or ny < 0:
            newim.putpixel((x, y),0)
        else:
            newim.putpixel((x, y), nim[int(sy - ny - 1)][x])
            
        
ax3.imshow(newim)



plt.show()


#F(startData, x)
