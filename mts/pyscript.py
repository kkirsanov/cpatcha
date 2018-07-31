#coding=utf-8
import hashlib
import base64
import random
import pickle
import urllib
import os
from django.http import HttpResponse
import httplib2
from HTMLParser import HTMLParser

import beeline, mts, mts_solve_simple

import sys
sys.stderr = sys.stdout
def Download(url):
    import urllib2
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    lines = response.readlines()
    return "".join(lines)

def initMts(sub_id, url, redirect_url, ua, workcnt=10):
    m = mts.MTSParser(url, sub_id)
    m.init(ua)
 
def confirmMts(sub_id, sms_code):
    m = mts.MTSParser("", sub_id)
    m.confirm(str(sms_code))

def confirmMts2(sub_id, sms_code):
    import pickle
    data = pickle.load(open('session_mts_%s.subscribe' % str(sub_id), "r"))
    url = data['url']
    m = mts_solve_simple.Mts2(url)
    m.confirm(str(sms_code))

def loadProxy():
    f = open ("prx.lst")
    p = []
    for l in f:
        p.append(l.split(':'))
        p[-1][-1] = int(filter(lambda x:x in "0123456789", p[-1][-1]))
    return p


def initBee(sub_id, url, redirect_url, workcnt=10):
    import pickle
    p, pp=random.choice(loadProxy())
    proxy=p#"195.68.156.250"
    proxyp=pp#8080
    pi = httplib2.ProxyInfo(3, proxy, proxyp)
    con = httplib2.Http(proxy_info=pi)
    #con = httplib2.Http()
    con.follow_redirects = False
    headers = {'Referer': redirect_url}
    resp, body = con.request(str(url), 'GET', headers=headers)
    cookies = resp['set-cookie']
    headers['cookie'] = cookies
    headers['Origin'] = 'http://signup.beeline.ru'
    headers['Referer'] = url
    capcha = []
    inputs = {}
    action = []
    class Step1Parser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            a = dict(zip([at[0] for at in attrs], [at[1] for at in attrs]))
            def form(tag, a):
                action.append('http://signup.beeline.ru' + a['action'])
            def input(tag, a):
                if a.get('name'):
                    inputs[a['name']] = a['value']
            def img(tag, a):
                capcha.append('http://signup.beeline.ru' + a['src'])
            def default(tag, a):
                pass
            tags = {
                'form': form,
                'input': input,
                'img': img,
            }
    
            tags.get(tag, default)(tag, a)
    parser = Step1Parser()
    parser.feed(body)
    

    action = action[0]
    capcha = capcha[0]
    import time
    for _x in range(workcnt):
        resp, body = con.request(capcha, 'GET', headers=headers)
        if resp.status != 200: 
            raise Exception(u'error getting capture from beeline')
        
        f = open('capbee_%s_%d.png' % (sub_id, _x), "w")
        f.write(body)
        f.close()
        time.sleep(0.1)
    import beeline
    ret = []    
    for _x in range(workcnt):
        import Image
        i=Image.open('capbee_%s_%d.png' % (sub_id, _x))
        i.save('capbee_%s_%d.tif' % (sub_id, _x))
        ret.append(beeline.capcha('capbee_%s_%d.tif' % (sub_id, _x)))
        os.unlink('capbee_%s_%d.png' % (sub_id, _x))
        os.unlink('capbee_%s_%d.tif' % (sub_id, _x))

    import urllib
    ret = filter(lambda x:len(x) == 4, ret)
    try:
        inputs['verify_code'] = ret[0]
    except:
        print "capture parse error"
        return# Exception(u'capture parse error')
        
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    resp, body = con.request(action, 'POST', headers=headers, body=urllib.urlencode(inputs))
    if resp.status != 302: 
        raise Exception('error accept capture to beeline')
    del headers['Content-Type']

    data = {'headers': headers, 'url': resp['location'], 'v_code':ret[0], 'proxy':proxy, 'proxyp':proxyp}
    import pickle
    s = pickle.dumps(data)
    f = open('session_%s.subscribe' % str(sub_id), "w")
    f.write(s)
    print " captcha: ", ret[0]
    return sub_id

