
import numpy as np
import matplotlib
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
from scipy import signal

import Image
import scipy
import math

im = Image.open('/home/kkirsanov/workspace/LMM/cap/img/488.jpg').convert("L")

nim = np.asarray(im)
nim = signal.medfilt(nim, 3)
print im.format, im.size, im.mode


sy, sx = nim.shape


fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

#print m2
ax1.imshow(nim)


plt.show()
