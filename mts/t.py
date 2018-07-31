#coding=utf-8
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *
import time, datetime, os, random, sys, thread


class MTSParser:
    def doExit(self, threadName, delay):
        count = 0
        while count < 5:
            time.sleep(1)
            count += 1
            if self.debug:
                print "timer: ", 35-count
        print "False"
        self.app.exit()
        time.sleep(1)
        os.abort()
              
    def __init__(self, url, subid):
        self.step=0
        self.debug=True
   
    def onDone2(self,val):
        print "done"
        self.app.processEvents()
        frame = self.web.page().mainFrame()
        size = frame.contentsSize()
        self.web.page().setViewportSize(size)
        image = QImage(size, QImage.Format_ARGB32)
        image.fill(0)
        paint = QPainter(image)
        frame.render(paint)
        paint.end()
        imname = "zz.png"
        print "Saved"
        image.save(imname, "PNG")   

        self.exit()


    def exit(self):
        self.app.exit()
        exit()
    def percent(self, p):
        if self.debug:
            #print "percent: ", p
            pass
        self.web.update()

    def url_changed(self, url):  
        if self.debug:        
            print 'url changed: ', url
    def confirm(self, smscode):
        import pickle
        self.debug=False
        self.smscode = smscode
        self.code = smscode

        now = datetime.datetime.today().date()
        self.app = QApplication(sys.argv)
        print (sys.argv)
        self.web = QWebView()
        
        self.web.loadFinished.connect(self.onDone2)
        self.web.connect(self.web, SIGNAL("urlChanged(const QUrl&)"), self.url_changed)
        self.web.load(QUrl("http://www.ya.ru"))
        
        self.web.show()
        self.debug=True#False
        thread.start_new_thread( self.doExit, ("Thread-1", 1) )
        self.app.exec_()
if __name__=="__main__":
    m = MTSParser("", 422003)
    m.confirm("6915")
