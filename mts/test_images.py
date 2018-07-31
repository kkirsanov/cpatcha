#coding=utf8
import mts_learn_images

import os


F = []
d = mts_learn_images.Detector()
for root, subFolders, files in os.walk("./newim2/"):
    #for folder in subFolders:
        #print "%s has subdirectory %s" % (root, folder)
    for filename in files:
        filePath = os.path.join(root, filename)
        if ".png" in filePath:
            try:
                if int(filePath.split("/")[-1].split('.')[0])>=0:
                    F.append(filePath)
            except:
                pass
            

from PIL import Image


im = Image.open("/home/kkirsanov/workspace/LMM/capcha/newim2/397.png")
im2 = d._imageWork(im)
im2.save("./chair.png.bmp")

#d._imageWork()
exit()

for i, f in enumerate(F):
    print f
    cls = d.classify(f)
    print i,len(F),     
    if cls:
        for c in cls:
            print c,
    else:
        print f
        fl = open(f, "r")
        z = fl.read(9999999)
        fl2 = open ("./newim2/%d.png"%i, "w")
        fl2.write(z)
        fl.close()
        fl2.close()

