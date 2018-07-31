#import httplib2, httplib, socks
import time
import multiprocessing
import os
def loadProxy():
    f = open ("proxy.lst")
    p = []
    for l in f:
        p.append(l.split(':'))
        p[-1][-1] = int(filter(lambda x:x in "0123456789", p[-1][-1]))
    return p

# :3128

def checkProxy(proxy):
    import socket
    socket.setdefaulttimeout(5)
    t0 = time.time()
    pi = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, proxy[0], proxy[1])
    con = httplib2.Http(proxy_info=pi, timeout=1)
    con.follow_redirects = False
    headers = {'Referer': 'http://www.ya.ru'}
    try:
        resp, body = con.request('http://www.ya.ru', 'GET', headers=headers)
        if resp.status != 200: 
            print "fail"
            pass
        else:
            if (time.time()-t0) < 3:
                print "%s:%d" % (proxy[0], proxy[1]), 
                print time.time() - t0
    except Exception, e:
        print e, "%s:%d" % (proxy[0], proxy[1]), "fail"
        pass
if  __name__ == "__main__":
    p2 = loadProxy()
    checkProxy(p2[0])
    #p = multiprocessing.Pool(10)
    #p.map(checkProxy, p2)
#checkProxy(p2[0])
