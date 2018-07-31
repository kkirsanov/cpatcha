# coding=utf-8
import os
import scipy as sp
import numpy
import hashlib
from PIL import Image
import ImageFilter
import yaml
from scipy.misc import imread

class Detector:
    def _readRaw(self, fname):
        z = imread(fname)
        z.shape = (1, 50 * 50)
        z = z.astype(numpy.int16)
        return z
    def _prepepare(self):
        files = None
        for p, d, f in  os.walk("./mts-data"):
            files = f
        files.sort()
        imgFiles = filter(lambda x:'.png' in x, f)
        images = set()
        for i, fname in enumerate(imgFiles):
            f = open('./mts-data/' + fname, "r")
            im = Image.open(f)
            im2 = self._imageWork(im)
            f.close()
            im2.save("./t1/%s.bmp" % fname)
    def _imageWork(self, im):
        i = im.copy()
        i = i.filter(ImageFilter.MedianFilter(3))
        i = i.filter(ImageFilter.MinFilter(3))
        i = i.convert("L")
        i = Image.eval(i, lambda px: 0 if px < 252 else 255)
        return i
    def __init__(self):
        self.objects = yaml.load(open('objects.yaml'))
        self.images = dict()
        for k, v in self.objects.iteritems():
            if v:
                self.images[k] = []
                for f in v:
                    if len(filter (lambda x:x in "0123456789", f)) == 0:
                        for object in self.objects[f]:
                            f2 = "./t1/%s.png.bmp" % object
                            self.images[k].append(self._readRaw(f2))
                    else:
                        f2 = "./t1/%s.png.bmp" % f
                        self.images[k].append(self._readRaw(f2))
    def _loadIm(self, image_path):
        i = Image.open(open(image_path, "r"))
        i2 = self._imageWork(i)
        im1 = numpy.asarray(i2)
        im1.shape = (1, 50 * 50)
        return im1
    def check(self, image_path, term):
        im = self._loadIm(image_path)
        for x in self.images[term]:
            dif = (x - im).std()
            # print dif
            if dif < 17:
                return True
        return False

    def classify(self, image_path):
        data = []
        mindif = 10000
        minterm = ""
        im = self._loadIm(image_path)
        for term, images in self.images.iteritems():
            for image in images:
                # print images
                dif = (im - image).std()
                if dif < mindif:
                     mindif = dif
                     minterm = term
                if dif < 40:
                    data.append((dif, term))
        data.sort()
        return set([x for y, x in data])

if __name__ == "__main__":
    C = Detector()
    # C._prepepare()
    # exit()
    ans = C.classify("./e10bdc68-aa42-fb17-5a83-000014272949/0-1.png")
    for term in ans:
        print term
    """
    files = None
    for p, d, f in  os.walk("./mts-data"):
        files = f
    files.sort()
    imgFiles = filter(lambda x:'.png' in x, f)
    images = set()
    for i, fname in enumerate(imgFiles):
        z = C.classify('./mts-data/' + fname)
        if not z:
            print i, fname, z
    """