import Image
import numpy as np
from scipy import signal
import subprocess
from os import unlink

def F(V, x):
    return  V[0] + V[1] * np.sin(x * V[2] + V[3]) + V[4] * np.sin(x * V[5] + V[6])

def capcha(filepath):
    im = Image.open(filepath).convert("L")
    
    nim = np.asarray(im)
    nim = signal.medfilt(nim, 1)
    sy, sx = nim.shape
    V = [1.30637172e+01, 6.30227864e+02, 1.01086914e-01, 1.04784433e+01, 6.27265787e+02, 1.01292067e-01, 1.04071755e+00]
    x = np.arange(0, sx)
    newim = Image.new("L", (sx, sy), color=255)
    for x in range(sx):
        newY = F(V, x)
        for y in range(sy):
            ny = y - newY
            if ny > sy or ny < 0:
                pass
            else:
                newim.putpixel((x, sy - y - 1), nim[int(sy - ny - 1)][x])
    newim = newim.crop((0, 0, sx, 40))
    
    newname = filepath + ".new.tif"
    newim.save(newname)
    try:
        f = open('digits', "w")
        f.write('tessedit_char_whitelist 0123456789')
        f.close()
    except:
        pass
    #process = subprocess.Popen(['tesseract', newname, newname, '-psx8', './digits'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    process = subprocess.Popen(['tesseract', newname, newname], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    process.communicate()
    
    txt = open(newname + ".txt", "r")
    txt = "".join(txt.readlines())
    t1 = txt.replace("\n", "")
    #print txt
    unlink(newname + ".txt")
    unlink(newname)
    txt = filter(lambda x:x in '0123456789', txt)
    
    if len(txt) == 6:
        return txt
    else:
        return "FAIL: " + t1

#mini test
cnt=0
if __name__ == '__main__':
    print capcha('/var/www/capmega_8.png')