def confirmBee(sub_id, sms_code):
    import pickle
    data = pickle.load(open('session_%s.subscribe' % str(sub_id), "r"))
    headers = data['headers']
    url = data['url']
    proxy=data['proxy']
    proxyp=data['proxyp']
    pi = httplib2.ProxyInfo(3, proxy, proxyp)
    con = httplib2.Http(proxy_info=pi)

    con = httplib2.Http()
    con.follow_redirects = False
    resp, body = con.request(url, 'GET', headers=headers)
    headers['Referer'] = url
    inputs = {}
    action = []
    capcha = []

    class Step2Parser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            a = dict(zip([at[0] for at in attrs], [at[1] for at in attrs]))
            def form(tag, a):
                action.append('http://signup.beeline.ru' + a['action'])

            def input(tag, a):
                if a.get('name'):
                    inputs[a['name']] = a['value']

            def img(tag, a):
                capcha.append('http://signup.beeline.ru' + a['src'])

            def default(tag, a):
                pass

            tags = {
                'form': form,
                'input': input,
            }

            tags.get(tag, default)(tag, a)
    parser = Step2Parser()
    parser.feed(body)
    inputs['code'] = str(sms_code)
    action = action[0]

    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    resp, body = con.request(action, 'POST', headers=headers, body=urllib.urlencode(inputs))
    #f=open("f.html","w")
    #f.write(body)
    
    if resp.status != 302: return

    del headers['Content-Type']
    resp, body = con.request(resp['location'], 'GET', headers=headers)
    print "True"
    return True


def initMegafon(sub_id, url, redirect_url, workcnt=10):
    for tmp in range(10):
        #print 't1'
        import pickle
        con = httplib2.Http()
        con.follow_redirects = True
        headers = {'Referer': redirect_url}
        resp, body = con.request(str(url), 'GET', headers=headers)
        page = body
        try:
            cookies = resp['set-cookie']
        except:
            print "Fail cookie"
            return

        headers['cookie'] = cookies
        headers['Origin'] = 'http://wap.megafonpro.ru'
        headers['Referer'] = url
        
        import re
        r = re.compile("'captcha' src='([a-z:/\.0-9\?=A-Z&]*)'", re.DOTALL | re.MULTILINE)
        s = re.search(r, body)
        capcha_url = s.group(1)
        ccookies = None
        import datetime, time
        headers['Referer'] = resp['content-location']
        while True:
            #print "c"
            t = str(int(time.mktime(datetime.datetime.now().timetuple())))
            
            resp2, body = con.request(capcha_url + "&%s" % t, 'GET', headers=headers)
            ccookies = resp2['set-cookie']
            if resp.status != 200: 
                print "error"
            
            f = open('capmega_%s.png' % sub_id, "w")
            f.write(body)
            f.close()
            import megafon
            cap = megafon.capcha('capmega_%s.png' % sub_id)
            
            if "FAIL" not in cap:
                break
            os.unlink('capmega_%s.png' % sub_id)
        
        con = httplib2.Http()
        data = {}
        data['msisdn'] = re.search("<input type='text' value='([0-9]*)'", page, re.DOTALL | re.MULTILINE).group(1)
        data['localsid'] = re.search('<input type="hidden" name="localsid" value="([0-9a-zA-Z\.]*)"', page, re.DOTALL | re.MULTILINE).group(1)
        data['service_id'] = re.search('<input type="hidden" name="service_id" value="([0-9a-zA-Z\.]*)"', page, re.DOTALL | re.MULTILINE).group(1)
        data['opt_id1'] = re.search('<input type="hidden" name="opt_id1" value="([0-9a-zA-Z\.]*)"', page, re.DOTALL | re.MULTILINE).group(1)
        data['new_if'] = ''
        data['return_url'] = re.search('<input type="hidden" name="return_url" value="([/a-z0-9_\.\?=&A-Z]*)"', page, re.DOTALL | re.MULTILINE).group(1)
        data['captcha'] = str(cap)

        headers['cookie'] #+= ", " + ccookies 
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        resp, body = con.request("http://wap.megafonpro.ru/is3nwp/psmweb/charge?localsid=%s" % data['localsid'], 'POST', headers=headers, body=urllib.urlencode(data))
        
        
        if 'class="error"' in body:
            #print 'e'
            #print body
            continue
        #f = open("f.html", "w")
        #f.write(body)
        d = dict(c2=resp['set-cookie'], localsid=data['localsid'], service_id=data['service_id'], opt_id1=data['opt_id1'])
        p = {'headers': headers, 'url': "http://wap.megafonpro.ru/is3nwp/psmweb/charge?localsid=%s" % data['localsid'], 'v_code':cap, 'data':d}
        pickle.dump(p, open('session_megafon_%s.subscribe' % sub_id, "w"))
        
        print " captcha: ", cap
        return sub_id    

