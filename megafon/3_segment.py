
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
import time

border = 150
class Strip:
    def __init__(self, x1, x2, y, m):
        self.x1 = x1
        self.x2 = x2
        self.y = y
        self.m = m
        self.b = False
    def len(self):
        return self.x2 - self.x1
    def __str__(self):
        return str((str(self.x1), str(self.x2), str(self.y), str(self.m)))
def genStrips(mt):
    splitY = 20
    
    sy, sx = mt.shape
    sizeY = sy / splitY    
    
    prevM = -1
    m = -1.0
    strips = []
    prevX = 0
    for stepY in range(splitY):
        strips.append([])
        for x in range(sx):
            prevM = m
            m = 0.0
            for y in range(stepY * sizeY, (stepY + 1) * sizeY):
                m += mt[y][x]
            m /= sizeY
            
            if len(strips[-1]) == 0:
                strips[-1].append(Strip(0, x, stepY, m))
            else:
                if abs(strips[-1][-1].m - m) < 35:
                    strips[-1][-1].x2 = x
                    strips[-1][-1].m = m#(strips[-1][-1].m + ((strips[-1][-1].m + m) / 2.0)) / 2.0
                else:
                    strips[-1].append(Strip(x, x, stepY, m))
    return strips




import subprocess
for filecnt in range(0, 1000):
    #process = subprocess.Popen(['tesseract', '/home/kkirsanov/workspace/LMM/cap/img2/%d.jpg' % filecnt, '/home/kkirsanov/workspace/LMM/cap/img2/%d' % filecnt, '-psm 8'], stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.STDOUT)
    #process.communicate()
    #print filecnt
    #continue

    im = Image.open('/home/kkirsanov/workspace/LMM/cap/img2/%d.jpg' % filecnt).convert("L")
    print filecnt
    
    nim = signal.medfilt(np.asarray(im), 3)
    
    img = np.asarray(Image.new("RGB", im.size))
    img.flags.writeable = True
    
    sx, sy = im.size
    
    curc = 0
    colors = [(255, 255, 0)]
            
    fig = plt.figure()
    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)
    ax1.imshow(nim)
    ax2.imshow(img)
    ax3.imshow(img)
    
    
    strips = genStrips(nim)
    for i, st in enumerate(strips):
        strips[i] = filter(lambda x:x.len() >= 1, st)
        
    
    mmin = strips[0][0].m
    mmax = strips[0][0].m
    
    #move together
    for i, st in enumerate(strips):
        for j, s in enumerate(st):
            if j == 0:
                s.x1 = 0
            if j == len(st) - 1:
                s.x2 = sx
                
            try:
                x1 = s.x2
                x2 = st[j + 1].x1
                x = x1 + (x2 - x1) / 2
                s.x2 = x
                st[j + 1].x1 = x
            except:
                pass
    #unite
    strips2 = []
    for i, st in enumerate(strips):
        strips2.append([])
        for j, s in enumerate(st):
            if j == 0:
                strips2[-1].append(s)
                continue
            if (strips2[-1][-1].m > border and s.m > border):
                strips2[-1][-1].x2 = s.x2
                continue
            else:
                if (strips2[-1][-1].m < border and s.m < border):
                    strips2[-1][-1].x2 = s.x2
                    continue
                else:
                    strips2[-1].append(s)
                
    for st in strips2:
        for s in st:
            c = "W"
            if s.m > border:
                c = "B"
            ax2.plot([s.x1, s.x2], [s.y * 2 + 1 ] * 2, color=c)
            if s.m <= border:
                ax2.plot([s.x1 + s.len() / 2 ], [s.y * 2 + 1 ], "x", color="R")
        
    img = Image.fromarray(np.uint8(img))
    plt.show()
    break
    plt.savefig("/home/kkirsanov/workspace/LMM/cap/img3/%d.jpg" % filecnt)
    plt.clf()
    #break
