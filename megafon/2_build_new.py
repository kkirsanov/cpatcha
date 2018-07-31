#generate new images

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

def F(V, x):
    return  V[0] + V[1] * np.sin(x * V[2] + V[3]) + V[4] * np.sin(x * V[5] + V[6])


for i in range(1000):
    
    im = Image.open('/home/kkirsanov/workspace/LMM/cap/img/%d.jpg' % i).convert("L")
    
    nim = np.asarray(im)
    nim = signal.medfilt(nim, 1)
    sy, sx = nim.shape
    V = [1.30637172e+01 , 6.30227864e+02   , 1.01086914e-01 , 1.04784433e+01, 6.27265787e+02  , 1.01292067e-01  , 1.04071755e+00]
    x = np.arange(0, sx)
    newim = Image.new("L", (sx, sy), color=255)
    #V[0] = 0
    for x in range(sx):
        newY = F(V, x)
        for y in range(sy):
            ny = y - newY
            if ny > sy or ny < 0:
                pass
            else:
                newim.putpixel((x, sy - y - 1), nim[int(sy - ny - 1)][x])
    #newim.show() 
    newim = newim.crop((0, 0, sx, 40))
    newim.save('/home/kkirsanov/workspace/LMM/cap/img2/%d.jpg' % i)
    print i
