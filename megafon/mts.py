#codng=utf-8
import random
from pprint import pprint
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

import time

import os
#os.putenv("DISPLAY", ":99")

import thread
import time

def loadProxy():
    f = open ("prx.lst")
    p = []
    for l in f:
        p.append(l.split(':'))
        p[-1][-1] = int(filter(lambda x:x in "0123456789", p[-1][-1]))
    return p



class MTSParser:
# Define a function for the thread
    def doExit(self, threadName, delay):
        count = 0
        while count < 15:
            time.sleep(delay)
            count += 1
            print count
        print "False"
        self.app.exit()
          

    def __init__(self, url, subid):
        p,pp=random.choice(loadProxy())
        self.proxy=p#"195.68.156.250"
        self.proxyp=pp#8080
        self.mtsData = {}
        self.cntDone = 0
        self.cookies = []
        self.url = url
        self.action = ""
        self.subid = str(subid)
        self.canexit=False
    def print_load_percent(self, percent):
        #print percent
        pass
    def onDone1(self, val):
        #print " ", self.web.url(), " "
        #print 'd',self.cntDone 
        self.cntDone += 1
        z = self.web.page().mainFrame().toHtml()
        #if "LinkButtonSendActivationCode" in z:
        #    print "False"
        #    self.app.exit()
        #    return
#        f = open("mts_mf2.html", "w+")
#        f.write(z)
#        f.write("\r\n=============================\r\n")
#        f.close()
        #print  self.cntDone, len(z),  self.web.url() 
        try:
            if len (unicode(z)) < 40 and ('7hlp' in self.web.url() or 're-billing' in self.web.url()) and ("SubscribeResult=t" not in self.web.url()):
                print "True"
                self.app.exit()
                #sys.exit()
        except:
            pass
            
        #if self.cntDone < 0:
        #    print "True"
        #    self.app.exit()
        #    return
        if self.cntDone >= 1:
            #print 'd1'
            
            e = self.web.page().mainFrame().findAllElements("input");
            e3 = self.web.page().mainFrame().findFirstElement("#TextBoxActivationCode");
            e3.setAttribute('value', self.smscode)
            button = self.web.page().mainFrame().findFirstElement("input[type=submit]");
            button.evaluateJavaScript("alert(this)");
            #button.evaluateJavaScript("this.click();");
            #self.cntDone = -10
            #print 'True'
            #self.app.exit()
    def saveState(self):
        data = {}
        data['url'] = self.url
        data['action'] = self.action
        data['form'] = self.mtsData
        data['cookies'] = self.cookies
        data['proxy']=self.proxy
        data['proxyp']=self.proxyp
        
        import pickle
        pickle.dump(data, open("session_mts_%s.subscribe" % self.subid, "w"))
        #if resp.status != 302: return
        #print resp.status
        print 'True'
    def init(self, ua):
        
        import httplib2, httplib
        pi = httplib2.ProxyInfo(3, self.proxy, self.proxyp)

        con = httplib2.Http(proxy_info=pi)
        con.follow_redirects = False
        headers = {'Referer': 'http://' + self.url}
    
        resp, body = con.request(self.url, 'GET', headers=headers)
        #print 'resp 1', resp.status, resp, body
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
        pickle.dump(data, open('session_mts_%s.subscribe' % self.subid, "w"))
        print " captcha: pass",
        return
       
    def confirm(self, smscode):
        import pickle
        
        self.smscode = smscode
        data = pickle.load(open('session_mts_%s.subscribe' % self.subid, "r"))
        self.url = data['url']
        #print self.url
        self.proxy=data['proxy']
        self.proxyp=data['proxyp']
        self.app = QApplication(sys.argv)
        #QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.HttpProxy,self.proxy, self.proxyp))
        self.web = QWebView()
        self.web.loadProgress.connect(self.print_load_percent)
        self.web.loadFinished.connect(self.onDone1)
        self.web.load(QUrl(self.url))
        self.web.show()
        thread.start_new_thread( self.doExit, ("Thread-1", 1) )
        self.app.exec_()

if __name__=="__main__":
    #m = MTSParser("http://moipodpiski.ssl.mts.ru/lp/?SID=f456cee9-049f-4ba6-338c-000009682167", 9682167)
    #m.init(ua="webkit")
    m = MTSParser("", 9682167)
    m.confirm("6915")
