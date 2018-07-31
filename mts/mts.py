#coding=utf-8
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *
import time, datetime, os, random, sys, thread

#os.putenv("DISPLAY", ":99")

def loadProxy():
    f = open ("prx.lst")
    p = []
    for l in f:
        p.append(l.split(':'))
        p[-1][-1] = int(filter(lambda x:x in "0123456789", p[-1][-1]))
    return p

class MTSParser:
    def doExit(self, threadName, delay):
        count = 0
        while count < 25:
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
        p, pp=random.choice(loadProxy())
        self.proxy=p#"195.68.156.250"
        self.proxyp=pp#8080
        self.mtsData = {}
        self.cntDone = 0
        self.cookies = []
        self.url = url
        self.action = ""
        self.subid = str(subid)
        self.canexit=False

    def refresh(self):
        self.web.page().mainFrame().evaluateJavaScript("""
            $('.refreshButton').click();
        """)
        if self.debug:
            print "refresh"
        QTimer.singleShot(4000, self.getData)
    def click(self, i):
        self.web.page().mainFrame().evaluateJavaScript("""
            $('li.item').each(function(index, para) {
                if (index == %d){
                    $(para).click()
                };
            });
         """ % i);
    def getData(self):
        if self.debug:
            print "GD"
        self.web.update()
        task=None

        for i, x in enumerate(self.web.page().mainFrame().findAllElements('label').toList()):
            #print i,x
            if i == 1:
                task = x.toInnerXml ()
                task=unicode(task).encode('utf-8')
            if i > 50:
                task=None
                break;
        if not task:
            if self.debug:
                print "no task"
            self.refresh()
            return
        cnt = 0

        sdir = self.path + self.url.split('=')[-1]
        if self.debug:
            print "making dir", sdir
        try:
            os.mkdir(sdir)
        except Exception, e:
            if self.debug:
                print e
        self.images = []
        for x in self.web.page().mainFrame().findAllElements('img').toList():
            if self.debug:
                #print str(x.attribute("src"))
                pass
            cnt += 1
            
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
            imname = "%s/%d.png" % (sdir,cnt)
            # print imname
            if cnt>10:
                break
            image.save(imname, "PNG")
        f = open('%s/0-q.txt' % sdir, "w")
        f.write(task)
        time.sleep(0.3)
        f.close()
        #print '%s/0-q.txt' % sdir
        _f = open('%s/0-q.txt' % sdir)
        task = _f.readline().decode('utf-8')
        if u"цвет" in task:
            self.refresh()
        else:
            q = task.split('-')[-1].strip()
            term = q
            if self.debug:                
                print "TERM: ", term
                print "TASK: ", task
            items = []
            for x in range(1, 8):
                try:
                    if self.detector.check('%s/%d.png' % (sdir, x), unicode(term)):
                        items.append(True)
                    else:
                        items.append(False)
                except:
                    break
            if reduce(lambda a, b: a or b, items) == False:
                if self.debug:
                    print "zero find"
                self.refresh()
            else:
                for i, b in enumerate(items):
                    if b:
                        self.click(i)
                js = "$('#TextBoxActivationCode').val('%s');" % str(self.code)
                if self.debug:
                    print js
		        time.sleep(0.3)
                self.web.page().mainFrame().evaluateJavaScript(js)
                
                self.web.page().mainFrame().findFirstElement("#TextBoxActivationCode").setAttribute('value', self.code)
                
                self.web.page().mainFrame().findFirstElement("#ButtonSubmit").evaluateJavaScript('this.click();')
                time.sleep(0.3)
                self.web.page().mainFrame().evaluateJavaScript("""
                    $('#ButtonSubmit').click();
                """)
                self.RenderPage("click")
                if self.debug:
                    print "clicked with code", str(self.code)

    def testUrl(self):  
        tmpurl = str(self.web.url())
        if self.debug:
           print tmpurl
        if  ("moipodpiski.ssl.mts.ru" not in tmpurl) and (str(tmpurl)!="PyQt4.QtCore.QUrl(u'')"):
            print "True"
            self.exit()
            return
        else:
            if u"еверный код" in self.web.page().mainFrame().toHtml():
                print "False wrong code"
                self.exit()
                return
                pass
        QTimer.singleShot(3000, self.testUrl)
    def RenderPage(self, n=""):
        self.app.processEvents()
        frame = self.web.page().mainFrame()
        size = frame.contentsSize()
        self.web.page().setViewportSize(size)
        image = QImage(size, QImage.Format_ARGB32)
        image.fill(0)
        paint = QPainter(image)
        frame.render(paint)
        paint.end()
        imname = self.path + "render_%s_%s_%s.png"% (self.subid, self.step, n)
        image.save(imname, "PNG")   
    def onDone1(self, val):
        self.step += 1
        if True:#self.debug:
            #print "Done"
            z = self.web.page().mainFrame().toHtml()
            f=open(self.path + "html_%s_%s.html"% (self.subid, self.step) , "w")
            f.write(unicode(z).encode('utf-8'))
            f.close()
            self.RenderPage("done")
        tmpurl = str(self.web.url())
        if self.debug:
            print tmpurl
        if ("moipodpiski.ssl.mts.ru" not in tmpurl):# and ('re-billing' not in tmpurl):
            print "True"
            self.exit()
            

    def init(self, ua):
        try:
            os.mkdir('./mts')
        except:
            pass
        try:
            now = datetime.datetime.today().date()
            os.mkdir("./mts/" + str(now))
        except:
            pass
        import httplib2, httplib
        pi = httplib2.ProxyInfo(3, self.proxy, self.proxyp)
        con = httplib2.Http(proxy_info=pi)
        #con = httplib2.Http()
        con.follow_redirects = False
        headers = {'Referer': 'http://' + self.url}
        resp, body = con.request(self.url, 'GET', headers=headers)
        if resp.status != 200: 
            print "Fail: Session closed y operator"
            return
        cookies = resp['set-cookie']
        headers['User-Agent'] = ua
        headers['Cookie'] = cookies
        headers['Referer'] = self.url
        headers['Origin'] = 'http://moipodpiski.ssl.mts.ru/'
        inputs = {}
        data = {
            'url': self.url,
            'headers': headers,
            'inputs': inputs,
            'proxy' : self.proxy,
            'proxyp':self.proxyp
        }
        import pickle
        pickle.dump(data, open('./mts/%s/%s.subscribe' % (str(now), self.subid), "w"))
        print " captcha: pass",
        return
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
        try:
            #print './mts/%s/%s.subscribe' % (str(now), self.subid)
            data = pickle.load(open('./mts/%s/%s.subscribe' % (str(now), self.subid), "r"))
            self.path = './mts/%s/' % str(now)
        except Exception, e:
            #print e
            now = (datetime.datetime.today() - datetime.timedelta(days=1)).date()
            data = pickle.load(open('./mts/%s/%s.subscribe' % (str(now), self.subid), "r"))
            self.path = './mts/%s/' % str(now)
        self.url = data['url']
        self.proxy=data['proxy']
        self.proxyp=data['proxyp']
        self.app = QApplication(sys.argv)
        QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.HttpProxy,self.proxy, self.proxyp))
        self.web = QWebView()
        
        self.web.loadFinished.connect(self.onDone1)
        #self.web.loadProgress.connect(self.percent)
        self.web.connect(self.web, SIGNAL("urlChanged(const QUrl&)"), self.url_changed)
        self.web.load(QUrl(self.url))
        
        self.web.show()
        self.debug=True#False
        self.debug=False
        thread.start_new_thread( self.doExit, ("Thread-1", 1) )
        import mts_learn_images
        self.detector = mts_learn_images.Detector()
        QTimer.singleShot(2000, self.testUrl)
        QTimer.singleShot(1000, self.refresh)
        self.app.exec_()
if __name__=="__main__":
    #m = MTSParser("http://moipodpiski.ssl.mts.ru/lp/?SID=22bea70c-4947-1eb5-4146-000016946937", 16946937)
    #m.init(ua="webkit")
    m = MTSParser("", 16946937)
    m.confirm("7580")