def confirmMegafon(sub_id, sms_code):
    import pickle
    data = pickle.load(open('session_megafon_%s.subscribe' % str(sub_id), "r"))
    #print data
    headers = data['headers']
    url = headers['Referer']
    headers['cookie'] = data['data']['c2']
    con = httplib2.Http()
    con.follow_redirects = False
    resp, body = con.request(url, 'GET', headers=headers)
    import re
    newurl = re.search("<form method='post' action='([/a-z0-9_\.\?=&A-Z:]*)'", body, re.DOTALL | re.MULTILINE).group(1)
    #print newurl
    if "wap.megafonpro.ru/is3nwp/psmcharge" not in body:
        print "Fail"
        return
    
    data['data']['code']= str(sms_code)
    resp, body = con.request(newurl, 'POST', headers=headers, body=urllib.urlencode(data['data']))

    print "True"
    try:
       z = Download(resp['Location'])
    except:
        pass
 
    try:
       z = Download(resp['location'])
    except:
        pass

 

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-a", "--action", dest="action", default = '',
                      help="action: init|confirm")
    
    parser.add_option("-o", "--operator", dest="operator", default = '',
                      help="operator: beeline|megafon|mts")
    
    parser.add_option("-i", "--id", dest="id", default = '',
                      help="session id")
    parser.add_option("-u", "--url", dest="url", default = '',
                      help="session url")
    parser.add_option("-r", "--redirect_url", dest="redirect_url", default = '',
                      help="redirect_url")
    parser.add_option("-d", "--data", dest="data", default = '',
                      help="confirmation data")
    (options, args) = parser.parse_args()
    if options.operator=='beeline':
        if options.action=='init':
            initBee(options.id, options.url.replace("\n","").replace("\r","").replace(" ",""), options.redirect_url.replace("\n","").replace("\r","").replace(" ",""))
            exit()
        if options.action=='confirm':
            confirmBee(options.id, options.data)
            exit()
    if options.operator=='megafon':
        if options.action=='init':
            try:
                initMegafon(options.id, options.url.replace("\n","").replace("\r","").replace(" ",""), options.redirect_url.replace("\n","").replace("\r",""), options.data.replace("\n","").replace("\r","").replace(" ",""))
            except Exception, e:
                print e
                pass
            exit()
        if options.action=='confirm':
            confirmMegafon(options.id, options.data)
            exit()
    if options.operator=='mts':
        #print options
        if options.action=='init':
            initMts(options.id, options.url.replace("\n","").replace("\r","").replace(" ",""), options.redirect_url.replace("\n","").replace("\r",""), options.data.replace("\n","").replace("\r","").replace(" ",""))
            exit()
        if options.action=='confirm':
            confirmMts(options.id, options.data)
            exit()
        if options.action=='confirm2':
            confirmMts2(options.id, options.data)
            exit()
print "Not implementated yet"
