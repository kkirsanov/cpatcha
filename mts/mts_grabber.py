#codng=utf-8
import random
from pprint import pprint
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

import time, threading

import os
#os.putenv("DISPLAY", ":99")

import thread
import time

class Mts(object):
    def _button_click_event(self, event):
        print "button click", event

    def __init__(self, url):
        self.url=url
        self.app = QApplication(sys.argv)
        #QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.HttpProxy,self.proxy, self.proxyp))
        self.web = QWebView()
        self.web.loadProgress.connect(self.percent)
        self.web.loadFinished.connect(self.done)
        self.web.load(QUrl(self.url))
        self.web.show()
        self.app.exec_()
    def getData(self):
        for x in self.web.page().mainFrame().findAllElements('img'):
            print x.attribute("src")
            geom = x.geometry()
            size = QSize(50, 50)
            #print size
            continue
            image = QImage(size, QImage.Format_ARGB32)
            paint = QPainter(image)
            x.render(paint)
            paint.end()
            time.sleep(0.1)
            dir = self.url.split('=')[-1]
            try:
                pass
                #os.mkdir(dir)
            except:
                pass
            #image.save("./%s/%s.jpg"%(dir, str(x.attribute("src")).split('=')[-1]), "JPG")
        print "ok"
    def _button_click_event(self):
        print "asd"
    def done(self, var):
        #t = threading.Timer(x+1, self.getData)
        #t.start()
        #self.web.getElementsByTagName('body')
        doc = self.web.page().mainFrame().documentElement()
        nodes = doc.findFirstElement(body)
        #body = nodes.item(0)

        #d = doc.createElement("div")
        #b = doc.createElement("Button")
        #b.innerHTML = "hello"
        #d.appendChild(b)
        #doc.onclick = self._button_click_event
        self.getData()
        
    def percent(self, p):
        print p


if __name__=="__main__":
    m = Mts('http://moipodpiski.ssl.mts.ru/lp/?SID=6f4f96cf-d92d-fb3c-3af1-000014152045')
    
#12fgjcnjkjd