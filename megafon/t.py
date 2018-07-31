#coding=utf-8
import hashlib
import base64
import string
import random
import pickle
import urllib
import os
from django.http import HttpResponse
import httplib2
from HTMLParser import HTMLParser


def initMegafon(sub_id, url, redirect_url, workcnt=10):
    con = httplib2.Http()
    con.follow_redirects = True
    headers = {'Referer': redirect_url}
    resp, body = con.request(str(url), 'GET', headers=headers)
    page = body

    cookies = resp['set-cookie']

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
    
    
    if u"неверно" in body:
        print "FAIL"
    f = open("f.html", "w")
    f.write(body)
    d = dict(c2=resp['set-cookie'], localsid=data['localsid'], service_id=data['service_id'], opt_id1=data['opt_id1'])
    p = {'headers': headers, 'url': "http://wap.megafonpro.ru/is3nwp/psmweb/charge?localsid=%s" % data['localsid'], 'v_code':cap, 'data':d}
    pickle.dump(p, open('session_megafon_%s.subscribe' % sub_id, "w"))
    #code = sms
    
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
    print newurl
    if "wap.megafonpro.ru/is3nwp/psmcharge" not in body:
        print "Fail"
        return
    
    data['data']['code']= str(sms_code)
    resp, body = con.request(newurl, 'POST', headers=headers, body=urllib.urlencode(data['data']))
    print "Ok"

#
redirect_url = 'http://dostup.me'
url="http://partner2.jumpit.ru/col/mds4/partner/web_tmp/enter.jsp?msisdn=79233157065&status=new&serviceid=dostup&psid=oFDvv3NxsthD5zXx"
#initMegafon("8", url, redirect_url)
#confirmMegafon("8", "016040")
