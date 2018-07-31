#coding=utf-8
import random
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

import time  # , threading

import os
# os.putenv("DISPLAY", ":99")

# import thread
import time

import mts_learn_images

detector = mts_learn_images.Detector()

class Mts2(object):
    def LS(self):
        # print "LS"
        pass

    def __init__(self, url):
        self.step = 0
        self.url = url
    def start(self):
        self.app = QApplication(sys.argv)
        # QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.HttpProxy,self.proxy, self.proxyp))
        self.web = QWebView()
        # self.web.loadProgress.connect(self.percent)
        self.web.loadFinished.connect(self.done_exit)
        self.web.load(QUrl(self.url))
        #self.web.show()
        self.app.exec_()
        return True
    def confirm(self, code, proxy=None, proxyp=None):
        self.code = code
        self.app = QApplication(sys.argv)
 
        if proxy:       
            self.proxy=proxy
            self.proxyp=proxyp
            QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.HttpProxy,self.proxy, self.proxyp))
        self.web = QWebView()

        self.web = QWebView()
        self.web.loadFinished.connect(self.done)
        self.web.load(QUrl(self.url))
        self.web.show()
        self.app.exec_()    
        QTimer.singleShot(34000, self.exit)
    def refresh(self):
        self.web.page().mainFrame().evaluateJavaScript("""
            $('.refreshButton').click();
        """)
        QTimer.singleShot(6000, self.getData)
    def click(self, i):
        self.web.page().mainFrame().evaluateJavaScript("""
            $('li.item').each(function(index, para) {
                if (index == %d){
                    $(para).click()
                };
            });
         """ % i);
    def getData(self):
        self.web.update()
        import random
        for i, x in enumerate(self.web.page().mainFrame().findAllElements('label')):
            if i == 1:
                task = x.toInnerXml ()
                task=unicode(task).encode('utf-8')
        cnt = 0
        sdir = self.url.split('=')[-1]
        self.images = []
        
        for x in self.web.page().mainFrame().findAllElements('img'):
            # print str(x.attribute("src"))
            cnt += 1
            try:
                os.mkdir(sdir)
            except:
                pass
            geom = x.geometry()
            size = QSize(50, 50)
            # print size
            # continue
            image = QImage(size, QImage.Format_ARGB32)
            image.fill(0)
            paint = QPainter(image)
            paint.eraseRect(0, 0, 50, 50)
            x.render(paint)
            paint.end()
            imname = "./%s/%d-%d.png" % (sdir, self.step, cnt)
            # print imname
            
            image.save(imname, "PNG")
        f = open('./%s/%d-q.txt' % (sdir, self.step), "w")
        f.write(task)
        f.close()
        _f = open('./%s/0-q.txt' % sdir)
        task = _f.readline().decode('utf-8')
        # self.step = self.step + 1
        # print "step: ", self.step
        #try:
        if u"цвет" in task:
            #print "refresh"                
            QTimer.singleShot(1000, self.refresh)
        else:
            for p, d, f in os.walk('./%s/' % sdir):
                q = task.split('-')[-1].strip()
                term = q
                #print "TERM: ", term
                #print "TASK: ", task
                #exit()
                items = []
                for x in range(1, 6):
                    if detector.check('./%s/0-%d.png' % (sdir, x), unicode(term)):
                        items.append(True)
                    else:
                        items.append(False)
                #print items
            if reduce(lambda a, b: a or b, items) == False:
                QTimer.singleShot(1000, self.refresh)
            else:
                for i, b in enumerate(items):
                    if b:
                        self.click(i)
                        #e3 = self.web.page().mainFrame().findFirstElement("#TextBoxActivationCode");
                        #e3.setAttribute('value', str(self.code))
                        self.web.page().mainFrame().evaluateJavaScript("""
                            $('#TextBoxActivationCode').val('%s');
                        """%str(self.code))
                        self.web.page().mainFrame().evaluateJavaScript("""
                            $('#ButtonSubmit').click();
                        """)

        #except Exception, e:
        #    print "Error", e
        #    QTimer.singleShot(1000, self.exit)
    def testUrl(self):  
        tmpurl = str(self.web.url())
        if ("moipodpiski.ssl.mts.ru" not in tmpurl) and ('re-billing' not in tmpurl):
            print "True"
            QTimer.singleShot(1000, self.exit)
        else:
            if u"еверный код" in self.web.page().mainFrame().toHtml():
                print "False"
                QTimer.singleShot(1000, self.exit)   
        QTimer.singleShot(3000, self.testUrl)
    def done(self, var):
        self.testUrl()
        QTimer.singleShot(3000, self.getData)
    def exit(self):
        self.app.exit()
    def done_exit(self, var):
        QTimer.singleShot(10000, self.exit)
        
    def percent(self, p):
        # print p
        self.web.update()
        pass

if __name__ == "__main__":
    m = Mts2('http://moipodpiski.ssl.mts.ru/lp/?SID=65e8580a-8fbf-27ab-5a81-000014305326')
    # m.start()
    m.confirm(7699)
