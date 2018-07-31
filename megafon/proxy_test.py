import httplib2, httplib, socks
import time
import multiprocessing
import os
import random
def loadProxy():
    f = open ("proxy.lst")
    p = []
    for l in f:
        p.append(l.split(':'))
        p[-1][-1] = int(filter(lambda x:x in "0123456789", p[-1][-1]))
    return p

# :3128

def checkProxy(proxy):
    t0 = time.time()
    pi = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, proxy[0], proxy[1], proxy_user="VIPGKAKJ00aOF", proxy_pass="1q2w3e4r")
    con = httplib2.Http(proxy_info=pi, timeout=5)
    con.follow_redirects = False
    headers = {'Referer': 'http://www.ya.ru'}
    try:
        resp, body = con.request('http://www.ya.ru', 'GET', headers=headers)
        print "%s:%d" % (proxy[0], proxy[1]),
        if resp.status != 200: 
            print "fail"
        else:
            print time.time() - t0
    except Exception, e:
        print e, "%s:%d" % (proxy[0], proxy[1]), "fail"
    
if  __name__ == "__main__":
    p2 = loadProxy()
    p = multiprocessing.Pool(50)
    p.map(checkProxy, p2)

# checkProxy(p2[0])    
exit()   
# p2 = loadProxy()
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

import sys
app = QApplication(sys.argv)
web = QWebView()


QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.HttpProxy, p2[0][0], p2[0][1],user="asd" ,password="1q2w3e4r"))
# web.loadProgress.connect(self.print_load_percent)
# web.loadFinished.connect(self.onDone1)
# web.load(QUrl(self.url))
web.load(QUrl("http://2ip.ru/"))
web.show()
# self.web.show()
app.exec_()
